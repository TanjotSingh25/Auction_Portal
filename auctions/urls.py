from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListings", views.createListings, name="createListings"),
    path("closeListing", views.closeListing, name="closeListing"),
    path("addToWatchList/<str:listing_id>", views.addToWatchList, name="addToWatchList"),
    path("<str:listing_id>", views.openListing, name="openListing")
    
    
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)