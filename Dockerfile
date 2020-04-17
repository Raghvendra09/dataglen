FROM python:3.6.10-slim 
LABEL maintainer="Raghvendra Singh <raghvendra.iiitv@gmail.com>"
ENV PYTHONUNBUFFERED  1

RUN mkdir /dataglen
WORKDIR /dataglen
ADD . /dataglen/

RUN pip install -r requirements.txt
RUN env SECRET_KEY='FAKESECRET' python3 manage.py collectstatic --no-input
CMD gunicorn -w 4 -b 0.0.0.0:8001 dataglen.wsgi
