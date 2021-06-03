FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip

WORKDIR /app

# Install Packages
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app
CMD python ./app/main.py