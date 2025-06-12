FROM python:3.12
WORKDIR /devops-final-project

# Install the application dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy in the source code
COPY src ./src
#EXPOSE 5000 # current version doesnt need to expose ports

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask","run","--debug"]