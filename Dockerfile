FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-c", "from web.app import create_app; import json, os; config = json.load(open('config.json')); app = create_app(config); app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))"]
