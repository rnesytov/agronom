FROM python:3.6

RUN apt-get update -q && apt-get install --no-install-recommends -yq binutils libproj-dev gdal-bin

ENV PYTHONUNBUFFERED 1
RUN mkdir /agronom /pip_data

# Copy requirements only for caching and setup requirements
ADD agronom/requirements.txt /agronom/
ADD agronom/requirements/ /agronom/requirements/
WORKDIR /pip_data
RUN pip install -r /agronom/requirements.txt

# Copy sources
ADD agronom /agronom/

WORKDIR /agronom
