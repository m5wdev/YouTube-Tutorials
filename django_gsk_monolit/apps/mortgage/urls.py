from django.urls import path, include

from apps.mortgage.views import (
    MortgageView,
    MortgageCorporactiveView,
    MortgageMilitaryView,
    MortgageMotherView,
)


app_name = 'mortgage'

urlpatterns = [
    path('mortgage/', include([
        path('', MortgageView.as_view(), name='index'),
        path('corporactive/', MortgageCorporactiveView.as_view(), name='corporactive'),
        path('military/', MortgageMilitaryView.as_view(), name='military'),
        path('mother/', MortgageMotherView.as_view(), name='mother'),
    ])),
]
