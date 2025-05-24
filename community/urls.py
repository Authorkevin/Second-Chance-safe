from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.topic_list_view, name='topic_list'),
    path('topic/<int:topic_id>/', views.topic_detail_view, name='topic_detail'),
    path('topic/create/', views.create_topic_view, name='create_topic'),
    path('topic/<int:topic_id>/comment/', views.add_comment_view, name='add_comment'),
]
