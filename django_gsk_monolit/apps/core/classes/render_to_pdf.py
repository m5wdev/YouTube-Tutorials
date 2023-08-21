from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


class RenderToPDF:

    @staticmethod
    def render(path: str, params: dict, filename='my_filename'):
        template = get_template(path)
        html = template.render(params)
        result  = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result .getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={filename}.pdf'
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)
