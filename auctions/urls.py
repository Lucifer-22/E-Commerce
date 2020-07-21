from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("product/<str:title>", views.listing, name="listing"),
    path("watchlist/add/<str:title>", views.addToWatchlist, name="addToWatchlist"),
    path("watchlist/remove/<str:title>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("watchlist/view", views.watchlist, name="watchlist"),
    path("product/comment/<str:title>", views.comment, name="comment"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("closebid/<str:title>", views.closebid, name="closebid"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("cart", views.cart, name="cart")
]
