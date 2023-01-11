from django.urls import path

from user.views import GetUsers, CreateUsers, GetUserDetail, DeleteUser, Login, UpdateUser

urlpatterns = [
    path('', GetUsers.as_view(), name='get-users'),
    path('<int:pk>/', GetUserDetail.as_view(), name='get-user-detail'),
    path('create/', CreateUsers.as_view(), name='create-users'),
    path('delete/<int:pk>/', DeleteUser.as_view(), name='delete-user'),
    path('login/', Login.as_view(), name='login'),
    path('update/', UpdateUser.as_view(), name='update-user'),

]
