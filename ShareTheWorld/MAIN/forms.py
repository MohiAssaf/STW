from django import forms


from ShareTheWorld.MAIN.models import Post, Plan, Comment
from ShareTheWorld.validators.helpers import BootstrapFormMixin

# ------------ Start of FORM CBV for post -----------#
class CreatePostForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        post = super().save(commit=False)
        post.user = self.user
        if commit:
            post.save()

        return post

    class Meta:
        model = Post
        fields = ('owner', 'photo', 'place_visited', 'date_visited', 'description')
        widgets = {
            'owner': forms.TextInput(
                attrs={
                    'placeholder': 'Owner of the post',
                }
            ),
            'photo': forms.URLInput(
                attrs={
                    'placeholder': 'Photo of the post',
                }
            ),
            'place_visited': forms.TextInput(
                attrs={
                    'placeholder': 'destination of the post',
                }
            ),
            'date_visited': forms.DateInput(
                attrs={
                    'placeholder': 'Date of the visit',
                }
            ),
        }

class EditPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_visited'].disabled = True
        self.fields['place_visited'].disabled = True
        self.fields['photo'].disabled = True

    class Meta:
        model = Post
        fields = ('owner', 'photo', 'place_visited', 'date_visited', 'description')


class DeletePostForm(BootstrapFormMixin, forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Post
        fields = ()


# ------------ End of form CBV for post -----------#



# ------------ Start of form CBV for plans -----------#
class CreatePlanForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        plan = super().save(commit=False)
        plan.user = self.user
        if commit:
            plan.save()

        return plan

    class Meta:
        model = Plan
        fields = ('flag_of_place', 'name_of_place', 'budget', 'note', 'date_going')
        widgets = {
            'flag_of_place': forms.URLInput(
                attrs={
                    'placeholder': 'picture of the flag',
                }
            ),
            'name_of_place': forms.TextInput(
                attrs={
                    'placeholder': 'Name of the place visiting',
                }
            ),

            'budget': forms.NumberInput(
                attrs={
                    'placeholder': 'The budget for the journey',
                }
            ),
        }


class EditPlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ('flag_of_place', 'name_of_place', 'budget', 'note', 'date_going')




class DeletePlanForm(BootstrapFormMixin, forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for _, field in self.fields.items():
    #         field.widget.attrs['disabled'] = 'disabled'
    #         field.required = False  # this is to disable all the fields

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Plan
        fields = ()


# ------------ End of form CBV for plan -----------#



# ------------ Start of form CBV for comments -----------#

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_owner', 'comment_body')
        widgets = {
            'comment_owner': forms.TextInput(
                attrs={
                    'placeholder': 'owner of the comment',
                    'class': 'form-control',
                }
            ),
            'comment_body': forms.Textarea(
                attrs={
                    'placeholder': 'comment',
                     'class': 'form-control',
                }
            ),
        }



class DeleteCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ()

# ------------ End of form CBV for comments -----------#


