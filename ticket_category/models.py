import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q
#from event.models import Event

class TicketCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey('Event', on_delete=models.CASCADE,db_column='event_id', related_name='ticket_categories')
    category_name = models.CharField(max_length=50, null=False, blank=False)
    quota = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], null=False, blank=False)

    class Meta:
        db_table = 'TICKET_CATEGORY'
        ordering = ['event__event_title', '-price']

    def __str__(self):
        return f"{self.category_name} - {self.event.event_title}"


class UserAccount(models.Model):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'user_account' 
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'

    def __str__(self):
        return self.username


class Venue(models.Model):
    venue_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue_name = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'venue'
        constraints = [
            models.CheckConstraint(check=Q(capacity__gt=0), name='check_capacity_positive')
        ]

    def __str__(self):
        return f"{self.venue_name} ({self.city})"


class Organizer(models.Model):
    organizer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.EmailField(max_length=100, null=True, blank=True)
    
    user = models.ForeignKey(
        UserAccount, 
        on_delete=models.CASCADE, 
        db_column='user_id',
        related_name='organizers'
    )

    class Meta:
        db_table = 'organizer'

    def __str__(self):
        return self.organizer_name


class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_datetime = models.DateTimeField(null=False, blank=False)
    event_title = models.CharField(max_length=200, null=False, blank=False)
    
    venue = models.ForeignKey(
        Venue, 
        on_delete=models.PROTECT,
        db_column='venue_id',
        related_name='events'
    )
    
    # Foreign Key ke Organizer
    organizer = models.ForeignKey(
        Organizer, 
        on_delete=models.CASCADE, 
        db_column='organizer_id',
        related_name='events'
    )

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.event_title