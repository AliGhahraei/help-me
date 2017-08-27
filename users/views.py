from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import Filter
from users.models import Profile

from .forms import RegisterForm

# Create your views here.
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
            profile = Profile(user=user)
            user = authenticate(username=user.username, password=request.POST['password'])

            domain_name = form.cleaned_data['email'].split('@')[1]
            if not Filter.objects.filter(name=domain_name).exists():
                filter_ = Filter(name=domain_name)
                filter_.save()
            else:
                filter_ = Filter.objects.get(name=domain_name)

            profile.filter = filter_
            profile.save()

            login(request, user)
            return redirect('/')

        return redirect('/adios-amigow')
