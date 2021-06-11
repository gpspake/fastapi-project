FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip

WORKDIR /app

RUN apt-get update
RUN apt-get install sqlite3

# Install Packages
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN alembic upgrade head
CMD python ./app/main.py