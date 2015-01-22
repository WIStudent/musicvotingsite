from django.contrib import admin
from musicvoting.models import Artist, Album, User, Track
# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(User)
admin.site.register(Track)
