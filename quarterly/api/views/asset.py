import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy

from api.models import Asset, Portfolio


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    fields = ('ticker', 'name', 'holdings')
    template_name = 'api/create_asset.html'

    def form_valid(self, form):
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        form.instance.portfolio = Portfolio.objects.get(id=portfolio_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add all assets related to this portfolio
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        portfolio = Portfolio.objects.filter(id=portfolio_id)
        if portfolio.exists():
            assets = Asset.objects.filter(portfolio=portfolio.get(id=portfolio_id))
            context['assets'] = assets
            context['portfolio'] = portfolio.get(id=portfolio_id)
        else:
            context['assets'] = []
            context['portfolio'] = None

        return context

    def get_success_url(self):
        portfolio_id = uuid.UUID(self.request.get_full_path().split('/')[2])
        return reverse_lazy('create_asset', kwargs={'pk': portfolio_id})

@login_required
def AssetCreateFunctionView(request, **kwargs):
    if request.method == 'POST':
        portfolio = Portfolio.objects.filter(id=kwargs['pk'])
        if not portfolio.exists():
            # portfolio does not exist to associate asset to
            return HttpResponse(status=404)

        try:
            Asset.objects.create(
                ticker=request.POST.get('ticker'),
                name=request.POST.get('name'),
                holdings=request.POST.get('holdings'),
                portfolio=Portfolio.objects.get(id=kwargs['pk'])
            )
        except ValueError:
            # likely means one of the fields was empty
            pass

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return HttpResponse(status=405)


@login_required
def AssetUpdate(request, **kwargs):
    if request.method == 'POST':
        asset = Asset.objects.filter(id=kwargs['pk'])
        if not asset.exists():
            return HttpResponse(status=404)
        else:
            if request.POST.get('submit-type') == 'Update':
                asset.update(
                    ticker=request.POST.get('ticker'),
                    name=request.POST.get('name'),
                    holdings=request.POST.get('holdings'),
                )
            elif request.POST.get('submit-type') == 'Delete':
                asset.delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        return HttpResponse(status=405)
