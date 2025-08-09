from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'get_related_info']

    def get_related_info(self, obj):
        # For ManyToManyField:
        return ", ".join([related_obj.name for related_obj in obj.my_many_to_many_field.all()])


    get_related_info.short_description = 'Questionnaires'

admin.site.register(Profile, ProfileAdmin)