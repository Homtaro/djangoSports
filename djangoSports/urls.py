"""
URL configuration for djangoSports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from djangoSportApp import views
from djangoSportApp.views import login_view, signup_view, profile_view, user_password_change

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('', views.dummy_page, name='dummyPage'),
    path('catalogue/', views.catalogue_page, name='catalogue'),
    path('catalogue/structure/<int:pk>/', views.structure_detail_user, name='structure_detail_user'),

    #SportStructure CRUD
    path('structures/', views.structure_list, name='structure_list'),
    path('structures/add/', views.structure_create, name='structure_create'),
    path('structures/<int:pk>/', views.structure_detail, name='structure_detail'),
    path('structures/<int:pk>/edit/', views.structure_update, name='structure_update'),
    path('structures/<int:pk>/delete/', views.structure_delete, name='structure_delete'),

    #SportStructureImage CRUD
    path('images/', views.image_list, name='image_list'),
    path('images/create/', views.image_create, name='image_create'),
    path('images/update/<int:pk>/', views.image_update, name='image_update'),
    path('images/delete/<int:pk>/', views.image_delete, name='image_delete'),

    #Tags CRUD
    path('tags/', views.tags_list, name='tags_list'),
    path('tags/create/', views.tags_create, name='tags_create'),
    path('tags/update/<int:pk>/', views.tags_update, name='tags_update'),
    path('tags/delete/<int:pk>/', views.tags_delete, name='tags_delete'),

    #Category CRUD
    path('categories/', views.categories_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    #Comment CRUD
    path('comments/', views.comment_list, name='comments_list'),
    path('comments/create/', views.comment_create, name='comments_create'),
    path('comments/update/<int:pk>/', views.comment_update, name='comments_update'),
    path('comments/delete/<int:pk>/', views.comment_delete, name='comments_delete'),

    #Rating CRUD
    path('ratings/', views.rating_list, name='ratings_list'),
    path('ratings/create/', views.rating_create, name='ratings_create'),
    path('ratings/update/<int:pk>/', views.rating_update, name='ratings_update'),
    path('ratings/delete/<int:pk>/', views.rating_delete, name='ratings_delete'),

    #User CRUD
    path('users/', views.user_list, name='users_list'),
    path('users/create/', views.user_create, name='users_create'),
    path('users/update/<int:pk>/', views.user_update, name='users_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='users_delete'),
    path('users/<int:pk>/permissions/', views.user_permissions, name='user_permissions'),
    path('users/<int:pk>/change-password/', user_password_change, name='user_password_change'),







]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
