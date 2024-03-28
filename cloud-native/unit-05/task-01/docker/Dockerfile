# Dockerfile metadata
FROM python:3.10
LABEL Author="Victor Fernandez III, @cyberphor"

# install poetry (the second pip sentence is strictly for the submitter)
RUN python -m pip install poetry &&\
    python -m pip install djangorestframework-simplejwt[crypto] djangorestframework Django mysqlclient

# set the working directory
WORKDIR /opt/login/

# set the working directory
WORKDIR /opt/login/

# copy the source code and container entrypoint script
COPY src/ src/
COPY docker/entrypoint.sh src/entrypoint.sh

# set the working directory
WORKDIR /opt/login/src/

# install the project's Python dependencies 
RUN poetry install --no-interaction --no-ansi

# send stdout and stderr streams to the console
ENV PYTHONUNBUFFERED=1

# run the login service
ENTRYPOINT ["bash", "entrypoint.sh"]