import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from authentication.models import CustomUser
from simple_history.models import HistoricalRecords


class Portfolio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    risk_tolerance = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name="Additional Information", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.email}'s {self.nickname}"


CHOICES = (
    (1, 'Recommend significant changes'),
    (2, 'Recommend moderate changes'),
    (3, 'Recommend minor changes'),
    (4, 'Recommend little to no change'),
    (5, 'Recommend no change'),
)
class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True)
    risk_rating = models.IntegerField(
        choices=CHOICES, 
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, 
        blank=True,
        verbose_name='Risk Level'
    )
    overall_rating = models.IntegerField(
        choices=CHOICES, 
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, 
        blank=True,
        verbose_name='Overall Appropriateness'
    )
    description = models.TextField(verbose_name='Suggestions and/or feedback')
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
    holdings = models.FloatField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.ticker} ${self.holdings}"

    def get_percentage(self):
        portfolio_total = sum([asset.holdings for asset in Asset.objects.filter(portfolio=self.portfolio)])
        return (self.holdings / portfolio_total) * 100
