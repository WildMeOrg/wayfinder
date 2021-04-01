# Wild Me Wayfinder 

## Development 
```
virtualenv env 
source env/bin/activate
pip3 install 
python app.py
```

## Production
`gunicorn app:app`

## Initialize db
Enter python shell and run the following commands
```
from app import db
db.create_all()
```