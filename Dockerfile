FROM python:3
RUN apt-get update && apt-get install -y ffmpeg
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD streamdownloader.py /
RUN mkdir /output
RUN mkdir /config
CMD ["python", "./streamdownloader.py"]