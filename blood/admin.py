from django.contrib import admin

# Register your models here.
from .models import Stock,BloodRequest

admin.site.register(Stock)
admin.site.register(BloodRequest)

