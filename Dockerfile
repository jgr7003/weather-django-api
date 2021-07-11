FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PROVIDER_OPEN_WEATHER_KEY 4f116cec33ba75ae18bc11303739b0db
RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y nfs-common
ADD . /code/