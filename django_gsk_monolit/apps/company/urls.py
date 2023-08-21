from django.urls import path, include

from apps.company.views import (
    CompanyView,
    CompanyMissionView,
    CompanyManagementView,
    CompanyResponsibilityView,
    CompanyJobView,
    CompanyHistoryView,
    CompanyStructureView,
    CompanyPartnershipView,
    CompanyTendersView,
    CompanyTendersFaqView,
    ContactsView,
)


company_patterns = ([
    path('', CompanyView.as_view(), name='index'),
    path('mission/', CompanyMissionView.as_view(), name='mission'),
    path('management/', CompanyManagementView.as_view(), name='management'),
    path('responsibility/', CompanyResponsibilityView.as_view(), name='responsibility'),
    path('job/', CompanyJobView.as_view(), name='job'),
    path('history/', CompanyHistoryView.as_view(), name='history'),
    path('structure/', CompanyStructureView.as_view(), name='structure'),
    path('partnership/', CompanyPartnershipView.as_view(), name='partnership'),
    path('tenders/', CompanyTendersView.as_view(), name='tenders'),
    path('tenders/faq/', CompanyTendersFaqView.as_view(), name='tenders-faq'),
], 'company')


# app_name = 'company'

urlpatterns = [
    path('company/', include(company_patterns)),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
