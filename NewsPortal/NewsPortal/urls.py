"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from news.views import (
    subscriptions, CategoryListView,
)

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('newsportal/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('subscriptions/', subscriptions, name='subscriptions'),
    # path('articles/', include('news.urls')),
    # path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),  #  вебинар D 9/11 ??? delete!!!

]