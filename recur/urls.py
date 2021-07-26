from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from recurapp import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)


urlpatterns = [
    path('', include('recurapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls, name='admin'),
]
