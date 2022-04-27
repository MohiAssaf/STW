from django.urls import path

from ShareTheWorld.accounts.views import UserLoginView, UserRegisterView, ProfileDetailsView, \
    ProfileEditView, ChangePasswordView, LogoutPage, DeleteProfileView

urlpatterns = (

    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutPage, name='logout user'),

    path('profile_details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView, name='delete profile'),

    path('edit-password/', ChangePasswordView, name='change password'),
)
