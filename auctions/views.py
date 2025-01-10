from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ListingForm, BidForm, CloseForm, CommentForm
from .models import User, Listing, Bid, Watchlist, Comment, categories
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    listings = Listing.objects.filter(closed_auction="No")
    most_recent = listings.order_by('-created_on')[:5]
    w_list = []

    if not request.user.is_authenticated:
        w_list = None
    else:
        watchlist = Watchlist.objects.filter(user=request.user)

        for item in watchlist:
            w_list.append(item)

    context = {
        "listings": listings,
        "w_list": w_list,
        "recent": most_recent
    }

    return render(request, "auctions/index.html", {"context": context})


def closed_listing(request):
    listings = Listing.objects.filter(closed_auction="Yes")
    w_list = []

    if not request.user.is_authenticated:
        w_list = None
    else:
        watchlist = Watchlist.objects.filter(user=request.user)

        for item in watchlist:
            w_list.append(item)

    if not listings:
        listings = None

    context = {
        "listings": listings,
        "w_list": w_list,
        "category": category
    }

    return render(request, "auctions/closedlisting.html", {"context": context})


def loginview(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # POST route at login
        # Check if authentication unsuccessful
        if user is None:
            messages.error(request, "Login unsuccessful")
            return render(request, "auctions/login.html")
        else:
            # Successful
            login(request, user)
            messages.info(request, "Logged in successfully")
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        # Render form on GET
        return render(request, "auctions/login.html")


def logoutview(request):
    logout(request)
    messages.warning(request, "Logged out successfully")
    return HttpResponseRedirect(reverse("auctions:login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        messages.info(request, "Logged in successfully.")
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def not_found(request):
    return render(request, 'auctions/error.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ListingForm
from .models import Listing, User

@login_required
def add_listing(request):
    user = request.user

    if request.method == "GET":
        form = ListingForm()
        return render(request, "auctions/addlisting.html", {"form": form})

    else:
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                newlisting = form.save(commit=False)
                newlisting.listing_owner = user
                newlisting.save()

                messages.success(request, "Your listing has been saved.")
                return redirect("auctions:index")

            except Exception as e:
                messages.error(request, f"There was an error saving your listing: {e}")
                return render(request, "auctions/addlisting.html", {"form": form})

        else:
            messages.error(request, "There was an error with the form. Please correct it.")
            return render(request, "auctions/addlisting.html", {"form": form})


@login_required
def view_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(listing=listing)
    list_item = Watchlist.objects.filter(
        user=request.user, listing__id=listing_id)
    closed_status = None

    all_bids = []  # Set an empty bid list to get all bids if any exist
    # Set highest bid to 0 in case there are no bids
    highest_bid = listing.starting_price
    highest_bidder = ''
    winner = ''

    if bids:
        bid_list = list(bids)  # Convert Queryset to a list

        for index in bid_list:
            all_bids.append(index)
        # Get the highest bid from all_bids
        highest_bid = all_bids[-1].bid_amount
        # Get the highest bidder from all_bids
        highest_bidder = all_bids[-1].user
        listing.starting_price = highest_bid

    else:
        highest_bid  # Else highest bid is 0
        highest_bidder  # Else highest bid is blank

    if listing.closed_auction == "Yes":
        closed_status = "closed"

    if request.method == "GET":
        bid_form = BidForm()
        close_form = CloseForm()
        comment_form = CommentForm()
        close_form.initial['closed_auction'] = listing.closed_auction

        if closed_status == "closed":
            winner = highest_bidder

        context = {
            "listing": listing,
            "item": list_item,
            "bids": bids,
            "bid_form": bid_form,
            "close_form": close_form,
            "comment_form": comment_form,
            "comments": comments,
            "highest_bid": highest_bid,
            "highest_bidder": highest_bidder,
            "winner": winner,
            "closed_status": closed_status
        }

        return render(request, "auctions/viewlisting.html", {"context": context})

    else:  # On POST, allow a user to bid on an item
        try:
            form_type = request.POST.get("form_type")
            form = None

            if form_type == "form_bid": # from hidden value field in viewlisting.html
                form = BidForm(request.POST)

            if form_type == "form_close": # from hidden value field in viewlisting.html
                form = CloseForm(request.POST, instance=listing)

            if form_type == "form_comment": # from hidden value field in viewlisting.html
                form = CommentForm(request.POST, instance=listing)

            if form and form.is_valid():
                if form_type == "form_bid":
                    bid_amount = request.POST.get("bid_amount")
                    bid_value = form.cleaned_data['bid_amount']

                    if bid_value <= highest_bid:
                        raise ValueError
                    Bid.objects.create(
                        listing=listing, user=request.user, bid_amount=bid_value)

                    # Update the current price to the latest bid price if the form is valid
                    bid_price = Listing.objects.filter(
                        pk=listing_id).update(current_price=bid_value)
                    messages.info(request, "Your bid was accepted.")

                if form_type == "form_close":
                    closed_auction = request.POST.get("closed_auction")
                    messages.info(request, "Listing closed.")
                    form.save()

                if form_type == "form_comment":
                    comment = request.POST.get("content")
                    Comment.objects.create(
                        listing=listing, user=request.user, content=comment)
                    messages.success(request, "Your comment has been posted.")

                return HttpResponseRedirect(listing.get_absolute_url())

            return redirect("auctions:index")

        except ValueError:
            bid_amount = request.POST.get("bid_amount")
            close_form = CloseForm()

            context = {
                "listing": listing,
                "item": list_item,
                "bids": bids,
                "form": form,
                "highest_bidder": highest_bidder,
                "highest_bid": highest_bid
            }

            messages.error(
                request, f"Your bid of ${bid_amount} must be higher that the last ${highest_bid} bid.")
            return render(request, "auctions/viewlisting.html", {"context": context})


@login_required
def watchlist_switch(request, listing_id):
    listing = Listing.objects.get(id=int(listing_id))

    try:  # Check if the listing item exists in the user's watchlist
        watchlist_entry = Watchlist.objects.all().filter(
            listing__id=listing_id, user__id=request.user.id)
    except:  # else return None
        watchlist_entry = None

    if watchlist_entry:  # If it exists, give the option to remove
        watchlist_entry.delete()
        messages.success(request, f"Item removed from watchlist.")
        return HttpResponseRedirect(listing.get_absolute_url())
    else:  # If it doesn't, create a new wishlist item
        new_watchlist_entry = Watchlist(user=request.user, listing=listing)
        new_watchlist_entry.save()
        messages.success(request, f"Item added to watchlist.")
        return HttpResponseRedirect(listing.get_absolute_url())

    return redirect("auctions:index")


def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist = Watchlist.objects.filter(user_id=user.id)
    listings = watchlist.values('listing__id')
    my_listings = Listing.objects.filter(pk__in=listings)

    context = {
        "listings": my_listings,
        "category": category
    }

    return render(request, "auctions/watchlist.html", {"context": context})


def category(request):
    listings = Listing.objects.all()

    category_list = []
    for item in categories:
        category_list.append(item)
    return render(request, "auctions/category.html", {"categories": category_list, "listings": listings})


def list_categories(request, category):
    listings = Listing.objects.filter(category=category)

    w_list = []

    if not request.user.is_authenticated:
        w_list = None
    else:
        watchlist = Watchlist.objects.filter(user=request.user)

        for item in watchlist:
            w_list.append(item)

    if not listings:
        listings = None

    context = {
        "listings": listings,
        "w_list": w_list,
        "category": category
    }

    return render(request, "auctions/categorylist.html", {"context": context})
