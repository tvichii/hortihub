from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile, Contact
from .forms import UserForm, ProfileForm
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from actions.utils import create_action


# from actions.utils import create_action

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
    context_object_name = "prof"
    model = User
    template_name = 'registration/user_detail.html'

    # pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(UserDetail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        try:
            context['profile'] = Profile.objects.filter(user=User.objects.get(pk=pk))
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
        form2 = self.form_class_profile(data=request.POST, files=request.FILES, instance=request.user.profile)

        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.profile = form2.save(commit=False)
            user.save()
            user.profile.save()

        return render(request, self.template_name1)


# @ajax_required
# @require_POST
# def user_follow(request):
#     user_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if user_id and action:
#         try:
#             user = User.objects.get(id=user_id)
#             if action == 'follow':
#                 Contact.objects.get_or_create(user_from=request.user,
#                                               user_to=user)
#                 create_action(request.user, 'is following', user)
#             else:
#                 Contact.objects.filter(user_from=request.user,
#                                        user_to=user).delete()
#             return JsonResponse({'status':'ok'})
#         except User.DoesNotExist:
#             return JsonResponse({'status':'ko'})
#     return JsonResponse({'status':'ko'})

# @ajax_required
# @require_POST
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
                create_action(self.request.user, 'is following', celeb)
        return url_


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
#
#
# class UserFollowAPIToggle(APIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, pk=None, format=None):
#
#         pk = self.kwargs.get('pk')
#
#         celeb = get_object_or_404(User, pk=pk)
#         # url_ = celeb.get_absolute_url()
#         updated = False
#         followed = False
#         if self.request.user.is_authenticated:
#             if self.request.user in celeb.followers.all():
#                 Contact.objects.filter(user_from=self.request.user,
#                                        user_to=celeb).delete()
#                 followed = "False_y"
#             else:
#                 followed = True
#                 Contact.objects.get_or_create(user_from=self.request.user,
#                                               user_to=celeb)
#             updated = True
#         data = {
#             "updated": updated,
#             "followed": followed
#         }
#         return Response(data)

        # obj = get_object_or_404(Post, slug=slug)
        # url_ = obj.get_absolute_url()
        # user = self.request.user
        # updated = False
        # liked = False
        # if user.is_authenticated():
        #     if user in obj.likes.all():
        #         liked = False
        #         obj.likes.remove(user)
        #     else:
        #
        #
        #         obj.likes.add(user)
        #     updated = True
        # data = {
        #     "updated": updated,
        #     "liked": liked
        # }
        # return Response(data)


        # def post(self, request, pk):
        #     # user = User.objects.get(pk=pk)
        #     user_id = request.POST.get('id')
        #     print(user_id)
        #     action = request.POST.get('action')
        #
        #     if user_id and action:
        #         try:
        #             user = User.objects.get(id=user_id)
        #             if action == 'follow':
        #                 Contact.objects.get_or_create(user_from=request.user,
        #                                               user_to=user)
        #                 # create_action(request.user, 'is following', user)
        #             else:
        #                 Contact.objects.filter(user_from=request.user,
        #                                        user_to=user).delete()
        #             return JsonResponse({'status': 'ok'})
        #         except User.DoesNotExist:
        #             return JsonResponse({'status': 'ko'})
        #     return JsonResponse({'status': 'ko'})
