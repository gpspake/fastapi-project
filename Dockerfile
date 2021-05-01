FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Install Packages
RUN pip install --upgrade pip && pip install -r requirements.txt
