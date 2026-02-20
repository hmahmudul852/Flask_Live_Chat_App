import os
import sys
import time
import pytest

# Ensure project root is on sys.path so `main` can be imported when pytest
# runs from the tests directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, socketio, rooms, generate_unique_code


def test_generate_unique_code():
    code = generate_unique_code(4)
    assert isinstance(code, str)
    assert len(code) == 4


def test_create_room_and_send_message():
    # Create a Flask test client and POST to create a room
    flask_client = app.test_client()
    resp = flask_client.post('/', data={'name': 'Tester', 'create': '1'}, follow_redirects=True)
    assert resp.status_code in (200, 302)

    # There should be at least one room created
    assert len(rooms) >= 1
    room = next(iter(rooms.keys()))

    # Create a Socket.IO test client that shares the Flask test client session
    sock_client = socketio.test_client(app, flask_test_client=flask_client)
    assert sock_client.is_connected()

    # Send a plain string message (handled by the server)
    sock_client.send('hello')
    # small pause to allow server handlers to run
    time.sleep(0.05)

    # Verify message stored in room history
    assert rooms[room]['messages'][-1]['message'] == 'hello'
    assert rooms[room]['members'] == 1

    # Disconnect and ensure room is cleaned up (or members decremented)
    sock_client.disconnect()
    time.sleep(0.05)

    # After disconnect, room may be removed if no members left
    assert room not in rooms or rooms.get(room, {}).get('members', 0) == 0
