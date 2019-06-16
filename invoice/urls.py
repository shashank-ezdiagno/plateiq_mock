from django.contrib import admin
from django.urls import path
from .views.upload_invoice_view import upload
from .views.digitization_progress_view import list_view
from .views.invoice_view import show
from .views.invoice_viewset import InvoiceViewSet
from django.conf.urls import include, url
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'invoice', InvoiceViewSet)

urlpatterns = [
    url(r'^$', upload, name='upload'),
    url(r'^api/v1/', include(router.urls)),
    url(r'progress/', list_view, name="list"),
    url(r'^show/(?P<invoice_id>[0-9a-z-]+)/$', show, name="show")
]