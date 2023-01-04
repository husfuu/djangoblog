from blog import views
from django.urls import path

app_name = "blog"

urlpatterns = [
    path("sign-up/", views.sign_up, name="sign_up"),
    path("log-out/", views.log_out, name="log_out"),
    path("", views.post_list, name="post_list"),
    path("post/new", views.post_create, name="post_create"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path(
        "post/category/<int:category_id>",
        views.post_list_by_category,
        name="post_category",
    ),
    path("post/comment/<int:comment_id>/edit", views.comment_edit, name="comment_edit"),
    path(
        "post/comment/<int:comment_id>/delete",
        views.comment_delete,
        name="comment_delete",
    ),
    path("post/comment/<int:pk>/create", views.post_comment, name="post_comment"),
]
