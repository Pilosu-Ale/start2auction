from django.shortcuts import render, HttpResponseRedirect
from .forms import FormRegistration
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def registration_view(request):
    if request.method == "POST":
        form = FormRegistration(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = FormRegistration()
    context = {"form": form}
    return render(request, "registration/registration.html", context)
