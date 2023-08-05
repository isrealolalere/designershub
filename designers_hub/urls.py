from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new-post/', views.new_post, name='post'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.signin_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('post/<int:id>/', views.view_post, name='view_post'),
    path('profile/<slug:user>/', views.profile, name='profile'),
    path('profile/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('profile/update/<int:id>/', views.update_post, name='update_post'),
    path('like_post/<int:id>/', views.like_post, name='like_post'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('newsletter', views.news_letter, name='news_letter'),
]