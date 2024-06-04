1. start venv (may defer, this is done on Ubuntu22.04)
```
apt install python3.10-venv
python -m venv venv
source venv/bin/activate
```

3. install requests dependency
```
pip install requests
pip freeze > requirements.txt
```

or
```
pip install -r requirements.txt
```

3. prepare backup folder
```
mkdir zone_backups
```

4. run the script
```
python backup.py
```
