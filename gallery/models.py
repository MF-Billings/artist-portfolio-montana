from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class Tag(models.Model):
    """
    Hierarchical tag system for organizing artwork.
    Tags can be nested up to 5 levels deep.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\-]+$',
                message='Tag names can only contain letters and hyphens',
                code='invalid_tag_name'
            )
        ],
        help_text='Only letters (a-z, A-Z) and hyphens (-) allowed'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text='Parent tag for hierarchical organization'
    )
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.get_full_path()

    def get_full_path(self):
        """Returns the full hierarchical path of the tag (e.g., 'watercolour-landscape-mountains')"""
        if self.parent:
            return f"{self.parent.get_full_path()}-{self.name}"
        return self.name

    def get_depth(self):
        """Calculate the depth of this tag in the hierarchy (0-indexed)"""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def clean(self):
        """Validate that tag hierarchy doesn't exceed 5 levels"""
        if self.parent:
            depth = self.get_depth()
            if depth >= 5:
                raise ValidationError(
                    f'Tag hierarchy cannot exceed 5 levels. This tag would be at level {depth + 1}.'
                )

    def save(self, *args, **kwargs):
        """Auto-generate slug from name and validate before saving"""
        if not self.slug:
            self.slug = self.name.lower()
        self.full_clean()
        super().save(*args, **kwargs)

    def get_all_children(self):
        """Recursively get all descendant tags"""
        children = list(self.children.all())
        for child in list(children):
            children.extend(child.get_all_children())
        return children


class Artwork(models.Model):
    """
    Represents a piece of artwork (painting, drawing, or photograph)
    """
    MEDIUM_CHOICES = [
        ('watercolour', 'Watercolour'),
        ('drawing', 'Drawing'),
        ('photography', 'Photography'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text='Optional description of the artwork')
    medium = models.CharField(
        max_length=20,
        choices=MEDIUM_CHOICES,
        default='watercolour',
        help_text='Type of artwork'
    )
    image = models.ImageField(
        upload_to='artworks/%Y/%m/',
        help_text='Upload the artwork image'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='artworks',
        help_text='Select tags to categorize this artwork'
    )
    year_created = models.IntegerField(
        null=True,
        blank=True,
        help_text='Year the artwork was created'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Display this artwork prominently on the homepage'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'

    def __str__(self):
        return self.title

    def get_tag_hierarchy(self):
        """Returns all tags as a hierarchical list"""
        return [tag.get_full_path() for tag in self.tags.all()]


class Biography(models.Model):
    """
    Artist biography and life information.
    Only one biography entry should exist.
    """
    artist_name = models.CharField(max_length=200, default='Artist Name')
    content = models.TextField(help_text='Artist biography and life story')
    profile_image = models.ImageField(
        upload_to='biography/',
        null=True,
        blank=True,
        help_text='Optional profile photo of the artist'
    )
    birth_year = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Biography'
        verbose_name_plural = 'Biography'

    def __str__(self):
        return f"Biography of {self.artist_name}"

    def save(self, *args, **kwargs):
        """Ensure only one biography entry exists"""
        if not self.pk and Biography.objects.exists():
            raise ValidationError('Only one biography entry is allowed. Please edit the existing one.')
        super().save(*args, **kwargs)
