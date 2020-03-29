pip install gunicorn

gunicorn -w 4 -b 0.0.0.1:9001 run:app