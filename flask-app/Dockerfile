FROM python:3.7.1-alpine3.8

WORKDIR /app

EXPOSE "5000"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
