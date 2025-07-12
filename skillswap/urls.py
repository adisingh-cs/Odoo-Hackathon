"""
URL configuration for skillswap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('skills/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    path('search/', views.search, name='search'),
    path('swap/<int:skill_id>/', views.create_swap, name='create_swap'),
    path('swaps/', views.swap_inbox, name='swap_inbox'),
    path('swaps/<int:swap_id>/<str:action>/', views.update_swap, name='update_swap'),
    path('feedback/<int:swap_id>/', views.leave_feedback, name='leave_feedback'),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)