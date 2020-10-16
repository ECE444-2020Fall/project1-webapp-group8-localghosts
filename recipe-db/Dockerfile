FROM elasticsearch:7.9.2

# Install dependencies for Python3 loading script
COPY ./loading-scripts/requirements.txt .
RUN yum update -y -q \
    && yum install -y -q python3 \
    && pip3 install --no-cache-dir -r requirements.txt
COPY ./loading-scripts/ .

# Set environment variables e.g. for running a single node cluster of elasticsearch
ENV discovery.type=single-node

# Create modifiable elasticsearch data directory so we can pre-load data https://stackoverflow.com/a/39873112
RUN mkdir /data \
    && chown -R elasticsearch:elasticsearch /data \
    && echo 'path.data: /data' >> config/elasticsearch.yml

# Spin up a temporary instance of elasticsearch so we can populate the data in the image 
RUN docker-entrypoint.sh elasticsearch -p /tmp/epid > /dev/null 2>&1 & echo "Waiting for elasticsearch to start..." \
    && until curl -s -o /dev/null 'http://localhost:9200' ; do sleep 1 ; done \
    # Once it's up, we can call our bulk insertion script
    && python3 load.py \
    # When we're done setting up the data, spin down the temp instance of elasticsearch
    && kill $(cat /tmp/epid) \
    && wait $(cat /tmp/epid); \
    exit 0

# And now everything should be pre-loaded and ready to go @port 9200 (& 9300)