from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class UserPost(models.Model):
    author = models.ForeignKey(User, related_name='userpost', null=True, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    post_body = models.TextField(blank=True, null=True, default='Whats happening?')
    image = models.ImageField(upload_to='post_pics', blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    class Meta:
        ordering = ['-post_date']

    def publish(self):
        self.save()

    def get_absolute_url(self):
         return reverse_lazy('feed:post_detail', kwargs={'pk': self.id})

    # def likes_as_flat_user_id_list(self):
    #     return self.likes.values_list('id', flat=True)

    def __str__(self):
        return self.post_body

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
