FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=apprentice.py

# Note: this is an empty, DEV sqlite db so we should
# look into a proper, persistent db
RUN echo "db.create_all(); exit()" | flask shell

ENTRYPOINT [ "flask" ]

CMD [ "run", "--host=0.0.0.0" ]