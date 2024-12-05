
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_translation_scores, name='translation_scores'),
    path('get_translation_scores/', views.get_translation_scores, name='get_translation_scores'),

]