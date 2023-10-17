from django.contrib import admin
from .models import AuthToken, User, OtpToken

# Register your models here.

admin.site.register(User)
admin.site.register(AuthToken)
admin.site.register(OtpToken)