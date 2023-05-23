from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(OutgoingDocs)
admin.site.register(User)
admin.site.register(Tracking)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Notifications)