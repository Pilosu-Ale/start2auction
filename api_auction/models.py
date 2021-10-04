from django.db import models
from django.contrib.auth.models import User
from api_auction.utils import sendTransaction
import hashlib

    
class Auction(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_vendor')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_winner',null=True)
    asset_title = models.CharField(max_length=100, default="default_name")
    description = models.TextField(default="default_description")
    entry_price = models.FloatField(default=None)
    bid = models.FloatField(default=None, null=True)
    status = models.CharField(max_length=20, default="OPEN")
    start_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    
    hash = models.CharField(max_length=66, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def writeOnChain(self, jsonAuction):
        self.hash = hashlib.sha256(jsonAuction.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        
        self.save()
    