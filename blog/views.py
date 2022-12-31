from .models import Post, Category
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )

    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})


def post_edit(request, pk):
    # get post data (object based on id)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # put post object into form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_create.html", {"form": form})


def post_list_by_category(request, category_id):
    """Display a list of posts in a given category id

    Args:
        request (HttpRequest)   : The incoming HTTP request
        category_id (int)       : category id that got from client

    Returns:
        HttpResponse    : The HTTP response to be sent to the client
    """
    posts = Post.objects.filter(category__id=category_id)

    return render(request, "blog/post_list.html", {"posts": posts})
