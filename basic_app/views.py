from django.shortcuts import render, redirect
from basic_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.views.generic import (View, TemplateView, ListView, DetailView)
from basic_app.forms import PostForm
from basic_app.models import Post
# Create your views here.

class IndexView(ListView):
    template_name = 'basic_app/index.html'
    model = Post
    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html', {'user_form':user_form,'prifile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE!')

        else:
            print('Someone tried to login and failed')
            print('Username: {} and password {}'.format(username,password))
            return HttpResponse('Invalid login details supplied!')

    else:
        return render(request,'basic_app/login.html', {})

class PostDetailView(DetailView):
    context_object_name = 'detail_post'
    template_name = 'basic_app/post_detail.html'
    model = Post


class AddPostView(TemplateView):
    template_name = 'basic_app/createpost.html'

    def get(self, request):
        form = PostForm()
        posts = Post.objects.all()
        args = {'form':form, 'posts':posts}
        return render(request, self.template_name, args)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = form.cleaned_data['title']
            if 'image' in request.FILES:
                post.image = request.FILES['image']
            post.save()
            return redirect('index')
        args = {'form':form, 'image':image}
        return render(request,self.template_name,args)


class UserAnnouncesList(ListView):
    model = Post
    template_name = 'basic_app/author_view.html'
    context_object_name = 'author_posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['pk'])


