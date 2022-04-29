from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect


from django.views import generic as views


from ShareTheWorld.MAIN.forms import CreatePostForm, EditPostForm, DeletePostForm, CreatePlanForm, EditPlanForm, \
    DeletePlanForm, AddCommentForm, DeleteCommentForm
from ShareTheWorld.MAIN.models import Post, Plan, Comment




#----> Main  views start ----- #
class HomeView(views.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_nav_items'] = True
        return context

    def dispatch(self, request, *args, **kwargs):  # -----> CHECKS IF A USER IS LOGGED IN AND REDIRECTS SOMEWHERE ELSE
        if request.user.is_authenticated:
            return redirect('gallery')

        return super().dispatch(request, *args, **kwargs)


class GalleryView(views.ListView):
    model = Post
    template_name = 'main/gallery.html'
    context_object_name = 'post'


class PlanViewPage(views.ListView):
    model = Plan
    template_name = 'main/planner.html'
    context_object_name = 'plan'


#----> Main views end --------#




#----> posts views start ---------#



class CreatePostView(views.CreateView):
    template_name = 'posts/create-post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('gallery')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class EditPostView(views.UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('gallery')
    context_object_name = 'post'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("post details", kwargs={"pk": pk})


class DeletePostView(views.DeleteView):
    model = Post
    template_name = 'posts/delete-post.html'
    form_class = DeletePostForm
    success_url = reverse_lazy('gallery')
    context_object_name = 'post'




class DetailsPostView(views.DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context

#----> posts views end ----- #




# --------> plan CRUD views start ----- #



class CreatePlanView(views.CreateView):
    template_name = 'plans/create_plan.html'
    form_class = CreatePlanForm
    success_url = reverse_lazy('plans')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPlanView(views.UpdateView):
    model = Plan
    form_class = EditPlanForm
    template_name = 'plans/edit_plan.html'
    context_object_name = 'plan'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("plan details", kwargs={"pk": pk})



class DeletePlanView(views.DeleteView):
    model = Plan
    template_name = 'plans/delete_plan.html'
    form_class = DeletePlanForm
    success_url = reverse_lazy('plans')
    context_object_name = 'plan'


class DetailsPlanView(views.DetailView):
    model = Plan
    template_name = 'plans/plan details.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context

# --------> plan CRUD views end ----- #



# --------> comment CBV views start ----- #


class AddCommentView(views.CreateView):
    model = Comment
    template_name = 'comment/add_comment.html'
    form_class = AddCommentForm


    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("post details", kwargs={"pk": pk})





class CommentDeleteView(views.DeleteView):
    model = Comment
    form_class = DeleteCommentForm
    template_name = 'comment/delete_comment.html'


    def get_success_url(self):
        post = Post.objects.filter(comments=self.get_object())
        post_id = post.first().id
        return reverse_lazy('post details', kwargs={'pk': post_id})

# --------> comment CBV views end ----- #