from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Article
from users.models import CustomUser
from .twitter import post_to_twitter

@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    """
    Signal to automatically send notifications when an article is approved
    """
    # Check if article was just approved (not newly created)
    if not created and instance.is_approved:
        print(f"SIGNAL: Article approved: {instance.title}")
        
        # Get subscribers to this journalist
        subscribers = CustomUser.objects.filter(
            role='reader',
            subscribed_journalists=instance.author
        ).distinct()
        
        # Also get subscribers to the publisher if exists
        if instance.publisher:
            publisher_subscribers = CustomUser.objects.filter(
                role='reader',
                subscribed_publishers=instance.publisher
            ).distinct()
            subscribers = subscribers.union(publisher_subscribers)
        
        print(f"SIGNAL: Notifying {subscribers.count()} subscribers")
        
        # Send email notifications
        email_count = 0
        for subscriber in subscribers:
            try:
                subject = f'New Article Published: {instance.title}'
                message = render_to_string('news_app/email/new_article.html', {
                    'subscriber': subscriber,
                    'article': instance,
                    'site_url': 'http://localhost:8000'
                })
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    html_message=message,
                    fail_silently=True,
                )
                email_count += 1
            except Exception as e:
                print(f"SIGNAL: Email failed for {subscriber.email}: {e}")
        
        # Post to Twitter
        try:
            twitter_result = post_to_twitter(instance)
            print(f"SIGNAL: Twitter post: {twitter_result}")
        except Exception as e:
            print(f"SIGNAL: Twitter failed: {e}")
        
        print(f"SIGNAL: Completed - {email_count} emails sent")