FROM python:3.8

WORKDIR /karton/
COPY karton/minhash/ minhash
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python", "-m", "minhash" ]