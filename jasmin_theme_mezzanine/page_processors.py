
from mezzanine.pages.page_processors import processor_for
from .models import Portfolio, PortfolioItem, PortfolioItemCategory, HomePage


@processor_for(Portfolio)
def portfolio_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page)
    categories = PortfolioItemCategory.objects.filter(portfolioitems__in=items).distinct()
    return {'items': items, 'categories': categories}


@processor_for(PortfolioItem)
def portfolioitem_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    prortfolioitem = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related(
        'categories', 'images').get(id=page.portfolioitem.id)
    items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page.parent)
    categories = PortfolioItemCategory.objects.filter(portfolioitems__in=items).distinct()
    return {'portfolioitem': prortfolioitem, 'items': items, 'categories': categories}


@processor_for(HomePage)
def home_processor(request, page):
    '''
    Placeholder page processor in case other things (Portfolios etc)
    need to be passed into the context in future
    '''
    homepage = HomePage.objects.prefetch_related(
        'boxes').get(id=page.homepage.id)
    return {"homepage": homepage,}