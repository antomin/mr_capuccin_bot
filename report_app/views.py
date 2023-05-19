from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ReportIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'report_app/index.html'
