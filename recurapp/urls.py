from django.urls import path
from . import views
from django.contrib import admin

app_name = 'recurapp'


urlpatterns = [
    path('', views.home, name='home'),
    path('desc_search/', views.desc_search, name='desc_search'),
    path('desc_search/refuse/<int:food_code>/', views.ndb_search, name='ndb_search'),
    path('desc_search/<int:food_code>/', views.nutrient_search, name='nutrient_search'),
    path('calorieDisplay/', views.calorieDisplay, name='calorieDisplay'),
    path('calorieCreate/', views.calorieCreate, name='calorieCreate'),
    path('accounts/profile/', views.profile, name='profile'),
    path('create_meal/', views.create_meal, name='create_meal'),
    path('admin/', admin.site.urls, name='admin'),
]
