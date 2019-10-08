FROM python:3.7

WORKDIR /app/

RUN apt-get -y install ca-certificates

COPY ./requirements.txt /

RUN apt-get update
#RUN apt-get install -y wkhtmltopdf xvfb xauth xfonts-base xfonts-75dpi fontconfig vim

#ENV WKHTML2PDF_VERSION '0.12.5'
#RUN apt-get install -y openssl build-essential xorg xvfb xauth xfonts-base xfonts-75dpi libssl-dev vim
#RUN wget -O wkhtmltox.deb "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox_${WKHTML2PDF_VERSION}-1.stretch_amd64.deb"
#RUN dpkg -i wkhtmltox.deb

#ENV WKHTML2PDF_VERSION '0.12.4'
#RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz
#RUN tar -xJf "wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz"
#RUN mv wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

RUN pip install -r /requirements.txt

COPY . /app
ENV PYTHONPATH=/app

RUN pytest /app/tests/ -W ignore::DeprecationWarning

EXPOSE 8000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/app/start.sh"]
