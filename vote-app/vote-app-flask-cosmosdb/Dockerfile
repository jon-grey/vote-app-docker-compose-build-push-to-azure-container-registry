FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7


RUN pip install --upgrade pip

WORKDIR /usr/src/app

# Install application dependencies
COPY reguirements.txt .
RUN pip install -r reguirements.txt

# Copy application code
COPY /app .