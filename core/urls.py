from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('vision/', views.VisionView.as_view(), name='vision'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    
    # HTMX Endpoints
    path('htmx/newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('htmx/volunteer-signup/', views.volunteer_signup, name='volunteer_signup'),
]
