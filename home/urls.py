from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post_events_data$', 
             views.post_events_data, name='post_events_data'),
    url(r'^modify_events_data$', 
             views.modify_events_data, name='modify_events_data'),
    url(r'^delete_events_data$', 
             views.delete_events_data, name='delete_events_data'),
    url(r'^google_calendar_sync$', 
             views.google_calendar_sync, name='google_calendar_sync')
]
