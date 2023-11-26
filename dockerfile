FROM python:3.11.2-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY /app .
ENV PORT=8080
EXPOSE 8080
CMD [ "python3","-u", "app.py"]