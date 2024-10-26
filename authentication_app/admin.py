from django.contrib import admin

from authentication_app.models import CustomUser

admin.site.register(CustomUser)
