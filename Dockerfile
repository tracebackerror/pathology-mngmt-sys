FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /project

# Install Git
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone https://github.com/tracebackerror//pathology-mngmt-sys -b student /project

# Install project dependencies and migrations
RUN pip install -r requirements.txt

# Run the applicatio
CMD python manage.py runserver 0.0.0.0:8000