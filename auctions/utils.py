from .models import Bid

def get_highest_bid(listing):
    filtered = Bid.objects.filter(listing=listing)
    if filtered:
        return max(filtered, key=lambda bid: bid.amount)
    else:
        return 0
