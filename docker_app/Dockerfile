FROM python:3
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app .
EXPOSE 8000
CMD ["/bin/bash", "/app/gunicorn.sh"]
