from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post, Profile, Section, Comment, Replie
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreatePostForm
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


User = get_user_model()


def index(request):
    forums = Section.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("created_at")
    except:
        last_post = []

    context = {
        "forums": forums,
        "num_posts": num_posts,
        "num_users": num_users,
        "num_categories": num_categories,
        "last_post": last_post,
        "title": "FORUM"
    }
    return render(request, "forums.html", context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    author = None
    if request.user.is_authenticated:
        author = Profile.objects.get(user=request.user)

    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        comment_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=comment_id)
        new_reply, created = Replie.objects.get_or_create(user=author, reply_content=reply)
        comment_obj.replies.add(new_reply.id)

    context = {
        "post": post,
        "title": "FORUM: " + post.title,
    }

    return render(request, "detail.html", context)


def latest_posts(request):
    posts = Post.objects.all().filter()[:10]
    context = {
        "posts":posts,
        "title": "FORUM: Latest 10 Posts"
    }
    return render(request, "latest_posts.html", context)


def posts(request, slug):
    category = get_object_or_404(Section, slug=slug)
    posts = Post.objects.filter(sections=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts":posts,
        "forum": category,
        "title": "OZONE: Posts"
    }

    return render(request, "posts.html", context)


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    template_name = 'create_post.html'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


def search_result(request):
    return render(request, "search.html")




