from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from api.models import Asset, Portfolio, Review


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('description', 'risk_rating', 'overall_rating')
    template_name = 'api/create_review.html'

    def _get_valid_portfolio(self):
        """
        Return respective portfolio to write review on to the context
        
        Sort by:
        - Number of reviews
        - To be added...

        Exclude:
        - Portfolios that are your own
        - Portfolios you've already reviewed before
        """
        portfolios = Portfolio.objects.all() \
                    .annotate(num_reviews=Count('review')) \
                    .order_by('num_reviews')

        # exclude portfolios that are your own
        portfolios = portfolios.exclude(user=self.request.user)

        # only keep portfolios you haven't reviewed before
        for review in Review.objects.filter(author=self.request.user):
            if review.portfolio != None:
                portfolios = portfolios.exclude(id=review.portfolio.id)

        # select first portfolio to meet all conditions
        return portfolios[0] if len(portfolios) > 0 else None


    def dispatch(self, request, *args, **kwargs):
        self.portfolio = self._get_valid_portfolio()
        self.assets = Asset.objects.filter(portfolio=self.portfolio) if self.portfolio is not None else None

        return super(ReviewCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.portfolio = self.portfolio

        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['portfolio'] = self.portfolio
        context['assets'] = self.assets

        return context

    def get_success_url(self):
        return reverse_lazy('portfolios')


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'api/detail_review.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        portfolio = self.object.portfolio
        assets = Asset.objects.all().filter(portfolio=portfolio.id)

        context = super().get_context_data()
        context['portfolio'] = portfolio
        context['assets'] = assets
        context['assets_total'] = sum([asset.holdings for asset in assets])

        return context

    
@login_required
def RateReview(request, **kwargs):
    if request.method == 'POST':
        rating = request.POST.get('review-rating')
        review_id = kwargs['pk']

        # if user submitted an empty form, redirect back to original page
        if rating == None:
            return redirect(request.POST.get('next', '/'))

        # add 50 points for rating the review
        request.user.points += 50
        request.user.save()

        # add appropriate points for person that wrote the review based on the rating
        reviewer = Review.objects.get(id=review_id).author
        reviewer.points += ((int(rating) - 1) * 50)
        reviewer.save()

        # mark the review as rated
        review = Review.objects.get(id=review_id)
        review.rated = True
        review.save()

        # return to original page
        return redirect(request.POST.get('next', '/'))
    else:
        return HttpResponse(status=405)


class ReviewList(LoginRequiredMixin, ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'api/reviews.html'

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)
