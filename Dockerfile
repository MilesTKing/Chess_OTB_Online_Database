FROM openjdk:11.0.16-jdk

RUN apt-get update && apt-get install -y python3 python3-pip

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app
# ✅ Copy ONLY requirements first
COPY requirements.txt .

# ✅ Install deps (this gets cached)
RUN pip3 install -r requirements.txt

# ✅ Then copy code (changes won’t break cache)
COPY . .

CMD ["python3", "src/processing/process_pgn.py"]