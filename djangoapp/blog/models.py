# This file defines what the database looks like for the blog
# Each class here = one table in the database

from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse


class PostAttachment(AbstractAttachment):
    # Handles images uploaded inside post content through the editor
    # When a new image is uploaded, we resize it to keep file sizes reasonable
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        # Only resize if the file actually changed, not on every save
        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


class Tag(models.Model):
    # Tags are small labels you can attach to posts, like "Beach" or "City"
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=225)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        # Auto-create the slug from the name if it's not set yet
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    # Categories group posts together, like "Beaches" or "Cities"
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=225)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        # Auto-create the slug from the name if it's not set yet
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    # Static pages like "About Me" or "Purpose" - not blog posts
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    # Page won't show on the site unless this is checked in the admin
    is_published = models.BooleanField(
        default=False,
        help_text='This camp will need to be market'
        'for the page to be publicly exhibited.'
    )
    content = models.TextField()

    def get_absolute_url(self):
        # Send unpublished pages back to home instead of showing an error
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:page', args=(self.slug,))

    def save(self, *args, **kwargs):
        # Auto-create the slug from the title if it's not set yet
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class PostManager(models.Manager):
    # Custom manager so I can easily grab only published posts anywhere in the code
    def get_published(self):
        # Minus sign in front of pk means newest posts show first
        return self\
            .filter(is_published=True)\
            .order_by('-pk')


class Post(models.Model):
    # The main blog post - this is the most important model in the project
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    # Short description shown on the post card on the homepage
    # Write a real sentence here, not just the category name
    excerpt = models.CharField(max_length=150)

    # Post won't show on the site unless this is checked in the admin
    is_published = models.BooleanField(
        default=False,
        help_text=('This camp will need to be market'
                   'for the page to be publicly exhibited.'
                   ),
    )

    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')

    # Controls whether the cover image also appears at the top of the post
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='If market, it will exhibit the cover of the post.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_created_by.all
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_updated_by.all
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    # A post can have multiple tags
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Send unpublished posts back to home instead of showing an error
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        # Only resize the cover if a new image was uploaded
        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save
