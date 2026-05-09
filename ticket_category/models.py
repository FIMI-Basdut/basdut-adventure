import uuid
from django.db import models
from django.core.validators import MinValueValidator
# from event.models import Event

class TicketCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=255, null=False, blank=False)
    #event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='ticket_categories')
    category_name = models.CharField(max_length=50, null=False, blank=False)
    quota = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], null=False, blank=False)

    class Meta:
        db_table = 'TICKET_CATEGORY'
        ordering = ['event_name', '-price']
        #ordering = ['event__name', '-price']

    def __str__(self):
        return f"{self.category_name} - {self.event_name}"
        #return f"{self.category_name} - {self.event.name}"