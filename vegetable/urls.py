# """
# URL configuration for vegetable project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from vege.views import *
# from django.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns = [
#     path('receipes/', receipes),
#     path('admin/', admin.site.urls),
# ]
# urlpatterns += staticfiles_urlpatterns()

from django.contrib import admin
from django.urls import path
from vege.views import receipes, delete_receipe,update_recipes, login_page, register_page, logout_page, get_students, see_marks, send_email
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', receipes),
    path('logout/',logout_page),
    path('register/', register_page),
    path('login/', login_page),
    path('delete_receipe/<id>/', delete_receipe),
    path('update_receipe/<id>/', update_recipes),
    path('receipes/', receipes),
    path('student/',get_students),
    path('admin/', admin.site.urls),
    path('see_marks/<student_id>/', see_marks, name = "see_marks"),
    path('send-email/', send_email, name='send_email'),
    # Ensure 'send_email' matches
]


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
