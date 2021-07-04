from .models import ResultThrough, Order, Package
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.db.models import Sum

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


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, **kwargs):
    investigation_amt = 0
    pkg_list = instance.investigation_package.all()
    pkg_global_test_list = []
    for pkg in pkg_list:
        pkg_global_test_list.extend(pkg.linked_test.values_list("id",flat=True).all())    
    test_list = instance.investigation_test.all().exclude(id__in = pkg_global_test_list)
    if pkg_list:
        investigation_amt += pkg_list.aggregate(Sum('amount'))['amount__sum']
    if test_list:
        investigation_amt += test_list.aggregate(Sum('amount'))['amount__sum']

    instance.investigation_amount = investigation_amt
    final_amt = investigation_amt + instance.visiting_charge + instance.other_charge - instance.discount_amount
    balance_amt = final_amt - instance.advance_received
    Order.objects.filter(id=instance.id).update(
        investigation_amount = investigation_amt,
        final_amount = final_amt,
        balance_amount = balance_amt,
        )
