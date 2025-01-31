from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import User, Listings, Bids, Comments, Watchlist, Winner


def index(request):
    listings = Listings.objects.exclude(active=False).all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


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


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST.get("category", "")
        image_url = request.POST.get("image_url", "").strip()

        if not image_url:
            image_url = "https://img.favpng.com/22/10/12/question-mark-desktop-wallpaper-grey-computer-icons-png-favpng-FTNv8p4eRd8kVubahAEhbJXCc.jpg"
        else:
            if not is_string_an_url(image_url):
                return render(request, "auctions/create.html", {
                    "message": "Invalid image URL. Please provide a valid URL that points to an image."
                })
            
        try:
            price = float(price)
        except ValueError:
            return render(request, "auctions/create.html", {
                "message": "Invalid price format."
            })
        
        if price >= 100000:
            return render(request, "auctions/create.html", {
                "message": "Invalid price. Over $100 000.00"
            })
        
        new_listing = Listings(
            title=title,
            description=description,
            price=price,
            current_price=price,
            category=category,
            image_url=image_url,
            owner=request.user  # Set the owner to the current logged-in user
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create.html")


def listings(request, id):
    listing = Listings.objects.get(pk=id)
    bids = Bids.objects.filter(listing=listing)
    comments = Comments.objects.filter(listing=listing)
    winner = Winner.objects.filter(listing=listing).first()

    if request.user.is_authenticated:
        watchlist_item = Watchlist.objects.filter(user=request.user, listing=listing).first()
    else:
        watchlist_item = False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": bool(watchlist_item),
        "bids" : bids,
        "comments" : comments,
        "winner" : winner
    })


@login_required
def toggle_watchlist(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    watchlist_item = Watchlist.objects.filter(user=user, listing=listing).first()
    if watchlist_item:
        watchlist_item.delete()
    else:
        Watchlist.objects.create(user=user, listing=listing)

    return HttpResponseRedirect(reverse('listings', args=(id,)))


@login_required
def watchlist(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=user)
    items = [item.listing for item in watchlists]
    return render(request, "auctions/watchlist.html", {
            "items": items
        })


@login_required
def bid(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listings.objects.filter(pk=id).first()
        comments = Comments.objects.filter(listing=listing)
        last_bid = Bids.objects.filter(listing=listing).last()

        try:
            bid = float(request.POST["bid"])
        except ValueError:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "in_watchlist": bool(Watchlist.objects.filter(user=request.user, listing=listing).first()),
                "bids": Bids.objects.filter(listing=listing),
                "comments" : comments,
                "message": "Invalid bid amount."
            })

        if last_bid:
            if bid > last_bid.bid_price and bid > listing.price:
                new_bid = Bids.objects.create(user=user, listing=listing, bid_price=bid)
                new_bid.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "in_watchlist": bool(Watchlist.objects.filter(user=request.user, listing=listing).first()),
                    "bids": Bids.objects.filter(listing=listing),
                    "comments" : comments,
                    "message": "Invalid bid. Your bid must be greater than the last bid."
                })
        else:
            if bid >= listing.price:
                new_bid = Bids.objects.create(user=user, listing=listing, bid_price=bid)
                new_bid.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "in_watchlist": bool(Watchlist.objects.filter(user=request.user, listing=listing).first()),
                    "bids": Bids.objects.filter(listing=listing),
                    "comments" : comments,
                    "message": "Invalid bid. Your bid must be at least as large as the starting bid."
                })
        
        listing.current_price  = bid
        listing.save()
        return HttpResponseRedirect(reverse('listings', args=(id,)))

    return HttpResponseRedirect(reverse('listings', args=(id,)))

@login_required
def comment(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listings.objects.get(pk=id)
        comment = request.POST["comment"].strip()

        new_comment = Comments.objects.create(writer=user, listing=listing, comment=comment)
        new_comment.save()

        return HttpResponseRedirect(reverse('listings', args=(id,)))

    return HttpResponseRedirect(reverse('listings', args=(id,)))


@login_required
def close(request, id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=id)
        last_bid = Bids.objects.filter(listing=listing).last()
        winner = last_bid.user

        new_winner = Winner.objects.create(user=winner, listing=listing, bid=last_bid)
        new_winner.save()

        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('listings', args=(id,)))


def categories(request):
    CATEGORY_CHOICES = [
        "Clothing, Shoes & Accessories",
        "Sporting Goods",
        "Toys & Hobbies",
        "Home & Garden",
        "Jewelry & Watches",
        "Health & Beauty",
        "Business",
        "Electronics",
        "Collectibles & Art",
        "Books, Movies & Music",
        "Other",
    ]

    return render(request, "auctions/categories.html", {
        "categories": CATEGORY_CHOICES,
    })


def category(request, category):
    listings = Listings.objects.filter(category=category, active=True).all()
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category" : category
    })

def is_string_an_url(url_string: str) -> bool:
    validate_url = URLValidator()
    try:
        validate_url(url_string)
    except ValidationError:
        return False
    return True
