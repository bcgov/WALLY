FROM python:3.7

WORKDIR /app/

COPY ./requirements.txt /

RUN apt-get update
RUN apt-get install -y wkhtmltopdf xvfb xauth xfonts-base xfonts-75dpi fontconfig

RUN pip install -r /requirements.txt

COPY . /app
ENV PYTHONPATH=/app

RUN pytest /app/tests/ -W ignore::DeprecationWarning

EXPOSE 8000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start.sh"]
