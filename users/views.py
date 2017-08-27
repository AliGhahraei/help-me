from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q
import users.models as models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, ServiceForm, CommentForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

class ServiceList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'next'
    context_object_name = 'service_list'
    template_name = 'users/services.html'

    def get_queryset(self):
        profile = models.Profile.objects.get(user__id=self.request.user.id)
        filters = profile.filters.all()
        communities = models.Community.objects.none()
        services = models.Service.objects.none()
        for filter_ in filters:
            communities.union(models.Community.filter(filter=filter_.id))
        queries = self.request.GET.get('query')
        queries = queries.split(' ') if queries is not None else None
        if queries:
            for query in queries:
                for community in communities:
                    services.union(models.Service.filter(Q(name__icontains=query) | Q(tags__icontains=query) | Q(community=community)))
        else:
            for community in communities:
                services.union(models.Service.filter(community=community))
        return services


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = kwargs.get('profile_id')
        if profile_id:
            profile = models.Profile.get(pk=profile_id)
        else:
            profile = models.Profile.get(user=self.request.user)
        context['profile'] = profile
        comments = models.Comment.filter(target=profile)
        context['comments'] = comments

class ServiceView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        service = models.Service.objects.get(pk=kwargs['service_id'])
        comments = models.ServiceComment.objects.filter(target=service)
        context['service'] = service
        context['comments'] = comments
        return context


class ServiceCreate(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'next'

    template_name = 'users/new_service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceForm()
        return context

    def post(self, **kwargs):
        form = ServiceForm(self.request.POST)
        if form.is_valid():
            service = form.save(False)
            service.owner = models.Profile.objects.get(user=self.request.user)
            service.community = kwargs['community_id']
            service.save()
        return redirect('services_list')

class CommentForm(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(False)
            comment.author = models.Profile.objects.get(user=self.request.user)
            comment.target = models.Profile.objects.get(id=kwargs['profile_id'])
            comment.save()
        return redirect('/')


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
