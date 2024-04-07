# pull official base image
FROM python:3.12.1

# set working directory
WORKDIR /home/app/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/home/app/web

# install system dependencies
#RUN apt-get update \
#  && apt-get -y install netcat-traditional gcc postgresql \
#  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN chmod a+x ./entrypoint.sh
# add app
COPY . .

# add entrypoint.sh
#COPY ./entrypoint.sh .
RUN chmod +x /home/app/web/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]