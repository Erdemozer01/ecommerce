from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'created']
    search_fields = ['user__username', 'user__first_name', 'last_name', 'email']
    search_help_text = "Kullanıcı adı, ad soyad, email adresine göre ara"
    list_filter = ['created']
    ordering = ['-created']
    list_per_page = 25
