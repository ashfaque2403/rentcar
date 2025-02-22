from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# models.py

from django.db import models
from django.contrib.auth.models import User

CAR_TYPE_CHOICES = [
    ('sedan', 'Sedan'),
    ('suv', 'SUV'),
    ('truck', 'Truck'),
    ('hatchback', 'Hatchback'),
    ('convertible', 'Convertible'),
]

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    car_name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    kilometers_drove = models.IntegerField()
    seats = models.PositiveIntegerField()
    car_image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.car_name} - {self.car_type} (${self.price})"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    days = models.PositiveIntegerField(default=1)  # Added days field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.car_name} in {self.cart.user.username}'s cart"
  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    location = models.CharField(max_length=100)
    proof = models.FileField(upload_to='proofs/', blank=True, null=True)  # New field

    def __str__(self):
        return self.user.username


# Signal to automatically create Profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save Profile when User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='address')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    shipping_method = models.CharField(max_length=50, default='Standard Delivery', null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

from django.core.validators import RegexValidator

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    days = models.PositiveIntegerField(default=1)  # Duration in days
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    aadhar_number = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{12}$', 'Enter a valid 12-digit Aadhar number')],
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity



class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User model
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"


