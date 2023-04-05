# Vavruska downloader

Script to download all dancing videos from Vavruska.

## HOW TO
1. Create file `passwords` and fill passwords from emails. **You have to use your own passwords.** One password = one line.
```
password-for-course-1
password-for-course-2
password-for-course-3
```
2. Create venv and install requirements
```python
python3 -m venv venv
. venv/bin/activate
python -m pip install -r requirements.txt
```
3. Run script
```
python run.py
```
4. By default your videos will be in the `videos` folder in the current working directory.