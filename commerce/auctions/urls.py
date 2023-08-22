from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("index/", views.index, name="index"),
    path("new_auction", views.new_auction, name="new_auction"),
    path("category", views.category, name="category"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("bid/<int:id>/", views.bid, name="bid"),
    path("add/<int:id>/", views.addwatchlist, name="add"),
    path("remove/<int:id>/", views.removewatchlist, name="remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction") 
]
