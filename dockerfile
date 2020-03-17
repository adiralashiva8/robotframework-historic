FROM python:3.6

# Install any needed packages
RUN apt-get update \
&&  rm -rf /var/lib/apt/lists/*
RUN pip install git+https://github.com/accruent/robotframework-historic

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the rf-historic flask with argument to connect to db
#CMD rfhistoric -s localhost -t 3306 -u username -p password -a 0.0.0.0
CMD rfhistoric -s "${SQLHOST}" -t "${PORT}" -u "${USERNAME}" -p "${PASSWORD}" -a "${FLASKHOST}"

#docker run -it -p 5000:5000 --name rfhistoric rfhistoric:latest bash