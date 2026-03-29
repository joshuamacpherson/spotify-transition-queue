python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --noconsole --onefile main.py