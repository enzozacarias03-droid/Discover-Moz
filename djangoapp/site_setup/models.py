# This file controls the global site settings - things like the site title,
# description, and which sections show up on the page.
# All of this is managed through the admin panel, no code changes needed.

from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image


class MenuLink(models.Model):
    # Each navigation link in the menu is stored here
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    # If true, the link opens in a new browser tab
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True,
        null=True, default=None
    )

    def __str__(self):
        return self.text


class SiteSetup(models.Model):
    # Main site configuration - only one of these should exist at a time.
    # Controls what's visible on the site without touching any code.
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    # These toggles control which sections appear on the site
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    # Favicon must be a PNG - the validator checks this automatically
    # It gets resized to 32x32px which is the standard favicon size
    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True, default='',
        validators=[validate_png],
    )

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        # Only resize if a new favicon was uploaded
        if favicon_changed:
            resize_image(self.favicon, 32)

    def __str__(self):
        return self.title
