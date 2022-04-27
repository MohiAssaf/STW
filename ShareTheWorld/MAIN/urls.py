from django.urls import path

from ShareTheWorld.MAIN.views import HomeView, GalleryView, CreatePostView, EditPostView, \
    DeletePostView, DetailsPostView, PlanViewPage, CreatePlanView, EditPlanView, DeletePlanView, DetailsPlanView, \
    AddCommentView, CommentDeleteView

urlpatterns = (

    path('', HomeView.as_view(), name='index'),

    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('plans/', PlanViewPage.as_view(), name='plans'),

    # This is the CRUD operations for the posts
    path('add/post/', CreatePostView.as_view(), name='create post'),
    path('edit/post/<int:pk>/', EditPostView.as_view(), name='edit post'),
    path('delete/post/<int:pk>/', DeletePostView.as_view(), name='delete post'),
    path('details/post/<int:pk>/', DetailsPostView.as_view(), name='post details'),

    # This is the CRUD operations for the plans
    path('add/plan/', CreatePlanView.as_view(), name='create plan'),
    path('edit/plan/<int:pk>/', EditPlanView.as_view(), name='edit plan'),
    path('delete/plan/<int:pk>/', DeletePlanView.as_view(), name='delete plan'),
    path('details/plan/<int:pk>/', DetailsPlanView.as_view(), name='plan details'),

    # This is the CD for the Comments
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add comment'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete comment'),

)

