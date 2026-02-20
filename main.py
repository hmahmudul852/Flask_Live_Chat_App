from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import os

app = Flask(__name__)
# Load SECRET_KEY from environment for production safety. Falls back to a
# development key when not set (do NOT use fallback in production).
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret_key_for_local")
# Disable Flask-SocketIO managed sessions to avoid compatibility issues
# with newer Flask RequestContext session implementation. We rely on the
# regular Flask `session` object inside Socket.IO handlers.
socketio = SocketIO(app, manage_session=False)

# In-memory store for rooms. Each key is a room code mapping to a dict with
# a member count and a list of recent messages. This is fine for development
# but not suitable for production across multiple processes or restarts.
rooms = {}

def generate_unique_code(length):
    """Generate a random uppercase room code of `length` that doesn't
    collide with an existing room in `rooms`.
    """
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/", methods=["POST", "GET"])
def home():
    """Home page — handles creating or joining a room via POST and
    renders the join/create form on GET.
    """
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    """Room page — verifies the session has a room and name and renders
    the chat room with stored messages.
    """
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    """Handle incoming Socket.IO `message` events.

    Clients may send either a plain string (e.g., `socket.send('hi')`) or
    a dictionary payload. This handler extracts the text, validates the
    session, stores the message in the room history, and broadcasts it to
    the room.
    """
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        return

    # Support string messages (socket.send('hi')) and dicts ({data: 'hi'})
    if isinstance(data, dict):
        message_text = data.get("data") or data.get("message") or data.get("text")
    else:
        message_text = data

    if message_text is None:
        return

    content = {"name": name, "message": message_text}
    # Use explicit `room=` keyword for clarity and compatibility.
    send(content, room=room)
    rooms[room]["messages"].append(content)
    print(f"{name} said: {message_text}")

@socketio.on("connect")
def connect(auth):
    """Socket.IO connect event: when a client connects, validate the
    session and add them to the room. Broadcast a join message and
    increment the member count.
    """
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, room=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """Socket.IO disconnect event: remove the user from the room and
    decrement member count. If the room becomes empty, delete it.
    """
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return

    # Only attempt to leave/join/update if room exists
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, room=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)