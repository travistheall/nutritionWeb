from django.contrib import admin
from .models import CustomUser, UserWeights


admin.site.register(CustomUser)
admin.site.register(UserWeights)
