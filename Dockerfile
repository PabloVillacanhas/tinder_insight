FROM python:3.8.1-slim

# install netcat
RUN apt-get update \
  && apt-get -y install gcc libpq-dev python-dev netcat \
  && apt-get clean
# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .

# install requirements
RUN pip3 install pipenv
RUN pipenv install --deploy --ignore-pipfile

# run server
CMD ["./entrypoint.sh"]
