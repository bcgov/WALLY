FROM python:3.7

WORKDIR /app/
RUN useradd wally -M -G root -u 1021 && chmod -R 775 /app \
  && chown -R wally:root /app \ 
  && apt-get -y install ca-certificates

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app
ENV PYTHONPATH=/app

RUN pytest /app/tests/ -W ignore::DeprecationWarning

EXPOSE 8000
USER 1021

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start.sh"]
