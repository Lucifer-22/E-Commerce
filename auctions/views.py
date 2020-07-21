from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import listing_form

from .models import User, Bid, Listing, Comment, Cart, Watchlist, CATEGORY_CHOICES


def index(request):
    items = Listing.objects.filter(availability = True)
    context = {
        'items': items,
        'title': "Active Listing",
        'categories': CATEGORY_CHOICES
    }
    return render(request, "auctions/index.html", context)


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

def create(request):
    if request.method == "POST":
        form = listing_form(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                'form': form,
                'message': "Please try entering again."
            }
            return render(request, "auctions/create.html", context)

    else:
        form = listing_form()
        context = {
            'form':form,
            'message': "Enter Entry"
        }
        return render(request, "auctions/create.html", context)

def listing(request, title):
    data = Listing.objects.get(title = title)
    comments = Comment.objects.filter(items = data)
    bid =  Bid.objects.filter(items = data)
    try:
        watching = False
        owner = False
        highest_bidder = False
        if (data.availability == False) and (request.user == data.winner):
            highest_bidder = True
        if request.user == data.seller:
            owner = True
        for item in Watchlist.objects.filter(user = request.user):
            if item.items == data:
                watching = True
            else:
                watching = False
        context = {
            'item': data,
            'watching': watching,
            'comments': comments,
            'owner': owner,
            'highest_bidder': highest_bidder
        }
        return render(request, "auctions/product.html", context)
        
    except:
        context = {
        'item': data,
        'watching': False,
        'comments': comments,
        'owner': False,
        'highest_bidder': False
        }
        return render(request, "auctions/product.html", context)

    
def watchlist(request):
    watchItems = Watchlist.objects.filter(user = request.user)
    watching_Lists = []
    for i in range(len(watchItems)):
        tmp = Listing.objects.get(title = watchItems[i].items)
        watching_Lists.append(tmp)
    context = {
        'watching_Lists': watching_Lists,
        'count': len(watching_Lists)
    }
    return render(request, "auctions/watchlist.html", context)


def addToWatchlist(request, title):
    item = Listing.objects.get(title = title)
    user = User.objects.get(username = request.user)
    data = Watchlist(user = user, items = item)
    data.save()
    return HttpResponseRedirect(reverse("watchlist"))

def removeFromWatchlist(request, title):
    item = Listing.objects.get(title = title)
    user = User.objects.filter(username = request.user)[0]
    data = Watchlist.objects.filter(items = item, user = user)
    data.delete()
    return HttpResponseRedirect(reverse("watchlist"))

def comment(request, title):
    item = Listing.objects.get(title = title)
    user = User.objects.get(username = request.user)
    if request.method == "POST":
        comment = request.POST["comment"]
        data = Comment(user = user, items = item, comment = comment)
        data.save()
        return HttpResponseRedirect(reverse(listing, kwargs={
                'title': title
                }))
    else:
        return HttpResponseRedirect(reverse("index"))

def bid(request, title):
    item = Listing.objects.get(title = title, availability = True)
    current_bid = item.price
    user = User.objects.get(username = request.user)
    if request.method == "POST":
        bid_amount = request.POST["bid"]
        if float(current_bid) <= float(bid_amount):
            item.price = bid_amount
            item.winner = request.user
            item.save()
            data = Bid(items = item, user = request.user, bid = bid_amount)
            data.save()     
            context = {
                'title': title,
                'bid': bid_amount,
                'message': "Successful"
            }
            return render(request, "auctions/bid.html", context)
        else:
            context = {
                'error_message': "You cannot bid less than current price!."
            }
            return render(request, "auctions/bid.html", context)
    else:
        return HttpResponseRedirect(reverse("index"))

def closebid(request, title):
    item = Listing.objects.get(title = title)
    bid =  Bid.objects.filter(items = item)
    if request.user == item.seller:
        item.availability = False
        item.save()
        cart = Cart(user = item.winner, items = item)
        cart.save()
        return HttpResponseRedirect(reverse("index"))

def categories(request):
    context = {
        'categories': CATEGORY_CHOICES
    }
    return render(request, "auctions/categories.html", context)

def category(request, category):
    data = Listing.objects.filter(category = category, availability = True)
    if len(data) != 0:
        context = {
            'items': data,
            'title': category
        }
        return render(request, "auctions/index.html", context)
    else:
        context = {
            'title': "EMPTY",
        }
        return render(request, "auctions/index.html", context)

def cart(request):
    data = Cart.objects.filter(user = request.user)
    query = []
    for i in range(len(data)):
        tmp = Listing.objects.get(title = data[i].items)
        query.append(tmp)
    context = {
        'items': query,
        'count': len(query)
    }
    return render(request, "auctions/cart.html", context)
    
 