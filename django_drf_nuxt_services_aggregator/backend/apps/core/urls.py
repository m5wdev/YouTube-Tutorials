from django.urls import path, include

from apps.core.views import (
    SitemapXmlView,
    CompaniesSitemapXmlView,
    BrandsSitemapXmlView,
    CategoriesSitemapXmlView,
)


sitemapxml_patterns = ([
    path('companies.xml', CompaniesSitemapXmlView.as_view(), name='companies'),
    path('brands.xml', BrandsSitemapXmlView.as_view(), name='brands'),
    path('categories.xml', CategoriesSitemapXmlView.as_view(), name='categories'),
], 'sitemapxml')

urlpatterns = [
    path('sitemap.xml', SitemapXmlView.as_view(), name='sitemapxml'),
    path('sitemap/', include(sitemapxml_patterns)),
]
