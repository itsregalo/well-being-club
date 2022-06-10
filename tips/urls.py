from django.urls import path
from .views import *

app_name='tips'

urlpatterns = [
    path('', TipListView, name='tip-list'),
    path('detail/<slug>/<int:pk>/', TipDetailView, name='tip-detail'),
    path('new/create/', TipCreateView, name='tip-create'),
    path('detail/<slug>/<int:id>/update/', TipUpdateView, name='tip-update'),
    path('detail/<slug>/<int:id>/delete/', TipDeleteView, name='tip-delete'),
    path('search/', searchTip, name='search'),
    path('comment/<int:pk>/delete/', CommentDeleteView, name='comment-delete'),
    path('category-list/<slug:slug>/<int:pk>/', TipCategoryList, name='category-list'),
    path('tags/<slug:slug>/<int:pk>/', TipTagList, name='tag-list'),
    path('unauthenticated-comments-redirect/<slug>/<int:pk>/', 
                            UnauthenticatedCommentsRedirect, name='unauth-comments'),
]