# Python Live Chat App
Uses Flask Sockets to create a live chat room application.

## Environment

- **SECRET_KEY**: Set a secure `SECRET_KEY` environment variable in production. Example (macOS/Linux):

```bash
export SECRET_KEY='a-very-secure-random-string'
```

The app falls back to a development key when `SECRET_KEY` is not set; do not use the fallback key in production.

## Running

Follow the steps below to run the app locally. These show creating/activating a virtual environment, setting the `SECRET_KEY`, and starting the server.

macOS / Linux (bash/zsh):

```bash
# create and activate venv (only if you haven't already)
python3 -m venv .venv
source .venv/bin/activate

# (optional) install dependencies if you have a requirements file
pip install -r requirements.txt || true

# set a secure secret and start the app
export SECRET_KEY='a-very-secure-random-string'
python3 main.py
```

Windows PowerShell:

```powershell
# create and activate venv
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# set the secret and start the app
$env:SECRET_KEY = 'a-very-secure-random-string'
python main.py
```

Windows (cmd.exe):

```cmd
# create and activate venv
python -m venv .venv
.venv\Scripts\activate

# set the secret and start the app
set SECRET_KEY=a-very-secure-random-string
python main.py
```

After the server starts, open http://localhost:5000 in your browser.
## Features

- Real-time chat using Flask-SocketIO
- Multiple chat rooms
- User-friendly interface
- Message broadcasting to all users in a room
- Simple session management

## Project Structure

```
Flask_Live_Chat_App/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── static/              # Static files (CSS, JS)
│   └── css/
│       └── style.css
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   └── room.html
├── tests/               # Unit tests
│   └── test_main.py
└── README.md            # Project documentation
```

## Usage

1. Start the server as described above.
2. Open your browser and go to [http://localhost:5000](http://localhost:5000).
3. Enter a username and room name to join or create a chat room.
4. Start chatting in real time!

## Testing

To run unit tests:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License.
