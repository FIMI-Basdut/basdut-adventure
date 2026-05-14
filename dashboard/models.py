import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q



class Role(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'ROLE'

    def __str__(self):
        return self.role_name


class UserAccount(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    

    roles = models.ManyToManyField(
        Role, 
        through='AccountRole', 
        related_name='users'
    )

    class Meta:
        db_table = 'USER_ACCOUNT'

    def __str__(self):
        return self.username


class Venue(models.Model):
    venue_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue_name = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'VENUE'
        constraints = [
            models.CheckConstraint(check=Q(capacity__gt=0), name='capacity_check')
        ]

    def __str__(self):
        return f"{self.venue_name} ({self.city})"


class Artist(models.Model):
    artist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist_name = models.CharField(max_length=100, null=False, blank=False)
    genre = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'ARTIST'

    def __str__(self):
        return self.artist_name


class Promotion(models.Model):
    DISCOUNT_TYPES = [
        ('NOMINAL', 'Nominal'),
        ('PERCENTAGE', 'Percentage'),
    ]

    promotion_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    promo_code = models.CharField(max_length=50, unique=True, null=False, blank=False)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, null=False, blank=False)
    discount_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    usage_limit = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)

    class Meta:
        db_table = 'PROMOTION'
        constraints = [
            models.CheckConstraint(check=Q(discount_type__in=['NOMINAL', 'PERCENTAGE']), name='discount_type_check'),
            models.CheckConstraint(check=Q(discount_value__gt=0), name='discount_value_check'),
            models.CheckConstraint(check=Q(usage_limit__gt=0), name='usage_limit_check'),
        ]

    def __str__(self):
        return self.promo_code




class AccountRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = 'ACCOUNT_ROLE'
        unique_together = (('role', 'user'),)

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"




class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, db_column='user_id', related_name='customer')

    class Meta:
        db_table = 'CUSTOMER'

    def __str__(self):
        return self.full_name


class Organizer(models.Model):
    organizer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, db_column='user_id', related_name='organizer')

    class Meta:
        db_table = 'ORGANIZER'

    def __str__(self):
        return self.organizer_name


class Seat(models.Model):
    seat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.CharField(max_length=50, null=False, blank=False)
    seat_number = models.CharField(max_length=10, null=False, blank=False)
    row_number = models.CharField(max_length=10, null=False, blank=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, db_column='venue_id', related_name='seats')

    class Meta:
        db_table = 'SEAT'

    def __str__(self):
        return f"Sec {self.section}, Row {self.row_number}-{self.seat_number}"




class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_datetime = models.DateTimeField(null=False, blank=False)
    event_title = models.CharField(max_length=200, null=False, blank=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, db_column='venue_id', related_name='events')
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, db_column='organizer_id', related_name='events')
    

    artists = models.ManyToManyField(Artist, through='EventArtist', related_name='events')

    class Meta:
        db_table = 'EVENT'

    def __str__(self):
        return self.event_title


class EventArtist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='event_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')
    role = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'EVENT_ARTIST'
        unique_together = (('event', 'artist'),)

    def __str__(self):
        return f"{self.artist.artist_name} ({self.role}) @ {self.event.event_title}"


class TicketCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=50, null=False, blank=False)
    quota = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], null=False, blank=False)
    tevent = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='tevent_id', related_name='ticket_categories')

    class Meta:
        db_table = 'TICKET_CATEGORY'
        constraints = [
            models.CheckConstraint(check=Q(quota__gt=0), name='quota_check'),
            models.CheckConstraint(check=Q(price__gte=0), name='price_check'),
        ]

    def __str__(self):
        return f"{self.category_name} - {self.tevent.event_title}"


class TicketOrder(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateTimeField(null=False, blank=False)
    payment_status = models.CharField(max_length=20, null=False, blank=False)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id', related_name='orders')
    

    promotions = models.ManyToManyField(Promotion, through='OrderPromotion', related_name='orders')

    class Meta:
        db_table = 'TICKET_ORDER'
        constraints = [
            models.CheckConstraint(check=Q(total_amount__gte=0), name='total_amount_check'),
        ]

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.full_name}"


class Ticket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_code = models.CharField(max_length=100, unique=True, null=False, blank=False)
    tcategory = models.ForeignKey(TicketCategory, on_delete=models.CASCADE, db_column='tcategory_id', related_name='tickets')
    torder = models.ForeignKey(TicketOrder, on_delete=models.CASCADE, db_column='torder_id', related_name='tickets')
    
    seats = models.ManyToManyField(
        Seat, 
        db_table='HAS_RELATIONSHIP',
        related_name='tickets'
    )

    class Meta:
        db_table = 'TICKET'

    def __str__(self):
        return self.ticket_code


class OrderPromotion(models.Model):
    order_promotion_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, db_column='promotion_id')
    order = models.ForeignKey(TicketOrder, on_delete=models.CASCADE, db_column='order_id')

    class Meta:
        db_table = 'ORDER_PROMOTION'
        unique_together = (('promotion', 'order'),)

    def __str__(self):
        return f"Promo {self.promotion.promo_code} on Order {self.order.order_id}"