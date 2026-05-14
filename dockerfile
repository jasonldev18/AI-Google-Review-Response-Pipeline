#This file contains step-by-step instructions on how Docker should build container image

#start with python 3.11 env
FROM python:3.11-slim
#sets working dir inside container
WORKDIR /app
#copies requirements.txt into container first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#copies rest of code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]