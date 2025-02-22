from django.contrib import admin
from .models import Car

from .models import Cart,CartItem,Order,OrderItem,Address,Location,Profile,Feedback



admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)


# Register your models here.
admin.site.register(Car)
admin.site.register(Location)
admin.site.register(Profile)
admin.site.register(Feedback)