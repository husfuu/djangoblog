from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    path('post/<int:pk>/edit', views.post_edit, name="post_edit")
]