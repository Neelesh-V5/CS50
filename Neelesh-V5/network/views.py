from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms import ModelForm, Textarea
from django.core.paginator import Paginator
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime

from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['contents']
        labels = {
            "contents" : ("")
        }
        widgets = {
            "contents" : Textarea(attrs={"rows": 5})
        }

def index(request):
    if request.method == 'GET':
        post_list = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if not page_number:
            page_number = 1 

        form = PostForm

        return render(request, "network/index.html",{
            'form' : form,
            "page_obj" : page_obj,
            "prev" : page_obj.has_previous(),
            "next" : page_obj.has_next(),
            "page_number" : int(page_number)
        })

def following(request):
    if request.method == 'GET':
        # post_list = Post.objects.all().order_by("-timestamp")
        following_objs = Follow.objects.filter(follower = request.user)
        post_list = []
        for following_obj in following_objs:
            followed_user = following_obj.followed
            posts = Post.objects.filter(poster = followed_user)
            for post in posts:
                post_list.append(post)

        paginator = Paginator(post_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if not page_number:
            page_number = 1 

        return render(request, "network/following.html",{
            "page_obj" : page_obj,
            "prev" : page_obj.has_previous(),
            "next" : page_obj.has_next(),
            "page_number" : int(page_number)
        })
    

def post_view(request, id):
    try:
        post = Post.objects.get(id = id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        print(serializers.serialize('json', [post,]))
        return JsonResponse(serializers.serialize('json', [post,]) , safe=False)
    
def like_count(request, id):
    try:
        post = Post.objects.get(id = id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == 'GET':
        liked = Like.objects.filter(post = post)
        post.likes = len(liked)
        post.save()
        print(liked, post.likes)
        return JsonResponse(str(post.likes), safe=False)

@csrf_exempt
def like_view(request, id):
    if request.method == "GET":
        try:
            post = Post.objects.get(id = id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        try:
            liked = Like.objects.get(liked_by = request.user, post = post)
            liked = True
        except Like.DoesNotExist:
            liked = False
        
        return JsonResponse(str(liked), safe=False)
    
    elif request.method == "PUT":
        try:
            post = Post.objects.get(id = id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        data = json.loads(request.body)

        try:
            liked = Like.objects.get(liked_by = request.user, post = post)
        except Like.DoesNotExist:
            liked = False

        if data.get("like") is not None:
            if data['like']:
                if not liked:
                    new_like = Like.objects.create(post = post, liked_by = request.user)
                    new_like.save()
            else:
                if liked:
                    liked.delete()
                    
            no_liked = Like.objects.filter(post = post)
            post.likes = len(no_liked)
            post.save()
        return HttpResponse(status=204)

def profile(request, id):
    if request.method == "GET":
        user = User.objects.get(id = id)
        user_id = user.id
        name = user.username
        post_list = Post.objects.filter(poster = user).order_by("-timestamp")
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if not page_number:
            page_number = 1 

        print()

        return render(request, "network/profile.html",{
            'name' : name,
            "user_id" : user_id,
            "page_obj" : page_obj,
            "prev" : page_obj.has_previous(),
            "next" : page_obj.has_next(),
            "page_number" : int(page_number)
        })

@csrf_exempt  
def follow_count(request, id):
    try:
        user = User.objects.get(id = id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    if request.method == 'GET':
        followed_by = Follow.objects.filter(followed = user)
        following = Follow.objects.filter(follower = user)
        user.followed_by = len(followed_by)
        user.following = len(following)
        user.save()

        if request.user.is_authenticated:
            try:
                followed = Follow.objects.get(followed = user, follower = request.user)
                followed = True
            except Follow.DoesNotExist:
                followed = False
        else:
            followed = False

        #str(followed) + str(user.followed_by) + ',' + str(user.following
        return JsonResponse((str(followed) + ',' + str(user.followed_by) + ',' + str(user.following )), safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        try:
            followed = Follow.objects.get(follower = request.user, followed = user) 
        except Follow.DoesNotExist:
            followed = False

        if data.get('follow') is not None:
            if data['follow']:
                if not followed:
                    new_follow = Follow.objects.create(followed = user, follower = request.user)
                    new_follow.save()
            else:
                if followed:
                    print("Delete")
                    followed.delete()

            followed_by = Follow.objects.filter(followed = user)
            following = Follow.objects.filter(follower = user)
            user.followed_by = len(followed_by)
            user.following = len(following)
            user.save()

        return HttpResponse(status = 204)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): 
            item = form.save(commit=False)
            item.poster = request.user
            item.save()

        return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
@login_required
def edit(request, id):
    try:
        post = Post.objects.get(id = id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data['contents']:
            contents = data['contents']
            print(contents)
            if post.contents != contents:
                post.contents = contents
                post.last_mod = datetime.datetime.now()
                post.edited = True
                post.save()
        print(serializers.serialize('json', [post,]))
        return JsonResponse(serializers.serialize('json', [post,]) , safe=False)
        

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
