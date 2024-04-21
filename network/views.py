from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

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
        # request.method == "GET":
        posts = Post.objects.all().order_by('-date')
        return render (request, "network/index.html", {"posts": posts})
    
# def is_liked(likes, user):
#       #vybiram vsechny likes
#     for like in likes:
#         if user.username == like.user.username:
#             return True
#     return False

    
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
