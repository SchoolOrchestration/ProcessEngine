FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
COPY test_requirements.txt /code/
RUN pip install -U pip
RUN pip install -r test_requirements.txt
COPY . /code/
