I want to create a Flask-based portfolio website for an artist who specializes in
  watercolour painting and photography. I'd like to use an iterative, conversation-driven
  approach to build this.

  Please help me by conducting a structured discovery session with the following approach:

  1. **Start with constraints and priorities** - Ask about budget, timeline, technical
     skill level, and must-have vs. nice-to-have features to establish realistic scope

  2. **Explore the artist's needs** systematically:
     - Target audience and goals (selling work? attracting gallery interest? personal showcase?)
     - Visual identity (minimalist/bold, light/dark themes, inspiration sites)
     - Content structure (how many pieces to showcase, categories, filtering needs)
     - User experience (mobile-first? accessibility requirements? multi-language?)
     - Technical stack (Flask + what? database needs? frontend framework preferences?)
     - Hosting & deployment (local dev, cloud platform, domain/SSL requirements)
     - Performance & scale (expected traffic, image optimization strategy)
     - Security posture (authentication needs, form protection, rate limiting)
     - Content management (how will the artist update their portfolio?)

  3. **Challenge my assumptions** - If I'm over-engineering, under-planning, or missing
     important considerations, push back and explain why

  4. **Suggest best practices** I might not know about - especially around:
     - Image handling for art portfolios (formats, responsive images, loading strategies)
     - SEO for artist portfolios
     - Analytics and contact form functionality
     - Copyright/watermarking considerations
     - Progressive enhancement vs. JavaScript-heavy approaches

  Ask 3-5 focused questions at a time, building on my previous answers. After gathering
  enough context, propose an initial architecture and tech stack before we start coding.

# Additional Context

## Technical Skill Level
- I'm familiar with PHP and javascript but have only tinkered with PHP and have never used Flask before.  I'm definitely a begginer
- I'm comfortable with HTML and CSS, but complicated styling is a challenge for me.
- I'm familiar with command line, git, and feature branch development workflows.  I've used but never set up a deployment pipeline.

## Timeline and Launch Goals
I'm alright within launching several months from now, but would like an MVP within the next two months.  However, this is exploratory and there are no hard deadlines.

## Content Management
The artist has no technical capability so I would be managing everything myself.  The following admin pages would be useful but aren't necessary for phase 1:
- add or remove images
- categorize images based on tags.
  - examples of possible tags include painting, picture, watercolour, winter-project-2025, landscape.
- CRUD operations for blog posts
- ability to edit text displayed on the different pages
- role-based permission system
