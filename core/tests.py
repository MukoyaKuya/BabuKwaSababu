from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import NewsArticle, Subscriber, Volunteer


class NewsPageTests(TestCase):
    def test_news_page_renders_articles_from_database(self):
        NewsArticle.objects.create(
            source='Daily Planet',
            headline='Babu Announces New Cost Reduction Plan',
            link='https://example.com/news-1',
            date=date(2026, 4, 1),
        )

        response = self.client.get(reverse('news'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Babu Announces New Cost Reduction Plan')


class SignupFlowTests(TestCase):
    def test_newsletter_signup_updates_existing_subscriber(self):
        Subscriber.objects.create(email='supporter@example.com', first_name='Old')

        response = self.client.post(
            reverse('newsletter_signup'),
            {
                'email': 'supporter@example.com',
                'first_name': 'New',
                'last_name': 'Name',
                'constituency': 'Westlands',
                'ward': 'Karura',
                'phone_number': '0700000000',
            },
        )

        self.assertEqual(response.status_code, 200)
        subscriber = Subscriber.objects.get(email='supporter@example.com')
        self.assertEqual(subscriber.first_name, 'New')
        self.assertEqual(subscriber.ward, 'Karura')

    def test_volunteer_signup_saves_skill_and_message(self):
        response = self.client.post(
            reverse('volunteer_signup'),
            {
                'name': 'Jane Doe',
                'email': 'jane@example.com',
                'skill': 'digital',
                'message': 'I can help with social media strategy.',
            },
        )

        self.assertEqual(response.status_code, 200)
        volunteer = Volunteer.objects.get(email='jane@example.com')
        self.assertEqual(volunteer.skill, 'digital')
        self.assertEqual(volunteer.message, 'I can help with social media strategy.')

    def test_signup_endpoints_reject_non_post_requests(self):
        newsletter_response = self.client.get(reverse('newsletter_signup'))
        volunteer_response = self.client.get(reverse('volunteer_signup'))

        self.assertEqual(newsletter_response.status_code, 405)
        self.assertEqual(volunteer_response.status_code, 405)
