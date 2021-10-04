from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.shortcuts import redirect
from .models import Auction
from .serializers import AuctionSerializer
from .forms import *
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import viewsets
import json

class AuctionViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()

def homepage(request):
    
    if cache.get("cache"):
        auction_list_open = cache.get("cache")[0]
        auction_list_closed = cache.get("cache")[1]
        print("Data from cache")
    else:
        auction_list_open = Auction.objects.filter(status="OPEN").order_by('end_date')      
        auction_list_closed = Auction.objects.filter(status="CLOSED").order_by('-end_date')      
        cache.set("cache", [auction_list_open, auction_list_closed])
        print("Data from DB")
        
    time_limit = timezone.now()
        
    if auction_list_open:
        for auction in auction_list_open:
            if auction.end_date <= time_limit:
                auction.status = "CLOSED"
                if cache.get(f"{auction.id}") is None:
                    cache.expire(f"{auction.id}", timeout=0)
                    auction.save()
                else:
                    auction.winner = User.objects.get(username=cache.get(f"{auction.id}")[0])
                    auction.bid = cache.get(f"{auction.id}")[1]
                    cache.expire(f"{auction.id}", timeout=0)
                    jsonAuction = AuctionSerializer(auction)
                    j = json.dumps(jsonAuction.data)
                    auction.writeOnChain(j)
                cache.expire("cache", timeout=0)    
            else:
                if cache.get(f"{auction.id}") is None:
                    auction.bid = auction.entry_price
                else:
                    auction.winner = User.objects.get(username=cache.get(f"{auction.id}")[0])
                    auction.bid = cache.get(f"{auction.id}")[1]
                auction.save()
                    

    
    if request.method == "POST":
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.vendor = request.user
            auction.title = form.cleaned_data['asset_title']
            auction.description = form.cleaned_data['description']
            auction.entry_price = form.cleaned_data['entry_price']
            auction.end_date = timezone.now() + timedelta(minutes=1)
            auction.save()
            cache.expire("cache", timeout=0)
            return HttpResponseRedirect("/")   
    else:   
        form = CreateAuctionForm()
    
    return render(request, "homepage.html", {
                                            'form': form, 
                                            'auction_list_open': auction_list_open, 
                                            'auction_list_closed': auction_list_closed
                                            })  
            
    
            
    
def auction_bid_page(request, id):
    queryset = Auction.objects.exclude(status='CLOSED')
    auction = get_object_or_404(queryset, id=id)
   
    temp = auction.end_date + timedelta(hours=2)
    end_date = temp.strftime("%b %d, %Y %H:%M:%S")
    
    if cache.get(f"{auction.id}") is None:
        bid_temp = auction.entry_price
        winner_temp = None
    else:
        winner_temp = cache.get(f"{auction.id}")[0]
        bid_temp = cache.get(f"{auction.id}")[1]
        
    if request.method == "POST":
        form = BidAuctionForm(request.POST, instance=auction)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if cache.get(f"{auction.id}"):
                cache.set(f"{auction.id}", [request.user, bid], timeout=None)
                winner_temp = cache.get(f"{auction.id}")[0]
                bid_temp = cache.get(f"{auction.id}")[1]
            else:
                cache.set(f"{auction.id}", [request.user, bid], timeout=None)
                winner_temp = cache.get(f"{auction.id}")[0]
                bid_temp = cache.get(f"{auction.id}")[1]
            
            return redirect('auction_bid', id=auction.id)
    else:   
        form = BidAuctionForm()
    return render(request, "auction_bid_page.html", {
                                                    'form': form,  
                                                    'bid_temp': bid_temp, 
                                                    'winner_temp': winner_temp, 
                                                    'auction': auction, 
                                                    'end_date': end_date})

