from django.contrib import admin
from django.utils.html import format_html
from .models import Tag, Artwork, Biography


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for managing hierarchical tags"""
    list_display = ['name', 'parent', 'get_depth_display', 'slug', 'artwork_count']
    list_filter = ['parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Tag Information', {
            'fields': ('name', 'slug', 'parent')
        }),
    )

    def get_depth_display(self, obj):
        """Display the depth level of the tag"""
        depth = obj.get_depth()
        return f"Level {depth + 1}"
    get_depth_display.short_description = 'Hierarchy Level'

    def artwork_count(self, obj):
        """Show how many artworks use this tag"""
        count = obj.artworks.count()
        return count
    artwork_count.short_description = 'Artworks'


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    """Admin interface for managing artworks"""
    list_display = ['thumbnail', 'title', 'medium', 'year_created', 'is_featured', 'tag_list', 'created_at']
    list_filter = ['medium', 'is_featured', 'tags', 'year_created']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags']  # Nice UI for selecting multiple tags
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'medium', 'year_created')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Organization', {
            'fields': ('tags', 'is_featured')
        }),
    )

    def thumbnail(self, obj):
        """Display a small thumbnail in the list view"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    thumbnail.short_description = 'Preview'

    def tag_list(self, obj):
        """Display tags as a comma-separated list"""
        tags = obj.tags.all()
        if tags:
            return ', '.join([tag.name for tag in tags[:3]]) + ('...' if len(tags) > 3 else '')
        return '-'
    tag_list.short_description = 'Tags'


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    """Admin interface for managing artist biography"""
    list_display = ['artist_name', 'birth_year', 'updated_at']

    fieldsets = (
        ('Artist Information', {
            'fields': ('artist_name', 'birth_year', 'profile_image')
        }),
        ('Biography', {
            'fields': ('content',),
            'description': 'Write the artist\'s biography and life story'
        }),
    )

    def has_add_permission(self, request):
        """Only allow adding if no biography exists"""
        return not Biography.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the biography"""
        return False
