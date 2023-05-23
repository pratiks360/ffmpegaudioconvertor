FROM python:3
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python", "app.py"]