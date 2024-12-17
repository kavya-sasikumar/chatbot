# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ChatMessage)
admin.site.register(ChatSession)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(Vendor)