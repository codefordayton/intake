FROM python:3.5

RUN apt-get update && apt-get install -y \
    curl
RUN apt-get install -y build-essential
RUN apt-get install -y libssl-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y python-dev

RUN curl --silent --location https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install --global gulp-cli

RUN mkdir -p /data/web

WORKDIR /data/web

# INSTALL NODE DEPENDENCIES
COPY package.json .
RUN npm install

ENV PYTHONUNBUFFERED 1

# INSTALL PYTHON DEPENDENCIES
RUN mkdir requirements
COPY requirements requirements
RUN pip install -r requirements/dev.txt

COPY . .

RUN python /data/web/manage.py collectstatic --noinput

