from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Tag, Artwork, Biography

# ==============================================================================
# UNIT TESTS (Logic and Data Integrity)
# ==============================================================================

class TagModelTest(TestCase):
    """Tests for the Tag model logic and validation."""

    def test_tag_full_path_basic(self):
        """Verify that the tag full path is correctly generated for a single tag."""
        tag = Tag.objects.create(name="landscape")
        self.assertEqual(tag.get_full_path(), "landscape")

    def test_tag_full_path_hierarchical(self):
        """Verify that the tag full path includes parent names."""
        parent = Tag.objects.create(name="medium")
        child = Tag.objects.create(name="watercolour", parent=parent)
        grandchild = Tag.objects.create(name="winsor-newton", parent=child)
        self.assertEqual(grandchild.get_full_path(), "medium-watercolour-winsor-newton")

    def test_tag_slug_auto_generation(self):
        """Verify that slugs are automatically created from names if not provided."""
        tag = Tag.objects.create(name="Photography")
        self.assertEqual(tag.slug, "photography")

    def test_tag_hierarchy_depth_limit(self):
        """Verify that tag hierarchy cannot exceed 5 levels."""
        # Create 5 levels
        t1 = Tag.objects.create(name="level-one")
        t2 = Tag.objects.create(name="level-two", parent=t1)
        t3 = Tag.objects.create(name="level-three", parent=t2)
        t4 = Tag.objects.create(name="level-four", parent=t3)
        t5 = Tag.objects.create(name="level-five", parent=t4)
        
        # Level 6 should fail
        t6 = Tag(name="level-six", parent=t5)
        with self.assertRaises(ValidationError):
            t6.save()

    # --- STUBS FOR YOU TO COMPLETE ---
    
    def test_tag_invalid_name_regex(self):
        """TODO: Verify that tags with special characters (like 'tag!') raise a ValidationError."""
        pass

    def test_tag_get_all_children(self):
        """TODO: Verify that get_all_children returns all descendants recursively."""
        pass


class BiographyModelTest(TestCase):
    """Tests for the Biography singleton behavior."""

    def test_biography_singleton_enforcement(self):
        """Verify that only one biography can be created."""
        Biography.objects.create(artist_name="Alice", content="Hello")
        
        second_bio = Biography(artist_name="Bob", content="World")
        with self.assertRaises(ValidationError):
            second_bio.save()


# ==============================================================================
# INTEGRATION TESTS (Views and Routing)
# ==============================================================================

class GalleryViewsTest(TestCase):
    """Tests for the views and how they interact with models."""

    def setUp(self):
        # Create a dummy image for Artwork models
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x03\x02\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )
        self.tag_nature = Tag.objects.create(name="nature")
        self.artwork = Artwork.objects.create(
            title="Autumn Landscape",
            medium="watercolour",
            image=self.image,
            is_featured=True
        )
        self.artwork.tags.add(self.tag_nature)

    def test_home_page_status_code(self):
        """Verify the home page loads successfully."""
        response = self.client.get(reverse('gallery:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Autumn Landscape")

    def test_artwork_detail_view_success(self):
        """Verify the artwork detail page loads for existing artwork."""
        url = reverse('gallery:artwork_detail', args=[self.artwork.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['artwork'], self.artwork)

    def test_artwork_detail_view_404(self):
        """Verify that a 404 is returned for non-existent artworks."""
        url = reverse('gallery:artwork_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # --- STUBS FOR YOU TO COMPLETE ---

    def test_gallery_filtering_by_medium(self):
        """TODO: Create artworks with different mediums and verify the 'medium' GET param works."""
        pass

    def test_gallery_search_query(self):
        """TODO: Verify that the 'search' GET param correctly filters artworks by title/description."""
        pass


# ==============================================================================
# ACCEPTANCE TESTS (End-to-End User Scenarios)
# ==============================================================================

class UserExperienceTest(TestCase):
    """Tests that simulate higher-level user flows."""

    def test_user_can_filter_by_tag_name(self):
        """
        Acceptance Criteria:
        A user visits the gallery, searches for a tag, and sees relevant results.
        """
        # 1. Setup
        tag_photo = Tag.objects.create(name="photography")
        tag_painting = Tag.objects.create(name="painting")
        
        image = SimpleUploadedFile(name='a.jpg', content=b'...', content_type='image/jpeg')
        art1 = Artwork.objects.create(title="A Photo", image=image)
        art1.tags.add(tag_photo)
        
        art2 = Artwork.objects.create(title="A Painting", image=image)
        art2.tags.add(tag_painting)

        # 2. Action: User visits gallery and searches for 'photo'
        response = self.client.get(reverse('gallery:gallery'), {'tag_search': 'photo'})

        # 3. Verification
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Photo")
        self.assertNotContains(response, "A Painting")

    # --- STUBS FOR YOU TO COMPLETE ---

    def test_user_flow_from_home_to_detail(self):
        """
        TODO: 
        1. Visit homepage
        2. Find the link to an artwork detail page
        3. Click/Follow that link
        4. Verify you are on the detail page with correct content
        """
        pass
