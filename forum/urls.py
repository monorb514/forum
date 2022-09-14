from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("search/", views.search_result, name="search_result"),
    path("detail/<slug>/", views.detail, name="detail_post"),
    path("posts/<slug>/", views.posts, name="posts_list"),
    path("create/post", views.CreatePostView.as_view(), name="create_post"),
    path("latest-posts", views.latest_posts, name="latest_posts"),

]

