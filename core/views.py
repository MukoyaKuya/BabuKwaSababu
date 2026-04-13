from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import PlatformIssue, NewsArticle, Endorsement, Subscriber, Volunteer, CampaignSettings, CampaignVideo
import os
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dynamic content from models
        context['issues'] = PlatformIssue.objects.filter(is_active=True)
        context['news_articles'] = NewsArticle.objects.all()[:6]
        context['videos'] = CampaignVideo.objects.all()
        context['endorsements'] = Endorsement.objects.all()
        context['campaign_settings'] = CampaignSettings.objects.first()
        
        # Default static image check
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'babu.png')
        context['babu_image_exists'] = os.path.exists(image_path)
        return context

NEWSLETTER_SUCCESS_HTML = '<div class="text-center font-display text-[#111827] p-12 bg-white border border-gray-200 shadow-xl text-2xl uppercase">THANK YOU FOR SUBSCRIBING!</div>'
VOLUNTEER_SUCCESS_HTML = '<div class="bg-white p-8 border-4 border-black text-[#2522e8] font-display text-center shadow-[12px_12px_0px_rgba(0,0,0,1)] animate-pulse uppercase">WE WILL BE IN TOUCH SOON!</div>'


# HTMX Form Views
@require_POST
def newsletter_signup(request):
    email = request.POST.get('email')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    constituency = request.POST.get('constituency', '')
    ward = request.POST.get('ward', '')
    phone_number = request.POST.get('phone_number', '')

    if not email:
        return HttpResponse('Error', status=400)

    Subscriber.objects.update_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'constituency': constituency,
            'ward': ward,
            'phone_number': phone_number,
        },
    )
    return HttpResponse(NEWSLETTER_SUCCESS_HTML)

@require_POST
def volunteer_signup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    skill = request.POST.get('skill', 'other')
    message = request.POST.get('message', '')

    if not (name and email):
        return HttpResponse('Error', status=400)

    valid_skills = {choice for choice, _ in Volunteer.SKILL_CHOICES}
    if skill not in valid_skills:
        skill = 'other'

    Volunteer.objects.create(name=name, email=email, skill=skill, message=message)
    return HttpResponse(VOLUNTEER_SUCCESS_HTML)

# Placeholder Views
class VisionView(TemplateView):
    template_name = 'core/vision.html'

class NewsListView(TemplateView):
    template_name = 'core/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_articles'] = NewsArticle.objects.all()
        return context

class DonateView(TemplateView):
    template_name = 'core/donate.html'
