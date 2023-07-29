from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing


def index(request):
    listings = Listing.objects.all()
    list_url = [reverse("listing", args=[x.title]) for x in listings]
    list_w_urls = list(zip(listings, list_url))
    return render(request, "auctions/index.html", context={'obs' : list_w_urls})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, title):
    pass

@login_required
def addlisting(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        print(f"in addlisting,{form.is_valid()}")
        print(form.errors)
        if form.is_valid():
            print("inside")
            listing = form.save(commit=False)  # Get the unsaved instance
            listing.poster = request.user  # Assign the current user to poster
            listing.save()  # Now save it
            return redirect('index')  # Optionally redirect the user after successful save
    else:
        form = ListingForm()
    return render(request, 'auctions/addlisting.html', {'form': form})