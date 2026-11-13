from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccueilPriveView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/accueil.html'
