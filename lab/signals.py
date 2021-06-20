from .models import ResultThrough, Order, Package
from django.db.models.signals import post_init,post_save,m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Order.investigation_package.through)
def order_changed(sender, instance, **kwargs):
    action = kwargs['action']
    if action == "pre_remove" or action == "post_add":
        changed_package = Package.objects.filter(pk__in = kwargs["pk_set"])
        for pkg_obj in changed_package:
            if action == "pre_remove":
                test_list = pkg_obj.linked_test.all()
                ResultThrough.objects.filter(order=instance,Test__in=test_list).delete()
            else:
                list(map(lambda test : ResultThrough.objects.get_or_create(order=instance,Test=test), pkg_obj.linked_test.all()))