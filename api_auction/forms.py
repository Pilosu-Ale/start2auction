from django import forms
from .models import Auction
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache

class CreateAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['asset_title', 'description', 'entry_price']
    def clean_entry_price(self):
        entry_price = self.cleaned_data['entry_price']
        if entry_price < 1:
            raise forms.ValidationError("You must type at least 1$ entry price for the auction")
        return entry_price
            
        
class BidAuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['bid']
        
    def clean_bid(self):
        bid = self.cleaned_data['bid']
        auction = Auction.objects.get(id=self.instance.id)
        if cache.get(f"{auction.id}") is None:
            old = auction.entry_price
        else:
            old = cache.get(f"{auction.id}")[1]
        
        
        if bid <= old:
            raise forms.ValidationError(f"You have to offer more than {old}")
        return bid

        
    
