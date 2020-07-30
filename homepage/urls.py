from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('case/', views.case, name='case'),
    path('type/', views.type, name='type'),
    path('brand/', views.brand, name='brand'),
    path('hardware/', views.hardware, name='hardware'),
    path('results/<int:build_ID>', views.results, name='pastResults'),
    path('results', views.results, name='results'),
    path('lower_results', views.lower_results, name='lower_results'),
    path('upper_results', views.upper_results, name='upper_results'),
    path('info.html/', views.info, name='info'),
    path('about.html/', views.about, name='about')
]
