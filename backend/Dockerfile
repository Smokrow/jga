FROM python:3.5

COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install espeak -y
RUN pip install -r requirements.txt
EXPOSE 5555

CMD ["python", "main.py"]

