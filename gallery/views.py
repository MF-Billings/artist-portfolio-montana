from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Artwork, Tag, Biography


def home(request):
    """Homepage with featured artworks"""
    featured_artworks = Artwork.objects.filter(is_featured=True)[:6]
    recent_artworks = Artwork.objects.all()[:12]

    context = {
        'featured_artworks': featured_artworks,
        'recent_artworks': recent_artworks,
    }
    return render(request, 'gallery/home.html', context)


def gallery(request):
    """
    Gallery view with all artworks, filterable by tags, medium, and search query.
    Supports tag substring filtering.
    """
    artworks = Artwork.objects.all()

    # Get all tags for the filter sidebar
    all_tags = Tag.objects.all()

    # Filter by medium
    medium = request.GET.get('medium')
    if medium:
        artworks = artworks.filter(medium=medium)

    # Filter by tag (supports multiple tags)
    tag_ids = request.GET.getlist('tags')
    if tag_ids:
        for tag_id in tag_ids:
            artworks = artworks.filter(tags__id=tag_id)

    # Search by tag name (substring match)
    tag_search = request.GET.get('tag_search', '').strip()
    if tag_search:
        # Find all tags that match the substring
        matching_tags = Tag.objects.filter(name__icontains=tag_search)
        # Get artworks that have any of these tags
        artworks = artworks.filter(tags__in=matching_tags).distinct()

    # Text search in title and description
    search_query = request.GET.get('search', '').strip()
    if search_query:
        artworks = artworks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()

    # Remove duplicates and maintain order
    artworks = artworks.distinct()

    context = {
        'artworks': artworks,
        'all_tags': all_tags,
        'selected_medium': medium,
        'selected_tag_ids': [int(tid) for tid in tag_ids if tid],
        'tag_search': tag_search,
        'search_query': search_query,
        'medium_choices': Artwork.MEDIUM_CHOICES,
    }
    return render(request, 'gallery/gallery.html', context)


def artwork_detail(request, pk):
    """Individual artwork detail page"""
    artwork = get_object_or_404(Artwork, pk=pk)
    related_artworks = Artwork.objects.filter(
        tags__in=artwork.tags.all()
    ).exclude(pk=artwork.pk).distinct()[:4]

    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
    }
    return render(request, 'gallery/artwork_detail.html', context)


def biography(request):
    """Artist biography page"""
    try:
        bio = Biography.objects.first()
    except Biography.DoesNotExist:
        bio = None

    context = {
        'biography': bio,
    }
    return render(request, 'gallery/biography.html', context)


def tag_detail(request, slug):
    """
    View all artworks with a specific tag (and its children tags)
    """
    tag = get_object_or_404(Tag, slug=slug)

    # Get this tag and all its children
    child_tags = tag.get_all_children()
    all_related_tags = [tag] + child_tags

    # Get artworks with any of these tags
    artworks = Artwork.objects.filter(tags__in=all_related_tags).distinct()

    context = {
        'tag': tag,
        'artworks': artworks,
        'child_tags': child_tags,
    }
    return render(request, 'gallery/tag_detail.html', context)
