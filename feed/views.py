from django.shortcuts import render
from actions.models import Action
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView, RedirectView)
from feed.models import UserPost
from django.urls import reverse_lazy
from actions.utils import create_action


# class UserFeedView(ListView):
#     template_name = 'feed/user_feed.html'
#     context_object_name = 'actions'
#
#     def get_queryset(self):
#         return Action.objects.all()  # .exclude(user=self.request.user)


class CreatePostView(CreateView):
    model = UserPost
    fields = ['post_body', 'image']

    def get_context_data(self, **kwargs):
        kwargs['actions'] = Action.objects.all()
        return super(CreatePostView, self).get_context_data(**kwargs)

    def get_success_url(self):
        post = UserPost.objects.get(pk=self.object.pk)
        create_action(self.request.user, 'posted', post)
        return reverse_lazy('feed:userfeed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostDetailView(DetailView):
    model = UserPost
    fields = ['post_body', 'image']
    context_object_name = 'post'
    template_name = 'feed/post_detail.html'


    # # def dashboard(request):
    #     # Display all actions by default
    #     actions = Action.objects.all().exclude(user=request.user)
    #     following_ids = request.user.following.values_list('id', flat=True)
    #     if following_ids:
    #         # If user is following others, retrieve only their actions
    #         actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related(
    # 'target')
    #     actions = actions[:10]
    #
    #     return render(request, 'account/dashboard.html', {'section': 'dashboard',
    #                                                       'actions': actions})
