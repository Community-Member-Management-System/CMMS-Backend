from django.contrib import admin
from .models import Community, Invitation, Membership

# Register your models here.
admin.site.register(Community)
admin.site.register(Invitation)
admin.site.register(Membership)
