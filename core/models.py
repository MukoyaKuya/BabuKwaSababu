from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    constituency = models.CharField(max_length=100, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Volunteer(models.Model):
    SKILL_CHOICES = [
        ('canvassing', 'Canvassing'),
        ('digital', 'Digital/Social Media'),
        ('events', 'Event Planning'),
        ('legal', 'Legal/Compliance'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    skill = models.CharField(max_length=50, choices=SKILL_CHOICES, default='other')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class PlatformIssue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    source = models.CharField(max_length=200)
    headline = models.CharField(max_length=500)
    link = models.URLField(blank=True)
    date = models.DateField()
    excerpt = models.TextField(blank=True, help_text="A short snippet from the article.")
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.source}: {self.headline}"

class Endorsement(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class CampaignSettings(models.Model):
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="The candidate's portrait for the hero section.")
    quote_video_url = models.URLField(blank=True, help_text="YouTube video URL to display next to the quote section (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)")

    class Meta:
        verbose_name = "Campaign Settings"
        verbose_name_plural = "Campaign Settings"

    def get_quote_video_embed_url(self):
        """Convert a YouTube URL to an embed URL."""
        url = self.quote_video_url
        if not url:
            return ''
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in url:
            return url
        return ''

class CampaignVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50, help_text="The ID from the YouTube URL (e.g., dQw4w9WgXcQ)")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}"
