from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from .forms import PostForm
from .models import Post

# Create your views here.

def post_home(request):
    today = timezone.now().date()
    PostForm_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        PostForm_list = Post.objects.all().count()

    query = request.GET.get("q")
    if query:
        PostForm_list = PostForm_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(PostForm_list, 3) # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get('page_request_var')
    try:
        PostForm = paginator.page(page)
    except PageNotAnInteger:
        PostForm = paginator.page(1)
    except EmptyPage:
        PostForm = paginator.page(paginator.num_pages)
    context = {
        "object_list": PostForm,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
        
        }
    return render(request, "post/post.html", context)

def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404

    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Sucessfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Sucessfully Created")
    context = {
            "form": form,
        }
 
    return render(request, "post/post_form.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
            "title": instance.title,
            "instance": instance,
            "share_string": share_string,
        }
    return render(request, "post/post_detail.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Sucessfully delete")
    return redirect("posts:home")


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "title": instance.title,
            "instance": instance,
            "form": form,
        }
    return render(request, "post/post_form.html", context)

