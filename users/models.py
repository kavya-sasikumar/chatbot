# Create your models here.
from django.db import models
from decimal import Decimal
from PIL import Image
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    """ Product Categories to keep details of a Product's categories """
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    #For the admin view
    def __str__(self):
        return f'{self.title} Category'

class Product(models.Model):
    """ Product Class to keep details of a Product """
    title = models.CharField(max_length=255)
    description = models.TextField()
    color = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    #For the admin view
    def __str__(self):
        return f'{self.title} Product'
    
class Order(models.Model):
    """ Order Class to keep details of a Product Order """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=20)
    StatusType = models.TextChoices('StatusType', 'PENDING SHIPPED DELIVERED CANCELLED')
    status_type = models.CharField(choices=StatusType.choices, max_length=9, default='PENDING')
    order_date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
 
    #For the admin view
    def __str__(self):
        return f'{self.id} Order for {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
 
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.title}'

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ChatMessage {self.id} by {self.user.username}'

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'ChatSession {self.id} for {self.user.username}'

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Event {self.title}'

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_pics/')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Event Image for {self.event.title}'