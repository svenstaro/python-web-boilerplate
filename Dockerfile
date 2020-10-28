FROM python:3.8

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml /app
COPY dependecies.sh /app
RUN chmod +x dependecies.sh
RUN ./dependecies.sh

COPY app.py /app
COPY boilerplateapp/ /app/boilerplateapp
COPY tests/ /app/tests
COPY run.sh /app
RUN chmod +x run.sh

EXPOSE 5000

CMD ["./run.sh"]
