FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /agronom /pip_data

# Copy requirements only for caching and setup requirements
ADD agronom/requirements.txt /agronom/
ADD agronom/requirements/ /agronom/requirements/
WORKDIR /pip_data
RUN pip install -r /agronom/requirements.txt

# Copy sources
ADD agronom /agronom/

#WORKDIR /agronom
CMD python /agronom/manage.py migrate customuser && python /agronom/manage.py migrate
CMD python /agronom/manage.py runserver 0.0.0.0:8080
