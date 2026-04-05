FROM openjdk:11.0.16-jdk
# Install Python + Spark deps if needed
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "src/processing/process_games.py"]X