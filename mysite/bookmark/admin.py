from django.contrib import admin
from bookmark.models import BookMark

# Register your models here.
@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'url')
    
# admin.site.register(BookMark, BookMarkAdmin)
