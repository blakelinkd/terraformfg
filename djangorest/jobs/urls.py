from django.urls import path
from .views import JobSearchView
from .views import JobCreateView
from .views import JobScanView

urlpatterns = [
    path('search/', JobSearchView.as_view(), name='job-search'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('scan/', JobScanView.as_view(), name='job-scan'),


]
