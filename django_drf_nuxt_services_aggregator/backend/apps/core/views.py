from django.shortcuts import render
from django.views.generic import TemplateView

from apps.company.models.brand import Brand
from apps.company.models.company import Company
from apps.company.models.category import Category


class SitemapXmlView(TemplateView):
    template_name = 'seo/sitemaps_xml/sitemapxml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['courses'] = Course.objects.filter(active=True).order_by('order')
        # context['blog_posts'] = Blog.objects.filter(active=True).order_by('-updated')[:100]
        return context


class CompaniesSitemapXmlView(TemplateView):
    template_name = 'seo/sitemaps_xml/companies.html'
    content_type = 'application/xml'
    queryset = Company.objects.all()

    def get(self, request, *args, **kwargs):
        subdomain = request.headers['Host'].split('.')[0]

        if subdomain == 'localhost:8000' or \
            subdomain == 'localhost' or \
            subdomain == 'servis-centers.ru':
            subdomain = 'moscow'

        self.queryset = self.queryset.filter(city__subdomain__name=subdomain).order_by('-updated')[:50000]
        return render(request, self.template_name, context=self.get_context_data(queryset=self.queryset), content_type=self.content_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['companies'] = Company.objects.all()
        context['companies'] = self.queryset
        return context


class BrandsSitemapXmlView(TemplateView):
    template_name = 'seo/sitemaps_xml/brands.html'
    content_type = 'application/xml'
    queryset = Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = self.queryset.order_by('slug')
        return context


class CategoriesSitemapXmlView(TemplateView):
    template_name = 'seo/sitemaps_xml/categories.html'
    content_type = 'application/xml'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.queryset.order_by('slug')
        return context
