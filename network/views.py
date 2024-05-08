from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User
from .models import Post

import json

def index(request):
    if request.method == "POST":
        new_post = request.POST["new_post"]
        post = Post (information=new_post, author=request.user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        posts = Post.objects.all().order_by('-date')
        paginator = Paginator(posts, 10)  

        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        list_stranek = [i for i in range(1, paginator.num_pages+1)]
        return render (request, "network/index.html", {"posts": page_obj, "pages":list_stranek})
    
    
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Převedení JSON dat na Python slovník
        post_id = data.get('post_id', None)
        post = Post.objects.get(id=post_id)
        if not request.user in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
    return JsonResponse({'count_likes':len(post.likes.all())}, status=200)

def profile(request,author):
    # author = Post.objects.filter(author=author)

    posts = Post.objects.filter(author__username=author).order_by('-date')
    user_all = User.objects.get(username=author)
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get("page", 1) 
    page_obj = paginator.get_page(page_number)
    list_stranek = [i for i in range(1, paginator.num_pages+1)]
    return render (request, "network/profile.html", {
        "posts": page_obj,  
        "username_1":author,  
        "user_all":user_all, 
        "pages":list_stranek
        })
    



def follower(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        user_all = User.objects.get(username=user_name)
        if request.user != user_all:
            if not request.user in user_all.followers.all():
                user_all.followers.add(request.user)
            else:
                user_all.followers.remove(request.user)
        
    return HttpResponseRedirect(reverse("profile", kwargs={"author": user_name}))

def following_page(request):
    following_users = request.user.user_set.all()
    # Filtrování příspěvků, kde autor je mezi sledujícími uživateli
    following_posts = Post.objects.filter(author__in=following_users)
    # Vykreslení šablony s filtrovanými příspěvky
    paginator = Paginator(following_posts, 10)  

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    list_stranek = [i for i in range(1, paginator.num_pages+1)]
    return render (request, "network/following_page.html", {
        "posts": page_obj, 
        "pages":list_stranek
        })

def search_page(request):
    search_term = request.GET.get("new_search", '').strip()
    posts = Post.objects.filter(information__icontains = search_term).order_by('-date')
    paginator = Paginator(posts, 10)  
    
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    list_stranek = [i for i in range(1, paginator.num_pages+1)]
    return render (request, "network/search_page.html", {"posts": page_obj, "pages":list_stranek, "search_term":search_term})

    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
