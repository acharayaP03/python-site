
from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def starting_page(request):
    """ 
    Get all post from db ordered by date and only get the last 3 
    note "-date" will order by dsc
    """
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-3:]
    latest_posts = Post.objects.all().order_by("-date")[:3]

    return render(request, 'blog/index.html', {
        "posts": latest_posts
    })

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, 'blog/all-posts.html', {
        "all_posts": all_posts
    })

def post_details(request, slug):
    """ 
    finding related post with slug field. 
    """

    identified_post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/post-detail.html', {
        "post": identified_post,
        "post_tags": identified_post.tags.all()
    })