from django.conf.urls import url
from . import views

urlpatterns = [
    # LANDING
    url(r'^$', views.landing),
    url(r'^main$', views.landing),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logoff$', views.logoff),

    # HOME
    url(r'^quotes$', views.success),
    url(r'^process$', views.process),
    url(r'^favorite/(?P<user_id>\d+)$', views.add_favorite),
    url(r'^remove/(?P<user_id>\d+)$', views.remove_favorite),

    # USER
    url(r'^users/(?P<user_id>\d+)$', views.profile),
]