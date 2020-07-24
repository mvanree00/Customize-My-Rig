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
    path('info.html/', views.info, name='info'),
    path('about.html/', views.about, name='about')
]
