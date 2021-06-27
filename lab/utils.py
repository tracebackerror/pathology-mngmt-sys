from .models import ResultThrough, LabInformation
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from urllib.parse import urljoin

def get_report_context(order_obj):
    context = {}
    pkg_test_id_name = order_obj.investigation_package.values_list('linked_test','name').all()
    pkg_test = {id:name for id,name in pkg_test_id_name}
    results = ResultThrough.objects.filter(order = order_obj).order_by("-report_date")
    full_reports = {}
    others_test = []
    for res in results:
        pkg_name = pkg_test.get(res.Test.id,None)
        if pkg_name:
            if full_reports.get(pkg_name,None):
                full_reports[pkg_name].append(res)
            else:
                full_reports[pkg_name] = [res]
        else:
            others_test.append(res)

    if len(others_test) > 0:
        full_reports["Others Report"] = others_test
    
    context['full_reports'] = full_reports.items()
    context['full_reports_count'] = len(full_reports)
    context['order_obj'] = order_obj
    context['lab_info'] = LabInformation.objects.all().first()

    return context


def fetch_resources(uri, rel):
    uri.replace(settings.MEDIA_URL, "")
    path = urljoin(settings.ABS_URL,uri)
    return path
                
def convert_html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
    if not pdf.err:
        return result.getvalue()
    return None