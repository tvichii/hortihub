from django.shortcuts import render
from actions.models import Action
# from django.views.mixins.ajaxformresponse import AjaxFormResponseMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView, RedirectView)
from feed.models import UserPost
from django.urls import reverse_lazy
from actions.utils import create_action
# from notifications.utils import create_notification
import redis
from django.conf import settings
from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.http.response import HttpResponse
import json
from comments.models import Comment

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


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
        # create_notification(self.request.user, 'posted', post)
        return reverse_lazy('feed:userfeed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostDetailView(AjaxResponseMixin, DetailView):
    model = UserPost
    fields = ['post_body', 'image']
    context_object_name = 'post'
    template_name = 'feed/post_detail.html'

    def get_context_data(self, **kwargs):
        post = UserPost.objects.filter(pk=self.kwargs.get('pk')).first()
        comments = Comment.objects.filter_by_instance(post)
        kwargs['comments'] = comments
        try:
            total_views = r.incr('userpost:{}:views'.format(self.object.pk))
            kwargs['total_views'] = total_views
        except (redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError):
            pass

        return super(PostDetailView, self).get_context_data(**kwargs)

    def get_success_url(self):
        try:
            total_views = r.incr('userpost:{}:views'.format(self.object.pk))
        except (redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError):
            pass

    # def post_ajax(self, request, *args, **kwargs):
    #     data = request.POST.items()  # form data
    #     ctx = {'hi': 'hello'}
    #     return self.render_json_response(ctx)

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        liked = False

        if request.user in obj.likes.all():
            liked = False
            obj.likes.remove(request.user)
        else:
            liked = True
            obj.likes.add(request.user)

        response_data = {
            "liked": liked,
            "likes": str(obj.likes.count()),
        }
        # print(response_data["likes"])
        # if obj.likes:
        #     response_data = {'result': "enabled"}
        # else:
        #     response_data = {'result': "disabled"}

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

        # class PostLikeView(AjaxFormResponseMixin, UpdateView):
        #     # form_class = UpdateAuthorForm
        #
        #     def get_object(self, queryset=None):
        #         return get_object_or_json404(Author, pk=self.kwargs['pk'])
        #
        #     def get_context_data(self, context):
        #         context['success'] = True
        #         return context

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
