# Python-Live-Chat-App
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
