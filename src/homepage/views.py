from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
# A wedge of Django (awod)


class HomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_statement"] = "Nice to see you!"
        context["my_name"] = "Tony"
        return context

    def say_bye(self):
        return "Goodbye"
