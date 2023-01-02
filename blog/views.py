from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )

    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "form": form},
    )


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     comments = post.comments.all()
#     form = CommentForm()
#     return render(
#         request,
#         "blog/post_detail.html",
#         {"post": post, "comments": comments, "form": form},
#     )


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


def comment_edit(request, comment_id):
    """ """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            if request.user == comment.author:
                comment.save()
                return redirect("blog:post_detail", pk=comment.post.id)
            else:
                return redirect("blog:post_list")
    else:
        form = CommentForm(initial={"text": comment.text})

    return render(request, "blog/comment_edit.html", {"form": form, "comment": comment})


def comment_delete(request, comment_id):
    """TODO"""
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=comment.post.id)

    return HttpResponse(status=405)


# @require_POST
# def post_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)

#     comment = None
#     form = CommentForm(data=request.POST)

#     if form.is_valid():
#         # create a Comment object without saving it to the database
#         comment = form.save(commit=False)
#         # assign post to the comment
#         comment.post = post
#         comment.author = request.user
#         # save the comment to the db
#         comment.save()

#     return render(
#         request, "blog/comment.html", {"form": form, "post": post, "comment": comment}
#     )
