from django.shortcuts import render
from .models import BlogPost

# Create your views here.


def blog_index(request):
	blog_posts = BlogPost.objects.all().order_by('-date')
	return render(request, 'blog/blog_index.html', {'blog_posts': blog_posts})

def blog_detail(request, slug):
	blog_post = BlogPost.objects.get(slug=slug)
	return render(request, 'blog/blog_detail.html', {'blog_post': blog_post})
