from django.contrib import admin
from .models import Profile, Requests, SavedSignals, Task


admin.site.register(Profile)
admin.site.register(Requests)
admin.site.register(SavedSignals)
admin.site.register(Task)
