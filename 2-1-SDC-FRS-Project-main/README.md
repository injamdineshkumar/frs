# Face Recognition System

A student face registration and recognition app using OpenCV LBPH, with a
Streamlit webcam interface and a command-line alternative.

## Requirements

- Python 3.10 or newer
- A webcam
- Windows, macOS, or Linux

## Install and run on Windows

Open PowerShell in this project folder (the folder containing `app.py` and
`requirements.txt`) and run:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
python -m streamlit run .\app.py
```

Using `python -m streamlit` works even if the Python `Scripts` directory is not
on `PATH`. If PowerShell blocks virtual-environment activation, run the
`python -m pip` and `python -m streamlit` commands using
`.\.venv\Scripts\python.exe` instead.

The first run ensures the OpenCV Haar cascade file is available. If it is not
already in `haarcascades`, the app copies it from OpenCV or downloads it, so
network access may be needed.

## Use the app

1. Open **Register Student**, enter a positive numeric roll number, name, and
   gender, then allow browser camera access and capture face samples.
2. Open **Train Model** and train or retrain the model after registering
   students.
3. Open **Recognize Face** and allow camera access for live recognition.
4. Use **Student List** to review sample status or delete a student and their
   captured samples.

Student details are stored in `data/students.json`, face samples in
`data/dataset`, and the trained model in `data/trainer`. These files are local
project data and should be backed up separately if they need to be retained.
Live camera frames are sent to the server running the app for processing. If
the app is hosted on a remote server, frames and stored data are handled by that
server's operator. Deleting a student removes their record and captured sample
folder; retrain the model afterward to replace the existing trained model.
Obtain appropriate authorization before collecting face samples and establish
your own access and retention rules. The
[Streamlit privacy policy](https://streamlit.io/privacy-policy) covers
Streamlit's services, not this project's data practices.

## Optional webcam relay configuration

The app uses a public STUN server by default. For networks that require TURN,
configure either Cloudflare TURN credentials:

- `CLOUDFLARE_TURN_KEY_ID`
- `CLOUDFLARE_TURN_KEY_API_TOKEN`

or your own TURN server:

- `TURN_SERVER_URLS` (comma-separated URLs)
- `TURN_USERNAME`
- `TURN_CREDENTIAL`

Keep credentials private; do not commit them to source control.

## Command-line mode

After installing the requirements, run:

```powershell
python .\main.py
```

The command-line camera capture and recognition windows use OpenCV. Press `q`
in the camera window to stop capture or recognition.
