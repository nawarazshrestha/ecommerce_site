from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from posts.forms import PostForm
from posts.models import Post
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .form import *

# Create your views here.
def index(request):
    today = timezone.now().date()
    PostForm_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        PostForm_list = Post.objects.all().count()
    query = request.GET.get("q")
    if query:
        PostForm_list = PostForm_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(PostForm_list, 5)  # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
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
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login Successfully')
            return redirect('/')
        else:
            messages.info(request, 'invalid Username and Password!')
            return redirect('/')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken')
            return redirect('register')
        else:
            if password1 != password2:
                messages.info(request, 'Password do not match')
                return redirect('register')
            else:
                newuser = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                   email=email, password=password1)
                new_profile = UserProfile(user=newuser, address=address, phone=phone)
                new_profile.save();
                messages.info(request, 'Register Successfully')
                return redirect('register')
        return redirect('register')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def profile(request):
    datas = UserProfile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'data': datas})


def Success(request):
    return render(request, 'success.html')

def product(request):
    today = timezone.now().date()
    PostForm_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        PostForm_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        PostForm_list = PostForm_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(PostForm_list, 5)  # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
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
    return render(request, "product1.html", context)


def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            template = get_template('contact_form.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_content': contact_content,
            }

            content = template.render(context)

            email = EmailMessage(
                "New contact form email",
                content,
                "Creative web" + '',
                ['nawarazstha@gmail.com'],
                headers={'Reply To': contact_email}
            )

            email.send()

            return redirect('success')
    return render(request, 'contact.html', {'form': Contact_Form})

