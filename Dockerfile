FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip

WORKDIR /app

# Install Packages
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
#EXPOSE 8009