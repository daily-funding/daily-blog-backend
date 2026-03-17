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
```bash
pip freeze > requirements.txt
```

## pytest
```bash
# 전체 pytest 수행
pytest -v

#print 출력 보기
pytest -s

# 특정 파일의 특정 함수만 테스트
pytest {테스트파일명}.py -k {테스트함수명}

# 특정 폴더의 파일들만 테스트
pytest blog/tests/admin -q
```

## 서버에 수동 cronjob 실행 등록 
가상환경이 루트에 설치되어있다는 전제하에 실행 
```bash
crontab -e

0 3 * * * cd /home/ubuntu/daily-blog-backend && DJANGO_SETTINGS_MODULE=config.settings.prod /home/ubuntu/daily-blog-backend/.venv/bin/python manage.py cleanup_orphan_post_images >> /home/ubuntu/daily_blog_cleanup.log 2>&1
```
