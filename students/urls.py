from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('add/add_student/', views.add_student, name='add_student'),
    path('add/add_group/', views.add_group, name='add_group'),
    path('delete/<int:id>', views.delete_student, name='delete'),
    path('group_detail/<int:group_id>/update/<int:id>', views.update_student, name='update'),
    path('group_detail/<int:group_id>/update/update_student/<int:id>', views.update_record, name='update_record'),
    path('vote/<int:group_id>/', views.vote, name='vote'),
    path('vote_list/<int:group_id>/', views.vote_list, name='vote_list'),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
]