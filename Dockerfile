FROM microsoft/mssql-tools as mssql
FROM python:3.8.0-alpine

COPY --from=mssql /opt/microsoft/ /opt/microsoft/
COPY --from=mssql /opt/mssql-tools/ /opt/mssql-tools/
COPY --from=mssql /usr/lib/libmsodbcsql-13.so /usr/lib/libmsodbcsql-13.so

# gcc, ffi, postgresql
WORKDIR /tmp
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo libc-dev linux-headers  
RUN apk update && \
    apk add git g++ make cmake libevent-dev libev-dev && \
    apk add perl zlib python3-dev openssl-dev openldap-dev redis && \
    apk add libxml2-dev libffi-dev postgresql-dev && \
    apk add libxslt-dev build-base jpeg-dev zlib-dev && \
    apk add freetype-dev lcms2-dev openjpeg-dev tiff-dev fontconfig ttf-dejavu && \
    apk add tk-dev tcl-dev bash musl-dev jpeg-dev zlib-dev cairo-dev pango-dev gdk-pixbuf-dev && \
    apk add py3-cffi py3-pillow py-lxml unixodbc unixodbc-dev boost-dev
RUN apk add mariadb-dev mariadb-client mariadb-connector-c

ENV LIBRARY_PATH=/lib:/usr/lib

# set work directory
WORKDIR /usr/src/code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

# install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install cryptography
COPY ./requirements.txt /usr/src/code/requirements.txt
RUN pip install -r requirements.txt --no-binary :all:
RUN pip install mysqlclient
RUN pip install tox 
RUN mkdir /etc/adjutant/

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/code/entrypoint.sh
COPY ./etc/adjutant.dev.yaml /etc/adjutant/adjutant.yaml

# copy project
COPY . /usr/src/code/

# run entrypoint.sh
CMD ["/usr/src/code/entrypoint.sh"]