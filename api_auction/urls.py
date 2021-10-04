from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.AuctionViewSet)

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('auction/<int:id>', views.auction_bid_page, name="auction_bid"),
    path('auction/', include(router.urls)),
]