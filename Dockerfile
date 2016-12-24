FROM ubuntu:xenial

WORKDIR /app

COPY requirements.txt dev-requirements.txt app.py setup.cfg /app/
COPY boilerplateapp /app/boilerplateapp
COPY tests /app/tests
RUN apt update && apt install -y python3-pip python3-dev libpq-dev postgresql-client && \
    pip3 install pip -r requirements.txt -r dev-requirements.txt \
 && rm -rf /var/lib/apt/lists/*
# Needed for pytest when run tests with docker exec -it
#ENV TERM xterm
# Having both `ADD` and `VOLUME` allows us to decide later if we want to have the source code folder
# inside the container (we just don't mount the volume) or mount it to the folder on the host machine
# and have the sources outside of the container.
# VOLUME /backend
# RUN git clean -dfx  # Clean up cache files and such
# Expose volume, so we can edit sources locally and it will be reflected inside the container.
EXPOSE 5000
# CMD python3 manage.py runserver
# ENTRYPOINT ["pytest"]
