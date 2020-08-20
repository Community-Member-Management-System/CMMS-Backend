FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade --requirement requirements.txt
COPY cmms/ /app/
COPY docker-entrypoint.sh /entrypoint.sh
EXPOSE 8000
CMD ["/entrypoint.sh"]
