FROM python:3.6.5
MAINTAINER Your Name "fadzri@alterra.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
# Import variable env
# ENV THIS_UNAME=THIS_UNAME_VALUE
# ENV THIS_PWD=THIS_PWD_VALUE
# ENV THIS_DB_TEST=THIS_DB_TEST_VALUE
# ENV THIS_DB_DEV=THIS_DB_DEV_VALUE
# ENV THIS_DB_ENDPOINT=THIS_DB_ENDPOINT_VALUE

WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
