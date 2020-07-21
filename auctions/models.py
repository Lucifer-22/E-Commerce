from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

CATEGORY_CHOICES = (
    ('MC','Mens Clothing'),
    ('WC','Womens Clothing'),
    ('G','Games'),
    ('T','Tech'),
    ('BP','Beauty Products'),
    ('O','Others'),
)

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    description = models.TextField()
    image = models.URLField(blank = True)
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name="winner")
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    items = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.items}: {self.user} = ( {self.bid} /- )"


class Comment(models.Model):
    comment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.items}: -/ {self.user} "


class Watchlist(models.Model):
    items = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.items}: -/ {self.user} "


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    items = models.ForeignKey(Listing, on_delete=models.CASCADE, null = True, blank = True)
    start_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username