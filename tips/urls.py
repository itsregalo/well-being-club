from django.urls import path
from .views import *

app_name='blog'

urlpatterns = [
    path('', BlogListView, name='blog-list'),
    path('detail/<slug>/<int:pk>/', BlogDetailView, name='blog-detail'),
    path('new/create/', BlogCreateView, name='blog-create'),
    path('detail/<slug>/<int:id>/update/', BlogUpdateView, name='blog-update'),
    path('detail/<slug>/<int:id>/delete/', BlogDeleteView, name='blog-delete'),
    path('search/', searchBlog, name='search'),
    path('comment/<int:pk>/delete/', CommentDeleteView, name='comment-delete'),
    path('category-list/<slug:slug>/<int:pk>/', BlogCategoryList, name='category-list'),
    path('tags/<slug:slug>/<int:pk>/', BlogTagList, name='tag-list'),
    path('unauthenticated-comments-redirect/<slug>/<int:pk>/', 
                            UnauthenticatedCommentsRedirect, name='unauth-comments'),
]