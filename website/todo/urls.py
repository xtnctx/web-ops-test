
from django.urls import path, include
from knox import views as knox_views
from . import views

urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
    path('read/<int:pk>', views.ReadView.as_view(), name='read'),
     path('read/all/', views.ToDoListView.as_view(), name='all_todos'),
    path('update/', views.UpdateView.as_view(), name='update'),
#     path('delete/', views.CreateView.as_view(), name='delete'),
    path('auth/register/', views.RegisterAPI.as_view()),
    path('auth/login/', views.LoginAPI.as_view()),
    path('auth/user/', views.UserAPI.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/', include('knox.urls')),
]
