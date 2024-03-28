FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
COPY .env .
RUN pip install --ignore-installed -r ./requirements.txt
EXPOSE 8080
CMD ["python3", "index.py"]
#could be better if gunicon is used although no difference is made.
