from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register$',views.register),
    url(r'^login$', views.login),
    url(r'^addpage$', views.addpage),
    url(r'^processadd$', views.processadd),
    url(r'^wishlist$', views.wishlist),
    url(r'^logout$', views.logout),
    url(r'^wishlist/wishpage/(?P<wishid>\d+)$', views.wish),
    url(r'^wishlist/delete/(?P<wishid>\d+)$', views.deletewish),
    url(r'^joinwish/(?P<wishid>\d+)$', views.joinwish),
    #url(r'^joinwish/(?P<tripid>\d+)$', views.jointrip),


      # This line has changed! Notice that urlpatterns is a list, the comma is in
]                            # anticipation of all the routes that will be coming soon
