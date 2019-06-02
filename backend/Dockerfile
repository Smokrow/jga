FROM ailispaw/alsa-utils

COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install espeak -y
RUN apt-get install -y python3 python3-pip
RUN apt install -y espeak python3-espeak speech-dispatcher-espeak
RUN apt-get install -y alsa-utils 
RUN pip install -r requirements.txt
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser
USER appuser
EXPOSE 5555

CMD ["python3", "main.py"]

