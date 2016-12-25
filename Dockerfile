FROM ubuntu:xenial

WORKDIR /app

# We copy the requirements here and then install the deps in order to make
# better use of Docker caching which goes top to bottom. This means that if we
# did it otherwise, we'd have to rebuild everything without caching each time
# the code changes.
COPY requirements.txt dev-requirements.txt /app/
RUN apt update && apt install -y python3-pip python3-dev libpq-dev postgresql-client build-essential git && \
    pip3 install pip -r requirements.txt -r dev-requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# Clean the repo just in case the repo that built this Docker container wasn't
# tidy.
COPY . /app
RUN git clean -dfx

EXPOSE 5000
ENTRYPOINT ["flask", "run"]
