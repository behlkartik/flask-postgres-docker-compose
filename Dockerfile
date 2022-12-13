FROM python:3.10
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app

# RUN python3 -m venv /opt/flask_env
# RUN . /opt/flask_env/bin/activate
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U Flask
ENV FLASK_ENV=development