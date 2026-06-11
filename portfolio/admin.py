from django.contrib import admin

from .models import ContactInquiry, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "featured", "created_at")
    list_filter = ("status", "featured", "created_at")
    search_fields = ("title", "client", "short_description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "short_description", "description", "client")}),
        ("Medios", {"fields": ("image", "preview_video")}),
        ("Enlaces y tecnología", {"fields": ("technologies", "project_url", "repository_url")}),
        ("Publicación", {"fields": ("status", "featured", "created_at", "updated_at")}),
    )


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "service", "is_read", "created_at")
    list_filter = ("is_read", "service", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
