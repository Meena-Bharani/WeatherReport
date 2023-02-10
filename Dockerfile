FROM python:3.8.5-alpine

RUN pip install --upgrade pip

RUN apk update && \
    apk add build-base && \
    pip install numpy==1.24.2 && \
    pip install pandas==1.4.0

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN mkdir /app
COPY ./ /app
WORKDIR /app

COPY ./release-task.sh /
ENTRYPOINT ["sh","/release-task.sh"]

EXPOSE 8000
CMD ["python", "manage.py","runserver","127.0.0.1:8000"]