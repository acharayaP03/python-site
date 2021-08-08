
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.urls import reverse
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

# class SinglePostView(DetailView):
#     model = Post
#     template_name = "blog/post-detail.html"

#     """
#     Inorder to access tags, we need to override a function which will then allow us to access tags from post model 
#     """

#     def get_context_data(self, **kwargs):
#         context=  super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm
#         return context

""" 
Since the post-detail has a comment form, Modifying detailView since 
DetailView only handles a incomming get request and more custom login will be little bit tricky and cumbersome, 
hence why we will turn this into a View which then will receive post request. 

"""
class SinglePostView(View):
    template_name = "blog/post-detail.html"
    model = Post
    

    def get(slef, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            """ 
            inorder to make comment editable, we need to get a refrence of the model, 
            we can do this by enabling commit set to false on save method, which will halt comment to hit database
            and creates an instance of the the post.
            """
            comment = comment_form.save(commit=False)
            comment.post = post
            """ now call save method and redirect"""
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        """
        if comment form validation fails then re fetch the context from get,

        """
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        
        context = {}
        
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")