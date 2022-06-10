from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Blog, BlogComment, BlogTags, Category
from django.core.paginator import Paginator
from .forms import BlogForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from itertools import chain
from django.conf import settings
from taggit.models import Tag



# Create your views here.
def BlogListView(request, *args, **kwargs):
    blog = Blog.objects.all()
    categories = Category.objects.order_by('view_count')[:10]

    paginator = Paginator(blog, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #to do recent posts
    
    context = {
        'blogs':page_obj,
        'latest_blog':Blog.objects.order_by('-pub_date')[:5],
        'popular_blog':Blog.objects.all().order_by('view_count')[:3],
        'categories':categories,
    }
    return render(request, 'blog/blog_list.html', context)

def BlogDetailView(request, slug, *args, **kwargs):
    blog = get_object_or_404(Blog, slug=slug)
    blog_comments = blog.get_blog_comments()
    comment_form = CommentForm()
    related_posts = Blog.objects.filter(category=blog.category).order_by('-pub_date').exclude(slug=slug)[:5]
    blogs_by_author = Blog.objects.filter(uploaded_by=blog.uploaded_by).order_by('-pub_date').exclude(slug=slug)[:5]
    categories = Category.objects.all()[:10]

    if request.method == 'POST':
        next_url = reverse('blog:blog-detail', kwargs={'slug':slug, 'pk':blog.pk})
        login_url = reverse(settings.LOGIN_URL)

        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = blog
                new_comment.save()
                return JsonResponse({"comment":model_to_dict(new_comment)})
            messages.error(request,'Oops! please try again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request,'Oops! please login to comment')
        return redirect(login_url+"?next="+next_url)

    context = {
        'blog':blog,
        'blog_comments':blog_comments,
        'latest_blog':Blog.objects.order_by('-pub_date')[:5],
        'comment_form':comment_form,
        'related_posts':related_posts,
        'blogs_by_author':blogs_by_author,
        'categories':categories,
    }

    return render(request, 'blog/blog_detail.html', context)

@login_required
def BlogCreateView(request, *args, **kwargs):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.uploaded_by = request.user
            new_blog.save()
            messages.success(request, 'blog added successfully')
            return redirect('blog:blog-list')
        messages.error(request, 'Oops, There was an error, Please try again')
        return redirect('blog:blog-list')
    context = {
        'form':form
    }
    return render(request, 'blog/blog-create.html', context)

def BlogCategoryList(request, slug, pk):
    category = Category.objects.get(id=pk)
    blogs = Blog.objects.filter(category=category)
    latest_blog = Blog.objects.order_by('-pub_date')[:5]
    categories = Category.objects.order_by('view_count')[:10]

    paginator = Paginator(blogs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category.view_count +=1
    category.save()

    context = {
        'tag-obj':category,
        'blogs':page_obj,
        'latest_blog':latest_blog,
        'categories':categories
        }
    return render(request, 'blog/blog-tag-list.html', context)

def BlogTagList(request, slug, id):
    blogs = Blog.objects.flter(tags__slug=slug)
    tag = Tag.objects.filter(slug=slug)
    latest_blog = Blog.objects.order_by('-pub_date')[:5]
    categories = Category.objects.order_by('view_count')[:10]
    

    paginator = Paginator(blogs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag-obj':tag,
        'blogs':page_obj,
        'latest_blog':latest_blog,
        'categories':categories
    }
    return render(request, 'blog/blogs-tag-list.html', context)


@login_required
def BlogUpdateView(request, slug, id, *args, **kwargs):
    blog = get_object_or_404(Blog, slug=slug, id=id)
    form = BlogForm(request.POST or None, instance=blog)

    if request.method == 'POST' and request.user == blog.uploaded_by.user:
        if form.is_valid():
            form.save()
            messages.success(request, "Blog has been updated successfully")
            return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={'slug':slug, 'pk':id}))
        messages.success(request,"Something went wrong, Please try again")
        return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={'slug':slug, 'pk':id}))

    context = {
        'form':form
    }
    return render(request, 'blog/blog-update.html', context)

@login_required
def BlogDeleteView(request, slug,id):
    blog = Blog.objects.get(id=id)
    owner = blog.uploaded_by.user

    if request.method == 'POST' and request.user == owner:
        blog.delete()
        messages.success(request, "blog deleted")
        return redirect('blog:blog-list')
    messages.error(request, "You are not authorized")
    return HttpResponseRedirect('core:blog-detail', blog.slug, blog.id)

#django search
def searchBlog(request, *args, **kwargs):
    if request.method == 'GET':
        blog_query = request.GET['blog_query']
        if blog_query is not None and blog_query != u"":
            blog_query = request.GET['blog_query']
            blogs = Blog.objects.filter(title__icontains=blog_query)
            context = {
                'blog_query':blog_query,
                'blogs':blogs, 
                'categories':Category.objects.all(),
                }
            return render(request, 'blog/search_results.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'Oops! something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def CommentDeleteView(request, pk):
    comment = BlogComment.objects.get(id=pk)

    if request.method == 'POST' and request.user == comment.user:
        comment.delete()
        messages.success(request, "Comment deleted")
        return redirect('blog:blog-detail', comment.post.slug, comment.post.id)
    messages.error(request, "You are not authorized")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def UnauthenticatedCommentsRedirect(request, slug, pk):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == 'POST':
        next_url = reverse('blog:blog-detail', kwargs={'slug':slug, 'pk':blog.pk})
        login_url = reverse(settings.LOGIN_URL)
        messages.error(request,'Oops! please login to comment')
        return redirect(login_url+"?next="+next_url)
    messages.error(request, "Oops!.. An Error occured")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))