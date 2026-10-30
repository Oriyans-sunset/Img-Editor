FROM python:3.8

WORKDIR /usr/src/app

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "run.py" ]