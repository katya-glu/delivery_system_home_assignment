from django.contrib import admin
from .models import *

admin.site.register(Courier)
admin.site.register(User)
admin.site.register(Timeslot)
admin.site.register(Address)
admin.site.register(Delivery)


