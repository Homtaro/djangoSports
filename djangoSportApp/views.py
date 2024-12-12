from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django import forms

from djangoSportApp.forms import SportStructureForm, SportStructureImageForm, TagsForm, CategoryForm, CommentForm, \
    RatingForm, UserPermissionsForm, CustomUserEditForm, RatingFormUser, CommentFormUser
from djangoSportApp.models import SportStructure, Category, Tag, SportStructureImage, Rating, Comment


# Create your views here.

def dummy_page(request):
    return render(request, 'dummyPage.html')


# def catalogue_page(request):
#     return render(request, 'catalogue.html')
#
# def catalogue_page(request):
#     sport_structures = SportStructure.objects.all()
#     return render(request, 'catalogue.html', {'sport_structures': sport_structures})

# def catalogue_page(request):
#     sport_structures = SportStructure.objects.all()
#     paginator = Paginator(sport_structures, 3)  # 9 items per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'catalogue.html', {'page_obj': page_obj})

# def catalogue_page(request):
#     # Fetch all categories and tags
#     categories = Category.objects.all()
#     tags = Tag.objects.all()
#
#     # Start with fetching all structures
#     structures = SportStructure.objects.all()
#
#     # Check for a search query and apply it if present
#     search_query = request.GET.get('search', '')
#     if search_query:
#         structures = structures.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )
#
#     # Filter by selected categories and tags if provided
#     selected_categories = request.GET.getlist('category')
#     selected_tags = request.GET.getlist('tag')
#
#     if selected_categories:
#         structures = structures.filter(category__id__in=selected_categories)
#
#     if selected_tags:
#         structures = structures.filter(tags__id__in=selected_tags)
#
#     # Pagination
#     paginator = Paginator(structures, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'catalogue.html', {
#         'categories': categories,
#         'tags': tags,
#         'page_obj': page_obj,
#         'selected_categories': [int(c) for c in selected_categories],
#         'selected_tags': [int(t) for t in selected_tags],
#         'search_query': search_query,
#     })

def catalogue_page(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    structures = SportStructure.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        structures = structures.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filters
    selected_categories = request.GET.getlist('category')
    selected_tags = request.GET.getlist('tag')

    if selected_categories:
        structures = structures.filter(category__id__in=selected_categories)

    if selected_tags:
        structures = structures.filter(tags__id__in=selected_tags)

    # Ensure distinct results
    structures = structures.distinct()

    # Pagination
    paginator = Paginator(structures, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build base query string without 'page' param for pagination links
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    base_query_string = query_params.urlencode()

    return render(request, 'catalogue.html', {
        'categories': categories,
        'tags': tags,
        'page_obj': page_obj,
        'selected_categories': [int(c) for c in selected_categories],
        'selected_tags': [int(t) for t in selected_tags],
        'search_query': search_query,
        'base_query_string': base_query_string,
    })

# Form for user registration
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Your account has been created successfully!')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return redirect('dummyPage')  # Redirect after successful signup
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Redirect to a page after successful login
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


# def structure_detail_user(request, pk):
#     structure = get_object_or_404(SportStructure, pk=pk)
#     images = structure.images.all()
#     comments = structure.comments.filter(is_approved=True).order_by('-created_at')
#     average_rating = structure.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
#
#     # Rating form
#     if request.method == 'POST' and 'rating_submit' in request.POST:
#         if request.user.is_authenticated:
#             rating_form = RatingFormUser(request.POST)
#             if rating_form.is_valid():
#                 rating, created = Rating.objects.update_or_create(
#                     sport_structure=structure,
#                     user=request.user,
#                     defaults={'rating': rating_form.cleaned_data['rating']}
#                 )
#                 messages.success(request, "Your rating has been saved!")
#                 return redirect('structure_detail_user', pk=pk)
#         else:
#             messages.error(request, "You need to log in to leave a rating.")
#     else:
#         if request.user.is_authenticated:
#             user_rating = Rating.objects.filter(sport_structure=structure, user=request.user).first()
#             initial_rating = user_rating.rating if user_rating else None
#         else:
#             initial_rating = None
#         rating_form = RatingFormUser(initial={'rating': initial_rating})
#
#     # Comment form
#     if request.method == 'POST' and 'comment_submit' in request.POST:
#         if request.user.is_authenticated:
#             comment_form = CommentFormUser(request.POST)
#             if comment_form.is_valid():
#                 Comment.objects.create(
#                     sport_structure=structure,
#                     user=request.user,
#                     text=comment_form.cleaned_data['text']
#                 )
#                 messages.success(request, "Your comment has been submitted for approval!")
#                 return redirect('structure_detail_user', pk=pk)
#         else:
#             messages.error(request, "You need to log in to leave a comment.")
#     else:
#         comment_form = CommentFormUser()
#
#     return render(request, 'structure_detail_user.html', {
#         'structure': structure,
#         'images': images,
#         'average_rating': round(average_rating, 1),
#         'comments': comments,
#         'rating_form': rating_form,
#         'comment_form': comment_form,
#     })


def structure_detail_user(request, pk):
    structure = get_object_or_404(SportStructure, pk=pk)
    images = structure.images.all()
    comments = structure.comments.filter(is_approved=True).order_by('-created_at')
    average_rating = structure.ratings.aggregate(Avg('rating'))['rating__avg'] or 0

    # Rating form
    if request.method == 'POST' and 'rating_submit' in request.POST:
        if request.user.is_authenticated:
            rating_form = RatingFormUser(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.update_or_create(
                    sport_structure=structure,
                    user=request.user,
                    defaults={'rating': rating_form.cleaned_data['rating']}
                )
                messages.success(request, "Your rating has been saved!")
                return redirect('structure_detail_user', pk=pk)
        else:
            messages.error(request, "You need to log in to leave a rating.")
    else:
        if request.user.is_authenticated:
            user_rating = Rating.objects.filter(sport_structure=structure, user=request.user).first()
            initial_rating = user_rating.rating if user_rating else None
        else:
            initial_rating = None
        rating_form = RatingFormUser(initial={'rating': initial_rating})

    # Comment form
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if request.user.is_authenticated:
            comment_form = CommentFormUser(request.POST)
            if comment_form.is_valid():
                Comment.objects.create(
                    sport_structure=structure,
                    user=request.user,
                    text=comment_form.cleaned_data['text']
                )
                messages.success(request, "Your comment has been submitted for approval!")
                return redirect('structure_detail_user', pk=pk)
        else:
            messages.error(request, "You need to log in to leave a comment.")
    else:
        comment_form = CommentFormUser()

    # Pagination for comments
    paginator = Paginator(comments, 5)  # Display 5 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'structure_detail_user.html', {
        'structure': structure,
        'images': images,
        'average_rating': round(average_rating, 1),
        'page_obj': page_obj,  # Pass the page_obj to template
        'rating_form': rating_form,
        'comment_form': comment_form,
    })



#CRUDS

# Structure CRUD
@permission_required('djangoSportApp.view_sportstructure', raise_exception=True)
def structure_list(request):
    structures = SportStructure.objects.all()
    return render(request, 'crud/structure_list.html', {'structures': structures})


@permission_required('djangoSportApp.add_sportstructure', raise_exception=True)
def structure_create(request):
    if request.method == 'POST':
        form = SportStructureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('structure_list')
    else:
        form = SportStructureForm()
    return render(request, 'crud/structure_form.html', {'form': form})


@permission_required('djangoSportApp.view_sportstructure', raise_exception=True)
def structure_detail(request, pk):
    structure = get_object_or_404(SportStructure, pk=pk)
    return render(request, 'crud/structure_detail.html', {'structure': structure})


@permission_required('djangoSportApp.change_sportstructure', raise_exception=True)
def structure_update(request, pk):
    structure = get_object_or_404(SportStructure, pk=pk)
    if request.method == 'POST':
        form = SportStructureForm(request.POST, request.FILES, instance=structure)
        if form.is_valid():
            form.save()
            return redirect('structure_list')
    else:
        form = SportStructureForm(instance=structure)
    return render(request, 'crud/structure_form.html', {'form': form})


@permission_required('djangoSportApp.delete_sportstructure', raise_exception=True)
def structure_delete(request, pk):
    structure = get_object_or_404(SportStructure, pk=pk)
    if request.method == 'POST':
        structure.delete()
        return redirect('structure_list')
    return render(request, 'crud/structure_confirm_delete.html', {'structure': structure})


# Structure Images CRUD

@permission_required('djangoSportApp.view_sportstructureimage', raise_exception=True)
def image_list(request):
    images = SportStructureImage.objects.all()

    # Sort images by sport structure name
    images = images.order_by('sport_structure__name')

    return render(request, 'crud/image_list.html', {'images': images})


@permission_required('djangoSportApp.add_sportstructureimage', raise_exception=True)
def image_create(request):
    if request.method == 'POST':
        form = SportStructureImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = SportStructureImageForm()
    return render(request, 'crud/image_form.html', {'form': form, 'action': 'Create'})


@permission_required('djangoSportApp.change_sportstructureimage', raise_exception=True)
def image_update(request, pk):
    image = get_object_or_404(SportStructureImage, pk=pk)
    if request.method == 'POST':
        form = SportStructureImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = SportStructureImageForm(instance=image)
    return render(request, 'crud/image_form.html', {'form': form, 'action': 'Update'})


@permission_required('djangoSportApp.delete_sportstructureimage', raise_exception=True)
def image_delete(request, pk):
    image = get_object_or_404(SportStructureImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('image_list')
    return render(request, 'crud/image_confirm_delete.html', {'image': image})


# Tags CRUD

@permission_required('djangoSportApp.view_tag', raise_exception=True)
def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'crud/tag_list.html', {'tags': tags})


@permission_required('djangoSportApp.add_tag', raise_exception=True)
def tags_create(request):
    if request.method == 'POST':
        form = TagsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tags_list')
    else:
        form = TagsForm()
    return render(request, 'crud/tag_form.html', {'form': form, 'action': 'Create'})


@permission_required('djangoSportApp.change_tag', raise_exception=True)
def tags_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagsForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tags_list')
    else:
        form = TagsForm(instance=tag)
    return render(request, 'crud/tag_form.html', {'form': form, 'action': 'Update'})


@permission_required('djangoSportApp.delete_tag', raise_exception=True)
def tags_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        return redirect('tags_list')
    return render(request, 'crud/tag_confirm_delete.html', {'tag': tag})


# Category CRUD

@permission_required('djangoSportApp.view_category', raise_exception=True)
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'crud/category_list.html', {'categories': categories})


@permission_required('djangoSportApp.add_category', raise_exception=True)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'crud/category_form.html', {'form': form, 'action': 'Create'})


@permission_required('djangoSportApp.change_category', raise_exception=True)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'crud/category_form.html', {'form': form, 'action': 'Update'})


@permission_required('djangoSportApp.delete_category', raise_exception=True)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'crud/category_confirm_delete.html', {'category': category})


# Comment CRUD

@permission_required('djangoSportApp.view_comment', raise_exception=True)
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'crud/comment_list.html', {'comments': comments})


@permission_required('djangoSportApp.add_comment', raise_exception=True)
def comment_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comments_list')
    else:
        form = CommentForm()
    return render(request, 'crud/comment_form.html', {'form': form, 'action': 'Create'})


@permission_required('djangoSportApp.change_comment', raise_exception=True)
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comments_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'crud/comment_form.html', {'form': form, 'action': 'Update'})


@permission_required('djangoSportApp.delete_comment', raise_exception=True)
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('comments_list')
    return render(request, 'crud/comment_confirm_delete.html', {'comment': comment})


# Rating CRUD

@permission_required('djangoSportApp.view_rating', raise_exception=True)
def rating_list(request):
    ratings = Rating.objects.all()

    ratings = ratings.order_by('sport_structure__name')

    return render(request, 'crud/rating_list.html', {'ratings': ratings})


@permission_required('djangoSportApp.add_rating', raise_exception=True)
def rating_create(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ratings_list')
    else:
        form = RatingForm()
    return render(request, 'crud/rating_form.html', {'form': form, 'action': 'Create'})


@permission_required('djangoSportApp.change_rating', raise_exception=True)
def rating_update(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('ratings_list')
    else:
        form = RatingForm(instance=rating)
    return render(request, 'crud/rating_form.html', {'form': form, 'action': 'Update'})


@permission_required('djangoSportApp.delete_rating', raise_exception=True)
def rating_delete(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if request.method == 'POST':
        rating.delete()
        return redirect('ratings_list')
    return render(request, 'crud/rating_confirm_delete.html', {'rating': rating})


# User CRUD

@permission_required('auth.view_user', raise_exception=True)
def user_list(request):
    users = User.objects.all()
    return render(request, 'crud/user_list.html', {'users': users})


# def user_create(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm()
#     return render(request, 'crud/user_form.html', {'form': form, 'action': 'Create'})
#
#
# def user_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'crud/user_form.html', {'form': form, 'action': 'Update'})
#
#
# def user_delete(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'crud/user_confirm_delete.html', {'user': user})

@permission_required('auth.add_user', raise_exception=True)
def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserCreationForm()
    return render(request, 'crud/user_form.html', {'form': form, 'title': 'Create User', 'action': 'Create'})


# def user_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = CustomUserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserChangeForm(instance=user)
#     return render(request, 'crud/user_form.html', {'form': form, 'title': f'Edit User: {user.username}',
#                                                    'action': 'Update'})

@permission_required('auth.change_user', raise_exception=True)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'crud/user_form.html', {'form': form, 'title': f'Edit User: {user.username}',
                                                   'action': 'Update'})


@permission_required('auth.delete_user', raise_exception=True)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    return render(request, 'crud/user_confirm_delete.html', {'user': user})


# User permission management

@permission_required('auth.change_user', raise_exception=True)
def user_permissions(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserPermissionsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserPermissionsForm(instance=user)
    return render(request, 'crud/user_permission_form.html', {'form': form, 'user': user, 'action': 'Update'})


@permission_required('auth.change_user', raise_exception=True)
def user_password_change(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = AdminPasswordChangeForm(user)

    return render(request, 'crud/user_passwd_reset.html', {'form': form, 'user': user})