FROM    tiangolo/uwsgi-nginx-flask:python3.8

RUN     apt-get update -y
RUN     apt-get install tree default-libmysqlclient-dev -y
        
RUN pip install --upgrade pip

# set working directory to /app/
WORKDIR /app

# Install application dependencies
COPY reguirements.txt .
RUN pip install -r reguirements.txt

# Copy application code
COPY /app .

ENV STATIC_PATH /app/static
ENV STATIC_URL /static
ENV STATIC_INDEX 0

RUN ls -la /app
RUN tree /app
