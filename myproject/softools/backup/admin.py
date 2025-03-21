from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, User, Alphabet, Word

# Register your models here.
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'type', 'description']
    ordering = ['id_alphabet']  # Default ordering A-Z
    search_fields = ['word', 'type']
    list_filter = ['type', 'id_alphabet']


admin.site.register(User, UserAdmin)
admin.site.register(Service)
admin.site.register(Alphabet)
admin.site.register(Word, WordAdmin)
