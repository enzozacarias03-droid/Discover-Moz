# This file controls what actually gets shown on each page.
# I used Class Based Views (CBVs) instead of function views -
# it's more code upfront but much cleaner when views share similar logic.

from typing import Any

from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

# How many posts to show per page across the whole site
PER_PAGE = 9


class PostListView(ListView):
    # The base view for showing a list of posts.
    # All other list views below inherit from this one.
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',
        })
        return context


class CreatedByListView(PostListView):
    # Shows all posts written by a specific author
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']

        # Show full name if available, otherwise just show username
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        ctx.update({
            'page_title': user_full_name + ' posts - ',
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        # Filter to only posts by this specific author
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        # If the author doesn't exist, show a 404 page
        if user is None:
            raise Http404

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })
        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    # Shows all posts in a specific category
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (
            f'{self.object_list.first().category.name}'  # type: ignore
            ' - Category - '
        )
        ctx.update({
            'page_title': page_title,
        })
        return ctx


class TagListView(PostListView):
    # Shows all posts with a specific tag
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Get the tag name to use in the page title
        tag = self.object_list.first().tags.filter(  # type: ignore
            slug=self.kwargs.get('slug')
        ).first()

        ctx.update({
            'page_title': f'{tag.name} - Tags - ',
        })
        return ctx


class SearchListView(PostListView):
    # Handles the search functionality
    # Searches across titles, excerpts, content, categories and tags

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        # Grab the search term from the URL and clean up any extra spaces
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) |
            Q(category__name__icontains=search_value) |
            Q(tags__name__icontains=search_value)
        ).distinct()
        # Note: .distinct() is needed because a post with multiple
        # matching tags could show up more than once without it

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value
        })
        return ctx

    def get(self, request, *args, **kwargs):
        # Don't bother searching if the box was submitted empty
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    # Shows a single static page like "About Me" or "Purpose"
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        ctx.update({
            'page_title': f'{page.title} - Page - ',  # type: ignore
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        # Unpublished pages shouldn't be accessible by URL
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    # Shows a single blog post
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        ctx.update({
            'page_title': f'{post.title} - Post - ',  # type: ignore
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        # Unpublished posts shouldn't be accessible by URL
        return super().get_queryset().filter(is_published=True)
