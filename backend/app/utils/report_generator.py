
class ReportGenerator:
    def __init__(self):
        wkhtmltopdf = WKhtmlToPdf(
            url='http://www.wikipedia.org',
            output_file='report.pdf',
        )
        wkhtmltopdf.render()