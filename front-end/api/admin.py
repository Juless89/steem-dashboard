from django.contrib import admin
from .models import votes_count_minute, blocks

# Register your models here.
admin.site.register(votes_count_minute)
admin.site.register(blocks)