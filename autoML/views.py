from django.views.generic import TemplateView

class LogInView(TemplateView):
    template_name='success_login.html'

class LogOutView(TemplateView):
    template_name='success_logout.html'
    
class IndexView(TemplateView):
    template_name='index.html'
