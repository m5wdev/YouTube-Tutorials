FROM python:3.10-slim

# Set python variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN adduser -D myuser
# USER myuser
# WORKDIR /home/myuser/backend
# COPY --chown=myuser:myuser . .

WORKDIR /app/backend

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements/requirements.txt
