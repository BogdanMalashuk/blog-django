from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Comment
# from .signals.signals import user_registered


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
                    # user_registered.send(sender=request, user=user, timestamp=now())  # сигнал о регистрации
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
def delcomment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    else:
        messages.error(request, "Только автор может удалить комментарий.", extra_tags='root_error')
    return redirect('postdetail', post_id=post_id)


@login_required
def reply_to_comment(request, comment_id):
    parent_comm = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        reply = form.save(commit=False)
        reply.article = parent_comm.article
        reply.author = request.user
        reply.parent = parent_comm
        reply.save()

    return redirect('postdetail', post_id=parent_comm.article.id)


@login_required
def addpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # без записи в бд
            post.author = request.user
            post.save()
            return redirect('main')
    else:
        form = PostForm()
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


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)
        post.likes -= 1
        if post.likes < 0:
            post.likes = 0
    else:
        post.liked_users.add(request.user)
        post.likes += 1
        if request.user in post.disliked_users.all():
            post.disliked_users.remove(request.user)
            post.dislikes -= 1

    post.save()
    return redirect('postdetail', post_id=post.id)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.disliked_users.all():
        post.disliked_users.remove(request.user)
        post.dislikes -= 1
    else:
        post.disliked_users.add(request.user)
        post.dislikes += 1
        if request.user in post.liked_users.all():
            post.liked_users.remove(request.user)
            post.likes -= 1

    post.save()
    return redirect('postdetail', post_id=post.id)
