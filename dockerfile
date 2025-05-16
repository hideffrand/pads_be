FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5050 
# sesuaikan port ^
CMD ["python", "app.py"]

# jangan lupa ganti nama jadi Dockerfile