from django.shortcuts import render
from django.views.generic import ListView
from notifications.models import Notification

# class NotificationListView(ListView):
#     template_name = 'notifications/not_list.html'
#     context_object_name = 'not_all'
#
#     def get_queryset(self):
#         return Notification.objects.all()  # .exclude(user=self.request.user)
