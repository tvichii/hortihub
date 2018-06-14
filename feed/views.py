from django.shortcuts import render
from django.views import generic
from actions.models import Action

class UserFeedView(generic.ListView):
    template_name = 'feed/user_feed.html'
    context_object_name = 'actions'

    def get_queryset(self):
        return Action.objects.all() #.exclude(user=self.request.user)


# def dashboard(request):
#     # Display all actions by default
#     actions = Action.objects.all().exclude(user=request.user)
#     following_ids = request.user.following.values_list('id', flat=True)
#     if following_ids:
#         # If user is following others, retrieve only their actions
#         actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
#     actions = actions[:10]
#
#     return render(request, 'account/dashboard.html', {'section': 'dashboard',
#                                                       'actions': actions})
