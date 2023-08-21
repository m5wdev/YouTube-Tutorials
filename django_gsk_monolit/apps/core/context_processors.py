from datetime import datetime
from dateutil import relativedelta

from apps.core.models import SiteSettings
from apps.realty.models.object import Object


def settings(request):
    return {'settings': SiteSettings.load()}


def monolit_objects(request):
    return {'monolit_objects': Object.objects.filter(active=True, all_sold=False).order_by('order')}


def monolit_company_age(request):
    foundation_date = datetime(2005, 8, 16, 00, 00)
    now = datetime.now()
    difference = relativedelta.relativedelta(now, foundation_date)

    years   = difference.years
    # months  = difference.years * 12 + difference.months
    # days    = difference.years * 365 + difference.days
    # hours   = difference.years * 8760 + difference.hours
    # minutes = (difference.years * (8760 * 60)) + difference.minutes
    return {'monolit_company_age': years}


def current_month_rus(request):
    months = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь', 7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}
    current_month = datetime.now().month
    current_month_text = months[current_month]
    return {'current_month_rus': current_month_text}


def compleated_objects(request):
    return {'compleated_objects': Object.objects.filter(active=True, all_sold=True, completed=True).exclude(slider_completed_image=None)}
