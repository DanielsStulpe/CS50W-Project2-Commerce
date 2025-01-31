from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("listing/<int:id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/comment", views.comment, name="comment"),
    path("listing/<int:id>/close", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>/", views.category, name="category"),
]
