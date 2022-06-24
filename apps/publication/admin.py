from django.contrib import admin

from .models import Publication, PublicationsImage


class PublicationsImageAdmin(admin.TabularInline):
    model = PublicationsImage
    extra = 1


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    model = Publication
    list_display = ('author', 'title', 'slug', 'created_at', 'updated_at', 'views_count', 'category')
    prepopulated_fields = {'slug': ('title', )}
    inlines = [PublicationsImageAdmin]