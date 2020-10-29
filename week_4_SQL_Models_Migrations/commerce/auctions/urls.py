from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing-<int:listing_id>/", views.listing, name="listing"),
    path("create-listing/", views.create_listing, name="create_listing"),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("listing-<int:listing_id>/delete/", views.delete_listing, name="delete_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>/", views.category, name="category")
    
]
