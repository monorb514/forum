from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from unidecode import unidecode
from django.template import defaultfilters

from django.shortcuts import reverse

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateField(auto_now_add=True)
    author = models.OneToOneField(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Section(models.Model):
    author = models.ForeignKey(User, related_name='sections_created', on_delete=models.RESTRICT)
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True, default='description')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.title))
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("posts_list", kwargs={
            'slug': self.slug
        })

    @property
    def num_posts(self):
        return Post.objects.filter(sections=self).count()

    @property
    def last_post(self):
        return Post.objects.filter(sections=self).latest("created_at")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    image = ResizedImageField(size=[50, 80], quality=100, upload_to='profile_images', default=None, null=True, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.user.username))
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()

    def get_url(self):
        return reverse("update_profile", kwargs={
            'slug': self.slug
        })


class Replie(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='replies', blank=True)
    reply_content = models.CharField(max_length=5000)
    image = models.ImageField(upload_to="images", default="", blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solution = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}, {self.updated_at}'


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Replie, blank=True)

    def __str__(self):
        return self.content[:100]


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=500)
    post_content = HTMLField()
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sections = models.ManyToManyField(Section)
    tags = TaggableManager()
    image = models.ImageField(upload_to="images", default="", blank=True)
    link = models.URLField(blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    visit_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    state = models.CharField(max_length=40, default="zero")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = defaultfilters.slugify(unidecode(self.title))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.user.username}, {self.updated_at}'

    def add_visit(self):
        if self.visit_count is not None:
            self.visit_count += 1
        else:
            self.visit_count = 0

    def get_url(self):
        return reverse("detail_post", kwargs={
            'slug': self.slug
        })

    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stats')
    days_visited = models.IntegerField(default=0)
    affections_given = models.IntegerField(default=0)
    affections_received = models.IntegerField(default=0)
    posts_answered = models.IntegerField(default=0)
    sections_created = models.IntegerField(default=0)

    def __str__(self):
        return f'Активность пользователя {self.user.full_name}'


