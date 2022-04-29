from django.contrib.auth import views as auth_views, update_session_auth_hash, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth.forms import PasswordChangeForm

from ShareTheWorld.MAIN.models import Post
from ShareTheWorld.accounts.forms import CreateProfileForm, EditProfileForm
from ShareTheWorld.accounts.models import Profile, STWUser
from django.contrib import messages
from django.contrib import auth

# -------- Start of User CBV ---------#


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('login user')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('gallery')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

def LogoutPage(request):
    auth.logout(request)
    return render(request, 'accounts/logout-page.html')

#--------- End of user CBV ---------#

# -------- Start of Profile CBV ---------#

class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = list(Post.objects.filter(user_id=self.object.user_id))

        post_count = len(posts)

        context.update({
            'post_count': post_count,

        })

        return context



class ProfileEditView(views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("profile details", kwargs={"pk": pk})



def DeleteProfileView(request, pk):
    user = STWUser.objects.get(username=request.user.username)
    logout(request)
    user.delete()

    return redirect('index')



#--------- End of profile CBV ---------#


# ----------- password change ----------#

def ChangePasswordView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


