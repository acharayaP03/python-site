
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import CommentForm
# Create your views here.


class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    

# def starting_page(request):
#     """ 
#     Get all post from db ordered by date and only get the last 3 
#     note "-date" will order by dsc
#     """
#     # sorted_posts = sorted(all_posts, key=get_date)
#     # latest_posts = sorted_posts[-3:]
#     latest_posts = Post.objects.all().order_by("-date")[:3]

#     return render(request, 'blog/index.html', {
#         "posts": latest_posts
#     })

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, 'blog/all-posts.html', {
#         "all_posts": all_posts
#     })

# def post_details(request, slug):
#     """ 
#     finding related post with slug field.  
#     """

#     identified_post = get_object_or_404(Post, slug=slug)

#     return render(request, 'blog/post-detail.html', {
#         "post": identified_post,Model
#         "post_tags": identified_post.tags.all()
#     })

class AllPostview(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    ordering = ["-date"]
    context_object_name = 'all_posts'

class SinglePostView(DetailView):
    model = Post
    template_name = "blog/post-detail.html"

    """
    Inorder to access tags, we need to override a function which will then allow us to access tags from post model 
    """

    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        context["comment_form"] = CommentForm
        return context

