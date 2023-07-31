from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm
from .models import User, Listing, Bid, Comment
from . import utils

def index(request):
    listings = Listing.objects.all()
    bids = Bid.objects.all()

    top_bids = []
    for listing in listings:
        top_bids.append(utils.get_highest_bid(listing))

    list_url = [reverse("listing", args=[x.id]) for x in listings]
    print(list_url)
    list_w_urls = list(zip(listings, list_url, top_bids))
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

def listing(request, id):
    listing = Listing.objects.get(id=id)
    bids = Bid.objects.filter(listing= listing)
    comments = Comment.objects.filter(listing=listing)
    maxbid, ambids = utils.get_highest_bid(listing), len(Bid.objects.filter(listing= listing))
    bidding_url = reverse('makebid', args=[id])

    return render(request, "auctions/listingspage.html",
                  {"listing": listing, "maxbids": maxbid,"ambids":ambids,
                  "bidding_url" : bidding_url   ,"comments": comments, "message": False})

@login_required
def addlisting(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)  # Get the unsaved instance
            listing.poster = request.user  # Assign the current user to poster
            listing.save()  # Now save it
            form.save_m2m()
            return redirect('index')  # Optionally redirect the user after successful save
    else:
        form = ListingForm()

    return render(request, 'auctions/addlisting.html', {'form': form})

@login_required
def makebid(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        print(request.POST)

        maxbid = utils.get_highest_bid(listing)
        amount = request.POST["amount"]
        print("amount digit", amount.isdigit())
        if amount.isdigit():
            valid = int(amount) > int(maxbid.amount)
        else:
            valid = False
        form = BidForm(request.POST)
        if form.is_valid() and valid:
            bid = form.save(commit=False)
            bid.poster = request.user
            listing = Listing.objects.get(id=id)
            bid.listing = listing
            form.save()
        else:
            ambids = len(Bid.objects.all())
            bidding_url = reverse('makebid', args=[id])
            comments = Comment.objects.filter(listing=listing)
            return render(request, 'auctions/listingspage.html', context = {"listing": listing, "maxbids": maxbid,"ambids":ambids,
                  "bidding_url" : bidding_url   ,"comments": comments, "message": True})
        return redirect('listing', id)