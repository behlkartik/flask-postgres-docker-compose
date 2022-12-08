FROM python:3.10
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
# RUN apt-get update && \
#     apt-get install build-deps gcc musl-dev && \
#     apt-get install postgresql-dev && \
#     rm -rf /var/cache/apt-get/*
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U Flask
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python", "app.py"]