FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install requests beautifulsoup4 flask
CMD ["python", "main.py"]
