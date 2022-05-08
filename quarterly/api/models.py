import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from authentication.models import CustomUser
from simple_history.models import HistoricalRecords


class Portfolio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.email}'s {self.nickname}"


class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True)
    description = models.TextField(verbose_name='Review Description')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    rated = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.author} reviewed {self.portfolio}"


class Asset(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ticker = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    holdings = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.ticker} ({self.holdings}%)"
