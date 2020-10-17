FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=apprentice.py

# Note: this is an empty, DEV sqlite db so we should
# look into a proper, persistent db
RUN echo "db.create_all(); exit()" | flask shell

# Wait for elasticsearch to be up and then start flasking
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD /wait && flask run --host=0.0.0.0