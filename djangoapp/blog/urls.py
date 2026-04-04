# URL patterns for the blog app.
# Each line connects a URL pattern to a view that handles it.

from blog.views import (
    PostListView,
    PostDetailView,
    PageDetailView,
    CreatedByListView,
    CategoryListView,
    TagListView,
    SearchListView
)
from django.urls import path

app_name = 'blog'

urlpatterns = [
    # Homepage - shows all published posts
    path('', PostListView.as_view(), name='index'),

    # Single post page e.g. /post/maputo-city/
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),

    # Static pages e.g. /page/about-me/
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),

    # All posts by one author e.g. /created_by/1/
    path('created_by/<int:author_pk>/',
         CreatedByListView.as_view(), name='created_by'),

    # All posts in a category e.g. /category/beach/
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),

    # All posts with a tag e.g. /tag/city/
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),

    # Search results e.g. /search/?search=maputo
    path('search/', SearchListView.as_view(), name='search'),
]
