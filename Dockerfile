FROM alpine

WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache python3-dev py-pip build-base linux-headers && pip install -r requirements.txt

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000