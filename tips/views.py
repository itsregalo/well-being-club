from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Tip, TipComment, TipTags, Category
from django.core.paginator import Paginator
from .forms import TipForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from itertools import chain
from django.conf import settings
from taggit.models import Tag



# Create your views here.
def TipListView(request, *args, **kwargs):
    tip = Tip.objects.all()
    categories = Category.objects.order_by('view_count')[:10]

    paginator = Paginator(tip, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #to do recent posts
    
    context = {
        'tips':page_obj,
        'latest_tip':Tip.objects.order_by('-pub_date')[:5],
        'popular_tip':Tip.objects.all().order_by('view_count')[:3],
        'categories':categories,
    }
    return render(request, 'tip/tip_list.html', context)

def TipDetailView(request, slug, *args, **kwargs):
    tip = get_object_or_404(Tip, slug=slug)
    tip_comments = tip.get_tip_comments()
    comment_form = CommentForm()
    related_posts = Tip.objects.filter(category=tip.category).order_by('-pub_date').exclude(slug=slug)[:5]
    tips_by_author = Tip.objects.filter(uploaded_by=tip.uploaded_by).order_by('-pub_date').exclude(slug=slug)[:5]
    categories = Category.objects.all()[:10]

    if request.method == 'POST':
        next_url = reverse('tips:tip-detail', kwargs={'slug':slug, 'pk':tip.pk})
        login_url = reverse(settings.LOGIN_URL)

        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = tip
                new_comment.save()
                return HttpResponseRedirect(reverse('tips:tip-detail', kwargs={'slug':slug, 'pk':tip.pk}))
            messages.error(request,'Oops! please try again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request,'Oops! please login to comment')
        return redirect(login_url+"?next="+next_url)

    context = {
        'tip':tip,
        'tip_comments':tip_comments,
        'latest_tip':Tip.objects.order_by('-pub_date')[:5],
        'comment_form':comment_form,
        'related_posts':related_posts,
        'tips_by_author':tips_by_author,
        'categories':categories,
    }

    return render(request, 'tip/tip_detail.html', context)

@login_required
def TipCreateView(request, *args, **kwargs):
    form = TipForm()
    if request.method == 'POST':
        form = TipForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_tip = form.save(commit=False)
            new_tip.uploaded_by = request.user
            new_tip.save()
            messages.success(request, 'tip added successfully')
            return redirect('tips:tip-list')
        messages.error(request, 'Oops, There was an error, Please try again')
        return redirect('tips:tip-list')
    context = {
        'form':form
    }
    return render(request, 'tip/tip-create.html', context)

def TipCategoryList(request, slug, pk):
    category = Category.objects.get(id=pk)
    tips = Tip.objects.filter(category=category)
    latest_tip = Tip.objects.order_by('-pub_date')[:5]
    categories = Category.objects.order_by('view_count')[:10]

    paginator = Paginator(tips, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category.view_count +=1
    category.save()

    context = {
        'tag-obj':category,
        'tips':page_obj,
        'latest_tip':latest_tip,
        'categories':categories
        }
    return render(request, 'tip/tip-tag-list.html', context)

def TipTagList(request, slug, id):
    tips = Tip.objects.flter(tags__slug=slug)
    tag = Tag.objects.filter(slug=slug)
    latest_tip = Tip.objects.order_by('-pub_date')[:5]
    categories = Category.objects.order_by('view_count')[:10]
    

    paginator = Paginator(tips, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag-obj':tag,
        'tips':page_obj,
        'latest_tip':latest_tip,
        'categories':categories
    }
    return render(request, 'tip/tips-tag-list.html', context)


@login_required
def TipUpdateView(request, slug, id, *args, **kwargs):
    Tip = get_object_or_404(Tip, slug=slug, id=id)
    form = TipForm(request.POST or None, instance=tip)

    if request.method == 'POST' and request.user == tip.uploaded_by.user:
        if form.is_valid():
            form.save()
            messages.success(request, "Tip has been updated successfully")
            return HttpResponseRedirect(reverse('tips:tip-detail', kwargs={'slug':slug, 'pk':id}))
        messages.success(request,"Something went wrong, Please try again")
        return HttpResponseRedirect(reverse('tips:tip-detail', kwargs={'slug':slug, 'pk':id}))

    context = {
        'form':form
    }
    return render(request, 'tip/tip-update.html', context)

@login_required
def TipDeleteView(request, slug,id):
    tip = Tip.objects.get(id=id)
    owner = tip.uploaded_by.user

    if request.method == 'POST' and request.user == owner:
        tip.delete()
        messages.success(request, "tip deleted")
        return redirect('tips:tip-list')
    messages.error(request, "You are not authorized")
    return HttpResponseRedirect('core:tip-detail', tip.slug, tip.id)

#django search
def searchTip(request, *args, **kwargs):
    if request.method == 'GET':
        tip_query = request.GET['tip_query']
        if tip_query is not None and tip_query != u"":
            tip_query = request.GET['tip_query']
            tips = Tip.objects.filter(title__icontains=tip_query)
            context = {
                'tip_query':tip_query,
                'tips':tips, 
                'categories':Category.objects.all(),
                }
            return render(request, 'tip/search_results.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'Oops! something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def CommentDeleteView(request, pk):
    comment = TipComment.objects.get(id=pk)

    if request.method == 'POST' and request.user == comment.user:
        comment.delete()
        messages.success(request, "Comment deleted")
        return redirect('tips:tip-detail', comment.post.slug, comment.post.id)
    messages.error(request, "You are not authorized")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def UnauthenticatedCommentsRedirect(request, slug, pk):
    tip = get_object_or_404(Tip, slug=slug)

    if request.method == 'POST':
        next_url = reverse('tips:tip-detail', kwargs={'slug':slug, 'pk':tip.pk})
        login_url = reverse(settings.LOGIN_URL)
        messages.error(request,'Oops! please login to comment')
        return redirect(login_url+"?next="+next_url)
    messages.error(request, "Oops!.. An Error occured")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))