from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q
import users.models as models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

class ServiceList(ListView, LoginRequiredMixin):

    context_object_name = 'service_list'
    template_name = 'users/services.html'

    def get_queryset(self):
        profile = models.Profile.objects.get(user__id=self.request.user.id)
        filters = profile.filters.all()
        communities = models.Community.objects.none()
        services = models.Service.objects.none()
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

def signup(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(False)
            user.set_password(user.password)
            user.save()
            profile = models.Profile(user=user)
            user = authenticate(username=user.username, password=request.POST['password'])

            domain_name = form.cleaned_data['email'].split('@')[1]
            if not models.Filter.objects.filter(name=domain_name).exists():
                filter_ = models.Filter(name=domain_name)
                filter_.save()
            else:
                filter_ = models.Filter.objects.get(name=domain_name)

            profile.filter = filter_
            profile.save()

            login(request, user)
            return redirect('/')

        return redirect('/adios-amigow')
