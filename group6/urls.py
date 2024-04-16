"""
URL configuration for group6 project.

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
from django.urls import path
from g6app import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', views.testmysql),
    path('login/', views.user_login, name='login'),
    path('landing/', views.landing_page, name='landing_page'),
    path('', views.hero_page, name='hero_page'),
    path('register/', views.register, name='register'),
    path('auctions/', views.auctions,name='auctions'),
    path('auction/<int:auctionid>/', views.auction, name='auction'),
    path('auctionitem/<int:itemid>/', views.auctionitem, name='auctionitem'),
    path('placebid', views.placebid, name="place_bid"),
    path('admin/', views.admin_page, name='admin_page'),
    path('logout/', views.user_logout, name="logout"),
    #path('messages', views.messages, name="messages"),
]
