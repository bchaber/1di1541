FROM python:alpine
WORKDIR /var/www
ENV FLASK_APP app/app.py
ENV FLASK_DEBUG false
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5050
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app app
CMD ["flask", "run"]
