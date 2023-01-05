from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, PostFilterForm, RegisterForm, EditPostForm
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # check user input in RegisterForm is valid or not
        if form.is_valid():
            user = form.save()
            return redirect("/login")

    # if method is GET then run the following code
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("login")


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    post_count_by_author = Post.objects.values("author__username").annotate(
        post_count=Count("id")
    )

    category_count_by_post = Category.objects.values("name").annotate(
        post_count=Count("post")
    )

    form = PostFilterForm(request.POST or None)
    start_date = end_date = None
    if request.method == "POST":
        # form = PostFilterForm(request.POST)
        if form.is_valid():
            # get data from the form
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            category = request.POST.getlist("category")
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            filters = Q()

            if title:
                filters &= Q(title__icontains=title)

            if author:
                filters &= Q(author__username=author)

            if category:
                filters &= Q(category__in=category)

            if start_date and end_date:
                filters &= Q(published_date__gte=start_date) or Q(
                    published_date__lte=end_date
                )

            posts = Post.objects.filter(filters)
        else:
            print(form.errors)
    # else:
    #     form = PostFilterForm()

    return render(
        request,
        "blog/post_list.html",
        {
            "form": form,
            "posts": posts,
            "post_count_by_author": post_count_by_author,
            "category_count_by_post": category_count_by_post,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "form": form},
    )


@login_required(login_url="/login")
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=pk)

    return redirect("blog:post_detail", pk=pk)


@login_required(login_url="/login")
def post_create(request):
    KATA_KOTOR = ["anjing", "goblok", "kampret", "asw", "jancok"]

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # body_text = request.POST["text"]
            # if KATA_KOTOR in body_text:
            #     censored_text = body_text.replace(KATA_KOTOR, "***")
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})


@login_required(login_url="/login")
def post_edit(request, pk):
    # get post data (object based on id)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # put post object into form
        form = EditPostForm(request.POST)
        if form.is_valid():
            form.save(post)
            return redirect("blog:post_detail", pk=post.pk)
    else:
        print("post :", post)
        # print("post category:", post.categories)
        form = EditPostForm(
            initial={
                "title": post.title,
                "text": post.text,
                "category": post.category.all(),
            }
        )

    return render(request, "blog/post_edit.html", {"form": form})


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


@login_required(login_url="/login")
@permission_required("blog.change_comment", login_url="/login", raise_exception=True)
def comment_edit(request, comment_id):
    """ """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            if request.user == comment.author or request.user.is_superuser:
                comment.save()
                return redirect("blog:post_detail", pk=comment.post.id)
            else:
                return redirect("blog:post_list")
    else:
        form = CommentForm(initial={"text": comment.text})

    return render(request, "blog/comment_edit.html", {"form": form, "comment": comment})


@login_required(login_url="/login")
@permission_required("blog.delete_comment", login_url="/login", raise_exception=True)
def comment_delete(request, comment_id):
    """TODO"""
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=comment.post.id)

    return HttpResponse(status=405)


# Create your views here.
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
#         "published_date"
#     )
#     start_date = end_date = None
#     if request.method == "POST":
#         form = PostFilterForm(request.POST)
#         if form.is_valid():
#             # get data from the form
#             title = form.cleaned_data["title"]
#             author = form.cleaned_data["author"]
#             category = form.cleaned_data["category"]
#             start_date = form.cleaned_data["start_date"]
#             end_date = form.cleaned_data["end_date"]

#             filter = Q()

#             if title:
#                 posts = posts.filter(title__icontains=title)

#             if author:
#                 posts = posts.filter(author__username=author)

#             if category:
#                 posts = posts.filter(category__in=category)

#             if start_date and end_date:
#                 start_date = form.cleaned_data["start_date"]
#                 end_date = form.cleaned_data["end_date"]
#                 posts = posts.filter(published_date__range=(start_date, end_date))
#     else:
#         form = PostFilterForm()

#     return render(request, "blog/post_list.html", {"form": form, "posts": posts})


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


# @login_required(login_url="/login")
# def post_edit(request, pk):
#     # get post data (object based on id)
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         # put post object into form
#         form = EditPostForm(request.POST, instance=post)
#         if form.is_valid():
#             user = User.objects.get(id=request.user.id)
#             # title = form.cleaned_data['title']
#             # text = form.cleaned_data['text']
#             # category = form.cleaned_data['category']
#             form.save(author=user)
#             # post = form.save(commit=False)
#             # post.author = request.user
#             # post.published_date = timezone.now()
#             # post.save()
#             # form.save_m2m()
#             return redirect("blog:post_detail", pk=post.pk)
#     else:
#         form = EditPostForm(instance=post)

#     return render(request, "blog/post_create.html", {"form": form})
