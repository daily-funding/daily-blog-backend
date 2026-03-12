## 가상환경 세팅 
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## DB migration
```bash
python manage.py makemigrations --settings=config.settings.local
python manage.py migrate --settings=config.settings.local
```
## 관리자 계정 만들기
```bash
python manage.py createsuperuser --settings=config.settings.local
```

## Server 실행
```bash
python manage.py runserver
#로컬
python manage.py runserver --settings=config.settings.local

```

## 배포 전 요구사항 맞추기
```
pip freeze > requirements.txt
```