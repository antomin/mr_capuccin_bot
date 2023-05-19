from django.urls import path

from report_app.views import ReportIndexView

urlpatterns = [
    path('', ReportIndexView.as_view(), name='index')
]
