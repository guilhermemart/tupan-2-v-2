FROM ubuntu:18.04

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="America/Sao_Paulo"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntugis/ppa -y
RUN apt-get update && apt-get install -y\
	gcc\
	python3-dev\
	postgresql\
	musl-dev\
	python3-tk \
	build-essential \
	libssl-dev \
	zlib1g-dev \
	libbz2-dev \
	libreadline-dev \
	libsqlite3-dev \
	wget \
	curl \
	llvm \
	gettext \
	libncurses5-dev \
	tk-dev \
	tcl-dev \
	blt-dev \
	libgdbm-dev \
	git \
	python-dev \
	python3-dev \
	aria2 \
	vim \
	libnss3-tools \
	python3-venv \
	liblzma-dev \
	libpq-dev \
	make\
	libgdal-dev\
	gdal-bin\
	python3-pip

RUN python3 -m pip install --upgrade pip
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/included/gdal
#RUN python3 -m pip install pipenv
RUN wget https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/software/rsl-v1.50.tar.gz
RUN tar -zxf rsl-v1.50.tar.gz
RUN cd rsl-v1.50 && ./configure && make && make install
ENV RSL_PATH=/usr/local/trmm
ENV PIPENV_NO_INHERIT=True
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir tupan-2
#RUN cd tupan-2 && pipenv install
RUN ogrinfo --version
#RUN pipenv install GDAL==2.4.2
RUN pip install GDAL==2.4.2
#trocar sempre que mudar a versao do gdal
#RUN pipenv install psycopg2 gunicorn wradlib georaster selenium requests Django pandas matplotlib\
#   scipy requests dj-database-url whitenoise
RUN pip install psycopg2 gunicorn wradlib georaster selenium requests Django pandas matplotlib\
    scipy requests dj-database-url whitenoise arm-pyart netCDF4 h5py

COPY . .

#RUN pipenv run python3 manage.py collectstatic --noinput
#RUN python3 manage.py collectstatic --noinput

#CMD gunicorn c137.wsgi:application --bind 0.0.0.0:$PORT

#RUN useradd -m python_user
#WORKDIR /home/python_user
#WORKDIR /app
#USER python_user
#chmod -x no buildpack-run não esquecer

