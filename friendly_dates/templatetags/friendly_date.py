from django import template
register = template.Library()

import datetime
from django.utils.timezone import now, localtime

@register.filter
def friendly_date(date_obj):
    date_obj = localtime(date_obj)
    has_time = isinstance(date_obj, datetime.datetime)

    current_date = localtime(now()).date()
    date_obj_date = date_obj.date() if has_time else date_obj # discard time info
    days_past= (current_date - date_obj_date).days
    
    if days_past == 0:
        return "Today at {}".format(date_obj.strftime("%I:%M %p")) if has_time else "Today"
    elif days_past == 1:
        return "Yesterday at {}".format(date_obj.strftime("%I:%M %p")) if has_time else "Yesterday"
    elif days_past == 2:
        return "Two days ago"
    else:
        if date_obj.year == current_date.year:
            return date_obj.strftime("%B %-d")
        return date_obj.strftime("%B %-d, %Y")
