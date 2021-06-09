from django.db import models
from django.utils.translation import gettext_lazy as _

class SampleCollectionType(models.TextChoices):
        HOME = 'HOME', _('HOME')
        LAB = 'LAB', _('LAB')
        HOSPITAL = 'HOSPITAL', _('HOSPITAL')
        OTHER = 'OTHER', _('OTHER')
        
class GenderChoice(models.TextChoices):
        MALE = 'MALE', _('MALE')
        FEMALE = 'FEMALE', _('FEMALE')
        TRANSGENGER = 'TRANSGENGER', _('TRANSGENGER')
        UNDISCLOSED = 'UNDISCLOSED', _('UNDISCLOSED')
        OTHER = 'OTHER', _('OTHER')
        
        
class PaymentType(models.TextChoices):
        CASH = 'CASH', _('CASH')
        CHEQUE = 'CHEQUE', _('CHEQUE')
        CARD = 'CARD', _('CARD')
        OTHER = 'OTHER', _('OTHER')