from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q
import users.models as models
from django.contrib.auth.mixins import LoginRequiredMixin

class ServiceList(ListView, LoginRequiredMixin):

    context_object_name = 'service_list'
    template_name = 'users/services.html'

    def get_queryset(self):
        profile = models.Profile.objects.get(user__id=self.request.user.id)
        filters = profile.filters.all()
        communities = models.Community.none()
        services = models.Service.none()
        for filter_ in filters:
            communities.union(models.Community.filter(filter=filter_.id))
        if self.request.GET.get('query'):
            services.union(models.Service.filter(Q(name__icontains=self.request.request.GET.get('query'))))
        else:
            for community in communities:
                services.union(models.Service.filter(community=community.id))
        return services


class ProfileView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs)
        profile_id = kwargs.get('profile_id')
        if profile_id:
            profile = models.Profile.get(pk=profile_id)
        else:
            profile = models.Profile.get(user=self.request.user)
        context['profile'] = profile
        comments = models.Comment.filter(target=profile)
        context['comments'] = comments
