FROM python:alpine

LABEL MAINTAINER="Arian Ventura Rodriguez (V3N2R4) <arianventura94@gmail.com>"

WORKDIR /AuthMicroservice


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /AuthMicroservice/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ /AuthMicroservice/

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
