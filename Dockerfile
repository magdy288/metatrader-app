FROM python:3.12-slim

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./requirements.txt 


RUN pip install -r requirements.txt

EXPOSE 8501

COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]