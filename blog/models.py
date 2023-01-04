from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# # Define permission
# content_type = ContentType.objects.get(app_label="blog", model="comment")

# if not Permission.objects.filter(
#     codename="can_edit_comment", content_type=content_type
# ).exists():
#     Permission.objects.create(
#         codename="can_delete_comment",
#         name="Can delete the post comment",
#         content_type=content_type,
#     )

# if not Permission.objects.filter(
#     codename="can_delete_comment", content_type=content_type
# ).exists():
#     Permission.objects.create(
#         codename="can_delete_comment",
#         name="Can delete the post comment",
#         content_type=content_type,
#     )

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
