from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Items)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(ActiveItems)
admin.site.register(InactiveItems)