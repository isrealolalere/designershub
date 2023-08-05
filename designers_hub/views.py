from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.mail import send_mail


# Create your views here.
def home(request):
    if request.method == 'POST':    
        search = request.POST['query']

        search_results = Post.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if search_results:
            posts = search_results
        else:
            messages.success(request, 'Matched results')
            posts = Post.objects.all()

        context = {
            'posts': posts,
            'show_search_bar': True
        }

        return render(request, 'core/home.html', context)
    else:
        posts = Post.objects.all()
        context = {
            'posts': posts,
            'show_search_bar': True
        }
        return render(request, 'core/home.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignupForm()
        if request.method == 'POST':
            form = SignupForm(request.POST or None, request.FILES)
            if form.is_valid():
                user = form.save()

                #saving the info into the customized model
                user_password = form.cleaned_data.get('password1')
                image = form.cleaned_data.get('profile_img')

                User_info.objects.create(
                    user=user,
                    user_password=user_password,
                    user_img = image
                )

                #authentication
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'You have successfully signed up')
                return redirect('home')
            else:
                messages.success(request, 'Invalid form')
                return render(request, 'auth/signup.html', context={
                    'form':form,
                    'show_search_bar': False
                })
        else:
            return render(request, 'auth/signup.html', context={
                'form':form,
                'show_search_bar': False
            })
        

@login_required
def update_profile(request):
    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST or None, request.FILES, instance=request.user)
        if update_form.is_valid():
            new_img = update_form.cleaned_data.get('profile_img')
            user = User_info.objects.filter(user=request.user)[0]

            if new_img != None:
                print("one image chosen")
                user.user_img = new_img
                user.save()
                update_form.save()
            
            messages.success(request, "Profile information successfully updated")
            return redirect('home')
        else:
            print(update_form.errors)
            messages.success(request, "Invalid informations")
            return redirect('update_profile')
    else:
        update_form = UpdateProfileForm(instance=request.user)
        user_info = User_info.objects.get(user__username=request.user.username)
        return render(request, 'auth/update-profile.html', context={
            'update_profile_form':update_form,
            'user_info':user_info,
            'show_search_bar': False
        })




def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST or None, request.FILES)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You have been logged in')
                    return redirect('home')
                else:
                    messages.success(request, 'User is not found. Check your details carefully')
                    return redirect('login')
            else:
                messages.success(request, 'User is not found. Check your details carefully')
                return redirect('login')
        else:
            return render(request, 'auth/signin.html', context={'form':form, 'show_search_bar': False})
        
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. Thank you')
    return redirect('login')


@login_required
def new_post(request):
    post_form = NewPost()
    if request.method == 'POST':
        post_form = NewPost(request.POST or None, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            user = User_info.objects.get(user=request.user)
            post.author = user
            post.save()
            return redirect('home')
        
        else:
            user_info = User_info.objects.get(user__username=request.user.username)
            return render(request, 'core/post.html', context={'post_form':post_form, 'user_info': user_info, 'show_search_bar': False})
    else:
        user_info = User_info.objects.get(user__username=request.user.username)
        return render(request, 'core/post.html', 
            context= {
                'post_form':post_form,
                'user_info':user_info,
                'show_search_bar': False
            }
        )


def view_post(request, id):
    post = Post.objects.get(pk=id)
    all_user_post = Post.objects.filter(author__user=post.author.user).exclude(pk=id)

    return render(request, 'core/view-post.html', context={
        'post':post,
        'all_user_post':all_user_post,
        'show_search_bar': True
    })


@login_required
def profile(request, user):
    # Ensure the requested user matches the currently logged-in user
    if request.user.username != user:
        return HttpResponseForbidden("You are not allowed to access this profile.")

    user_posts = Post.objects.filter(author__user__username=user)
    user_info = User_info.objects.get(user=request.user)
    return render(request, 'profile-temps/user-posts.html', context={
        'user_posts':user_posts,
        'user_info': user_info,
        'show_search_bar': False
    })



@login_required
def like_post(request, id):
    post = Post.objects.get(pk=id)
    user = request.user
    current_likes = post.likes
    liked = Like.objects.filter(user=user, post=post)

    if not liked:
        liked = Like.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked.delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return JsonResponse({'likes': current_likes})



@login_required
def delete_post(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('profile', user=request.user.username)


@login_required
def update_post(request, id):
    if request.user.is_authenticated:
        current_post = Post.objects.get(pk=id)
        update_form = NewPost(request.POST or None, instance=current_post)
        if request.method == 'POST':
            update_form = NewPost(request.POST or None, request.FILES, instance=current_post)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'You have successfully updated this post')
                return redirect('profile', user = request.user.username)
            else:
                messages.success(request, 'Enter valid informations')
                return redirect('update_post', id=id)
        else:
            user_info = User_info.objects.get(user__username=request.user.username)
            context = {
                'update_form':update_form,
                'user_info':user_info,
                'current_post': current_post,
                'show_search_bar': False
            }
            return render(request, 'core/update-post.html', context)
    else:
        messages.success(request, 'You have to sign up before you can access this page')
        return redirect('home')


def contact_us(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']

            #send the email
            subject = 'Contacted from designers hub'
            email_body = f"Name: {name} \nEmail: {email}\nMessage: {message}"
            sender_email = email
            receiver_email = 'isrealolalere09@gmail.com'

            send_mail(
                subject, 
                email_body, 
                sender_email, 
                [receiver_email],
            )

            messages.success(request, f"Hey {name}!, Thanks for contacting us. \nWe will reply as soon as possible")
            return redirect('home')

        except TimeoutError as e:
            messages.success(request, f"Sorry, {name}!, We couldn't process your request, try again")
            return redirect('contact_us')

    return render(request, 'core/contact.html')


def news_letter(request):
    if request.method == 'POST':
        email = request.POST['newsemail']
         
        email_queryset = NewsLetterEmail.objects.filter(email=email)
        if not email_queryset:
            NewsLetterEmail.objects.create(
                email=email
            )
            messages.success(request, 'Thanks for subscribing')
            return redirect('home')
        else:
            messages.success(request, 'Email already added')
            return redirect('home')
