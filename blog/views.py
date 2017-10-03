from django.shortcuts import render,get_object_or_404,render_to_response
from comments.forms import CommentForm
from django.http import HttpResponse
from .models import Post,Category
import markdown

def index(request):
	post_list = Post.objects.all()
	return render(request,'blog/index.html',context = {'post_list': post_list})

def detail(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.body = markdown.markdown(post.body,
								  extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
								  ])

	form = CommentForm()
	comment_list = post.comment_set.all()

	context = {
				'post' : post,
				'form' : form,
				'comment_list' :comment_list
				}
	return render(request,'blog/detail.html',context= context)


def archives(request,year,month):
	post_list = Post.objects.filter(create_time__year = year,
									create_time__month = month
									)
	return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
	cate = get_object_or_404(Category,pk = pk)
	post_list = Post.objects.filter(category = cate)
	return render(request,'blog/index.html', context = {'post_list' : post_list})

def page_not_found(request):
    return render_to_response('404.html')


def page_error(request):
    return render_to_response('500.html')