from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORY_CHOICES = (
    ("Clothing, Shoes & Accessories", "Clothing, Shoes & Accessories"),
    ("Sporting Goods", "Sporting Goods"),
    ("Toys & Hobbies", "Toys & Hobbies"),
    ("Home & Garden", "Home & Garden"),
    ("Jewelry & Watches", "Jewelry & Watches"),
    ("Health & Beauty", "Health & Beauty"),
    ("Business", "Business"),
    ("Electronics", "Electronics"),
    ("Collectibles & Art", "Collectibles & Art"),
    ("Books, Movies & Music", "Books, Movies & Music"),
    ("Other", "Other")
)

class User(AbstractUser):
    id = models.AutoField(primary_key=True) 

class Listings(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length = 30, choices = CATEGORY_CHOICES, blank=True) 
    image_url = models.URLField(max_length = 20000, default="https://img.favpng.com/22/10/12/question-mark-desktop-wallpaper-grey-computer-icons-png-favpng-FTNv8p4eRd8kVubahAEhbJXCc.jpg") 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_id")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.title} for ${self.price} by {self.owner}"

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}: Bid ${self.bid_price} for {self.listing} by {self.user}"

class Comments(models.Model):
    id = models.AutoField(primary_key=True) 
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_id_com")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer_id")
    comment = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id}: Comment for {self.listing} by {self.writer}"
    
class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_watch")

    def __str__(self):
        return f"{self.id}: User {self.user} is watching for {self.listing}" 

class Winner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_win")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_win")
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="winning_bid", null=True)

    def __str__(self):
        return f"{self.id}: {self.listing} listings winner is {self.user}"