FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=apprentice.py

# Note: this is an empty, DEV sqlite db so we should
# look into a proper, persistent db
RUN echo "db.create_all(); exit()" | flask shell

# Create startup script to wait for other containers before starting server
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait \
    && printf '#!/bin/bash\n/wait && "$@"' >> /wait-then \
    && chmod +x /wait-then

# Wait for $WAIT_HOSTS to be up and then start flasking
ENTRYPOINT [ "/wait-then" ]
CMD [ "flask", "run", "--host=0.0.0.0" ]