from actions.models import Action
from django.views.generic import (DetailView, CreateView, UpdateView)
from feed.models import UserPost
from django.urls import reverse_lazy
from actions.utils import create_action
import redis
from django.conf import settings
from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.http.response import HttpResponse
import json
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

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


class PostDetailView(AjaxResponseMixin, UpdateView):
    model = UserPost
    # fields = ['post_body', 'image']
    context_object_name = 'post'
    template_name = 'feed/post_detail.html'
    form_class = CommentForm

    def get_initial(self):
        initial_data = super(PostDetailView, self).get_initial()
        obj = self.get_object()
        print(obj.get_content_type)
        initial_data.update({
            "content_type": obj.get_content_type,
            "object_id": obj.id
        })
        return initial_data

    def get_context_data(self, **kwargs):
        # comment_form = CommentForm
        context = super(PostDetailView, self).get_context_data(**kwargs)
        kwargs['form_comment'] = context['form']#comment_form
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
        return reverse_lazy('feed:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        c_type = form.cleaned_data.get("content_type")
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(self.request.POST.get("parent_id"))
        except:
            parent_id = None
        print(parent_id)

        if parent_id:
            parent_qs = Comment.objects.filter(pk=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=self.request.user,
            content_type=c_type,
            object_id=obj_id,
            content=content_data,
            parent = parent_obj,
        )
        return super(PostDetailView, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid form")

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

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

