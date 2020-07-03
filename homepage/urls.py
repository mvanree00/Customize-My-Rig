from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('case/', views.case, name='case'),
    path('results', views.results, name='results'),
    path('info.html/', views.info, name='info'),
    path('about.html/', views.about, name='about')
]
