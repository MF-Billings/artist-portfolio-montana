# Implementation Plan - Artist Portfolio MVP

The goal is to build a Django-based portfolio website for an artist (Watercolour & Photography). The project emphasizes TDD, modularity, and a simple but effective design (Pico.css).

## Decisions Confirmed

> [!NOTE]
> **Data Structure**:
> *   **Tags**: Primary organizational structure. Galleries are logical views of Tags.
> *   **Search**: Searches both `Artwork.title` AND `Tag.name` (substring match).
>
> **Hosting & Storage**:
> *   **Strategy**: "Local Production" with Docker Compose + Nginx.
> *   **Storage**: Local persistent volumes for images.
> *   **Future**: Ready for PaaS (Render/Fly.io) + S3 (Cloudinary/AWS) migration in Phase 2.
>
> **Admin**: Customized Django Admin for MVP.

## Guiding Principles

### Development Philosophy
1.  **Test-Driven Development (TDD)**: No production code is written without a failing test.
2.  **Validation**: Every code change must be validated by running the relevant unit tests immediately.
3.  **Simplicity (YAGNI)**: Do not build features you "might" need. Stick to the requirements (e.g., Tags, not Complex Galleries).
4.  **Continuous Validation**: The entire test suite must pass before any commit.

### Testing Guidelines
1.  **Unit Tests**: Should be fast, isolated, and cover individual functions/models.
2.  **Integration Tests**: Test how modules work together (e.g., Views using Models and Templates).
3.  **End-to-End (E2E) Tests**: Simulate real user behavior (Playwright).
4.  **Independence**: Each test category (Unit, Integration, E2E) must be executable independently.
5.  **Coverage**: New features must strive for >80% code coverage.


## Proposed Changes

### 1. Environment & Project Setup
*   **Initialize Django Project**: Set up `config` directory as the project root.
*   **Docker Setup**: Create `Dockerfile` and `docker-compose.yml`.
*   **Dependencies**: Add `django-imagekit` (thumbnails), `django-storages` (S3), `boto3`, `whitenoise` (static files).
*   **SEO Setup**: Install `django-robots`.
*   **Settings**: Configure `STATIC_ROOT` with WhiteNoise. Configure `MEDIA_ROOT`.

### 2. Core App (`apps/core`)
#### `apps/core/`
*   `views.py`: 
    *   Home page (Featured works).
    *   About page (Bio).
    *   Contact page (Simple form, directs to Artist email).
    *   `sitemap.xml` and `robots.txt` configuration.
*   `tests/`: Tests for static pages and sitemap availability.

### 3. Portfolio App (`apps/portfolio`)
#### `apps/portfolio/`
*   `models.py`:
    *   `Tag` (treebeard).
    *   `Artwork`:
        *   Fields: `title`, `image` (Process with ImageKit), `description` (Rich text?), `medium`, `dimensions`, `year_created`, `is_featured`, `alt_text` (SEO), **`price`** (DecimalField).
        *   Relations: ManyToMany to Tag.
*   `views.py`:
    *   `GalleryListView`: Filterable by Tag and Search Query (`Q(title) | Q(tag)`).
    *   `ArtworkDetailView`: Includes semantic SEO metadata (Schema.org 'VisualArtwork').
*   `admin.py`: 
    *   Customized Dashboard.
    *   `ImageAdmin` with thumbnail previews.
*   `tests/`: TDD for new fields and Image assertions.

### 4. Frontend & Styling
#### [NEW] `static/scss/style.scss`
*   Import Pico.css.
*   Apply custom theme vars (colors, fonts).

#### [NEW] `templates/`
*   `base.html`: Main layout (Nav, Footer).
*   `home.html`, `artwork_list.html`, `artwork_detail.html`: core templates.

### 5. SEO Strategy (Detailed)
*   **Meta Tags**: Use `django-meta` or custom templates to inject `OpenGraph` and `Twitter Card` tags on all pages.
*   **Structured Data**: JSON-LD scripts for `WebSite` (Home), `Person` (About), and `VisualArtwork` (Detail).
*   **Sitemap**: Auto-generated via `django.contrib.sitemaps`.
*   **Robots**: `robots.txt` disallowing admin.
*   **Performance**: Responsive images with `srcset` and `lazy` loading.

## Verification Plan

### Automated Testing Strategy
*   **Principle**: Tests are separated by type and speed.
*   **Command**: `pytest` (runs Unit & Integration), `playwright` (runs E2E).

#### 1. Unit & Integration Tests (Pytest)
*   **Guideline**: All new models and logic must have unit tests.
*   **Guideline**: All views must have integration tests checking status codes and context.
*   **Coverage Target**: **>= 80%**
*   **Examples**:
    *   *Models*: Test `Tag` nesting depth and `Artwork.price` formatting.
    *   *Views*: Test `GalleryListView` filters by Tag and Search Query.
    *   *SEO*: Assert JSON-LD presence in `ArtworkDetailView`.

#### 2. End-to-End Tests (Playwright)
*   **Guideline**: Critical user flows must be verified by E2E tests to ensure the system works as a whole.
*   **Guideline**: E2E tests should be resilient to minor UI changes (semantic selection).
*   **Scenarios**:
    *   **Guest Flow**: Home -> Filter -> Details -> Contact.
    *   **Mobile Flow**: Responsive menu validation.

### Manual Verification
*   **Principle**: Manual testing is reserved for "Look and Feel" and Admin workflows that are hard to automate cheaply.
*   **Scope**:
    *   **Admin**: Visual check of Thumbnail generation.
    *   **Frontend**: Lighthouse Audits (SEO/Accessibility > 90).

> [!NOTE]
> **Phase 2 (Out of Scope for MVP)**:
> *   Blog System (CRUD)
> *   Advanced Role-based permissions (beyond Admin)
> *   Cloud Storage migration (S3)
