FROM python:3
RUN mkdir /opt/app
WORKDIR /opt/app
RUN pip install virtualenv
RUN virtualenv -p python3 .
RUN . bin/activate
RUN bin/pip install --upgrade pip
RUN bin/pip install Django
RUN bin/pip install djangorestframework
RUN bin/pip install mysqlclient
RUN bin/pip install django-cors-headers
RUN bin/pip install requests
WORKDIR /opt/app/tpaga
CMD /opt/app/bin/python /opt/app/tpaga/manage.py runserver 0.0.0.0:8000
