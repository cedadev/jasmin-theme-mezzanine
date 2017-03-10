from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.pages.models import Page
from mezzanine.core.models import Displayable, RichText, Orderable, Slugged, SiteRelated
from mezzanine.core.managers import SearchableManager
from mezzanine.utils.urls import path_to_slug, slugify
from mezzanine.utils.models import upload_to

class SiteSectionPage(Page):
    '''
    Structural page in site hierarchy, should appear in menu.
    Uses keywords to create relationship with KBArticlePages
    '''

    content = RichTextField(blank=True)
    search_fields = ("content",)

    class Meta:
        verbose_name = _("Site section")
        verbose_name_plural = _("Site sections")

class Portfolio(Page):
    '''
    A collection of individual portfolio items
    '''
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")


class PortfolioItem(Page, RichText):
    '''
    An individual portfolio item, should be nested under a Portfolio
    '''
    subtitle = models.CharField(max_length=200, blank=True)
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("theme.PortfolioItem.featured_image", "portfolio"),
        format="Image", max_length=255, null=True, blank=True)
    categories = models.ManyToManyField("PortfolioItemCategory",
                                        verbose_name=_("Categories"),
                                        blank=True,
                                        related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,
        help_text="A link to the finished project (optional)")

    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")


class PortfolioItemImage(Orderable):
    '''
    An image for a PortfolioItem
    '''
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("theme.PortfolioItemImage.file", "portfolio items"))
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """

    class Meta:
        verbose_name = _("Portfolio Item Category")
        verbose_name_plural = _("Portfolio Item Categories")
        ordering = ("title",)

ICON_BOX_LAYOUT_CHOICES = (
    ('TW', 'Two across'),
    ('TH', 'Three across'),
    ('TB', 'Three across boxes'),
)

class HomePage(Page):
    '''
    A page representing the format of the home page
    '''

    leader_text = models.TextField(blank=True,
        help_text="Add <br> for line breaks")
    button_text = models.CharField(max_length=100, blank=True,
        help_text="Optional, if present a button with the link specified "
        "below will be in the slide")
    button_link = models.CharField(max_length=2000, blank=True)
    icon_box_layout = models.CharField(max_length=2,
        choices=ICON_BOX_LAYOUT_CHOICES, default="TH")

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class IconBox(Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="boxes")
    icon = models.CharField(max_length=50,
        help_text="Enter the name of a font awesome icon, i.e. "
                  "fa-eye. A list is available here "
                  "http://fontawesome.io/")
    title = models.CharField(max_length=100)
    content = RichTextField()
    link = models.CharField(max_length=2000, blank=True,
        help_text="Optional, if provided clicking the box will go here.")
