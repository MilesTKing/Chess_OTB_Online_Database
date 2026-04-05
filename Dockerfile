FROM openjdk:11.0.16-jdk

RUN apt-get update && apt-get install -y python3 python3-pip

ENV PYTHONPATH=/app
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "src/processing/process_pgn.py"]