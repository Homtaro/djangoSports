from django import forms
from django.contrib.auth.models import User, Permission

from .models import SportStructure, SportStructureImage, Category, Tag, Rating, Comment


class SportStructureForm(forms.ModelForm):
    class Meta:
        model = SportStructure
        fields = ['name', 'description', 'rating', 'category', 'address', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class SportStructureImageForm(forms.ModelForm):
    class Meta:
        model = SportStructureImage
        fields = ['sport_structure', 'image', 'description']


class TagsForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['sport_structure', 'user', 'rating']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['sport_structure', 'user', 'text']


class RatingFormUser(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Your Rating"
    )


class CommentFormUser(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Leave your comment here...',
                'class': 'form-control'
            }),
        }



# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email', 'first_name', 'last_name']
#
#     password = forms.CharField(widget=forms.PasswordInput())

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


# class UserPermissionsForm(forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#
#     class Meta:
#         model = User
#         fields = ['permissions']

# class UserPermissionsForm(forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.filter(content_type__app_label='djangoSportApp'),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#         label="User Permissions"
#     )
#
#     class Meta:
#         model = User
#         fields = ['permissions']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['permissions'].initial = self.instance.user_permissions.all()

class UserPermissionsForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__app_label='djangoSportApp'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="User Permissions"
    )

    class Meta:
        model = User
        fields = ['permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['permissions'].initial = self.instance.user_permissions.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user
