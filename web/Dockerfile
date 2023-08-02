# pull official base image
FROM python:3.8.17-alpine3.18

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

## Expose the port on which the Flask app will run
#EXPOSE 5000
#
## Define the command to run the Flask app using manage.py
#CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]