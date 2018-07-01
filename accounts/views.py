from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile, Contact
from .forms import UserForm, ProfileForm
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from actions.utils import create_action
from feed.models import UserPost


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserListView(generic.ListView):
    template_name = 'user/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserDetail(generic.DetailView):
    context_object_name = "person"
    model = User
    template_name = 'registration/user_detail.html'

    # pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        try:
            context['profile'] = Profile.objects.filter(user=User.objects.get(pk=pk))
            context['user_posts'] = UserPost.objects.filter(author=User.objects.get(pk=pk))
        except ObjectDoesNotExist:
            pass
        return context


class UserUpdate(View):
    template_name = 'registration/profile.html'
    template_name1 = 'hortihome/base.html'
    form_class_user = UserForm
    form_class_profile = ProfileForm

    def get(self, request, pk):

        try:
            user = User.objects.get(pk=pk)
            form = self.form_class_user(instance=user)
            form2 = self.form_class_profile(instance=user.profile)
        except ObjectDoesNotExist:
            form2 = self.form_class_profile()

        return render(request, self.template_name, {'form': form, 'form2': form2})

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = self.form_class_user(data=request.POST, instance=request.user)
        try:
            form2 = self.form_class_profile(data=request.POST, files=request.FILES, instance=request.user.profile)
            if form2.is_valid():
                user.profile = form2.save(commit=False)
                user.profile.save()
        except ObjectDoesNotExist:
            #Creates new instance of profile to save user profile data
            form2 = self.form_class_profile(data=request.POST, files=request.FILES)
            if form2.is_valid():
                user.profile = form2.save(commit=False)
                user.profile.save()
            pass

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
            except:
                pass

        return render(request, self.template_name1)


class UserFollow(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        celeb = get_object_or_404(User, pk=pk)
        url_ = celeb.get_absolute_url()

        if self.request.user.is_authenticated:
            if self.request.user in celeb.followers.all():
                Contact.objects.filter(user_from=self.request.user,
                                       user_to=celeb).delete()
            else:
                Contact.objects.get_or_create(user_from=self.request.user,
                                              user_to=celeb)
                create_action(self.request.user, 'is now following', celeb)
        return url_

