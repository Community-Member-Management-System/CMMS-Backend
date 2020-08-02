FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade --requirement requirements.txt
COPY cmms/ /app/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
