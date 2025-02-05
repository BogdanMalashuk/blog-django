from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Comment


def home(request):
    return redirect('register')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']  # данные с формы
            password = form.cleaned_data['password']
            if 'login' in request.POST:
                user = authenticate(request, username=username, password=password)  # аутентиф юзера
                if user:
                    login(request, user)  # вход
                    return redirect('main')
                else:
                    messages.error(request, "Incorrect username or password.",  extra_tags='registration_error')

            elif 'register' in request.POST:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "This username is already taken.",  extra_tags='registration_error')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                    return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def main(request):
    posts = Post.objects.all()
    return render(request, 'main.html', {'user': request.user, 'posts': posts})


def profile(request):
    return render(request, 'profile.html')


def postdetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()  # пустая форма
    if 'addcomment' in request.POST:
        if request.method == 'POST':
            form = CommentForm(request.POST)  # форма с заполненными данными
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('postdetail', post_id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def delcomment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    cpid = comment.post.id
    if request.user == comment.author:
        comment.delete()
    else:
        messages.error(request, "Только автор может удалить комментарий.", extra_tags='root_error')
    return redirect('postdetail', cpid)


@login_required
def addpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # без записи в бд
            post.author = request.user
            post.save()  # с записью в бд
            return redirect('main')
    else:
        form = PostForm()  # пустая форма
    return render(request, 'addpost.html', {'form': form})


@login_required
def deletepost(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # определяет и записывает пост
    if request.user != post.author:
        messages.error(request, "Only author can edit this post.", extra_tags='root_error')
        referer = request.META.get('HTTP_REFERER', 'main')   # определяет отправителя, либо на мейн
        return redirect(referer)
    else:
        post.delete()
        return redirect('main')


@login_required
def editpost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        messages.error(request, "Only author can edit this post.", extra_tags='root_error')
        referer = request.META.get('HTTP_REFERER', 'main')  # определяет отправителя, либо на мейн
        return redirect(referer)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('postdetail', post_id)
    else:
        form = PostForm(instance=post)  # форма с данными из объекта пост
    return render(request, 'editpost.html', {'form': form})
