
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def starting_page(request):
	return render(request, 'blog/index.html')

def posts(request):
	return HttpResponse('hello from the blog page')

def post_details(request):
	pass