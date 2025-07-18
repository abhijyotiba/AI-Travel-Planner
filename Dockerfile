FROM python:3.12-slim

WORKDIR /app

# Copy all files first (this includes setup.py or pyproject.toml)
COPY . .

# Install dependencies after all code is present
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

