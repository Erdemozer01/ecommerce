from django.contrib import admin
from .models import SiteSettingModels, SiteSettingMeta, SiteSettingsAboutModels, SiteSettingsTeamsModels, \
    SiteSettingsFqModels, SiteSettingsSocialMedialModels, SiteSettingsLicenseModels
from .forms import SiteSettingModelsForm

# Register your models here.

class SiteSettingsLicenseModelsAdmin(admin.TabularInline):
    model = SiteSettingsLicenseModels
    extra = 1
    classes = ['collapse']


class SiteSettingsSocialMedialModelsAdmin(admin.TabularInline):
    model = SiteSettingsSocialMedialModels
    extra = 1
    classes = ['collapse']


class SiteSettingsFqModelsAdmin(admin.TabularInline):
    model = SiteSettingsFqModels
    extra = 1
    classes = ['collapse']


class SiteSettingsTeamsModelsAdmin(admin.TabularInline):
    model = SiteSettingsTeamsModels
    extra = 1
    classes = ['collapse']


class SiteSettingsAboutModelsAdmin(admin.TabularInline):
    model = SiteSettingsAboutModels
    extra = 1
    classes = ['collapse']


class SiteSettingMetaNameModelsAdmin(admin.TabularInline):
    model = SiteSettingMeta
    extra = 1
    classes = ['collapse']


@admin.register(SiteSettingModels)
class SiteSettingAdmin(admin.ModelAdmin):
    inlines = [SiteSettingMetaNameModelsAdmin, SiteSettingsAboutModelsAdmin, SiteSettingsTeamsModelsAdmin,
               SiteSettingsFqModelsAdmin, SiteSettingsSocialMedialModelsAdmin, SiteSettingsLicenseModelsAdmin]
    list_display = ['theme', 'name', 'email', 'url', 'is_active', 'created']
    search_fields = ['name']
    list_editable = ['is_active']