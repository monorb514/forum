from .models import Post


def search_function(request):
    search_context = {}
    posts = Post.objects.all()
    if "search" in request.GET:
        query = request.GET.get("q")
        search_box = request.GET.get("search-box")
        if search_box == "Descriptions":
            objects = posts.filter(post_content__icontains=query)
        else:
            objects = posts.filter(title__icontains=query)
        search_context = {
            "objects":objects,
            "query":query,
        }
    return search_context