from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User, Listing, Watchlist, Bid, categories

def add_listings_to_layout(request):
    open_listings = Listings = Listing.objects.filter(closed_auction="No")

    listings_length = len(open_listings)
    return { 'listings_total': listings_length }


def add_closed_to_layout(request):
    closed_listings = Listings = Listing.objects.filter(closed_auction="Yes")

    closed_length = len(closed_listings)
    return { 'closed_total': closed_length }


def add_watchlist_to_layout(request):
    if request.user.id is not None:
        user = User.objects.get(pk=request.user.id)
        watchlist = Watchlist.objects.filter(user_id=user.id)
        listings = watchlist.values('listing__id')
        my_listings = Listing.objects.filter(pk__in=listings)
    else:
        user = None
        watchlist = None

    if watchlist:
        watchlist_length = len(my_listings)
    else:
        watchlist_length = 0

    return { 'length': watchlist_length }


def category_count(request):
    category_count = len(categories)
    return { 'category_count': category_count }