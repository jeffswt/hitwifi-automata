pipenv install
pipenv shell
pip install -r requirements.txt
pip install pyinstaller
ffmpeg -i ../assets/icon.png ../assets/icon.ico
pyinstaller --onefile --windowed --icon ../assets/icon.ico hitwa.pyw