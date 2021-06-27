from django import template
register = template.Library()


@register.filter(name='get_pkg_amt')
def getPkgAmt(pkg_name):
    from lab.models import Package
    pkg_obj = Package.objects.get(name=pkg_name)
    return f"Rs. {pkg_obj.amount}"
