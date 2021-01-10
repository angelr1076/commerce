from django.urls import path
from . import views

app_name = "auctions"
urlpatterns = [

    # Listing paths
    path("", views.index, name="index"),
    path("login/", views.loginview, name="login"),
    path("logout/", views.logoutview, name="logout"),
    path("register/", views.register, name="register"),
    path("addlisting/", views.add_listing, name="addlisting"),
    path("viewlisting/<int:listing_id>", views.view_listing, name="viewlisting"),
    path("closedlisting/", views.closed_listing, name="closedlisting"),

    # Watchlist paths
    path("watchlistswitch/<int:listing_id>", views.watchlist_switch, name="watchlistswitch"),
    path("watchlist/", views.watchlist, name="watchlist"),

    # Categories
    path("category/", views.category, name="category"),
    path("category/<str:category>", views.list_categories, name="categorylist"),
]
