```bash
source .venv/bin/activate
pip freeze > requirements.txt
pip install -r requirements.txt
```

DB migration
```bash
python manage.py migrate --settings=config.settings.local
```

```bash
python manage.py runserver
#로컬
python manage.py runserver --settings=config.settings.local

```