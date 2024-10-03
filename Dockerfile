FROM python:3.12-slim

EXPOSE 8501

WORKDIR /app

COPY app.py requirements.txt 


RUN apt-get update && apt-get install -y \
        build-essential \
        sofware-properties-common \
        git \
        && rm -rf /var/apt/lists/*

RUN pip install -upgrade pip
RUN pip3 install -r requirements.txt


ENTRYPOINT ["streamlit", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]