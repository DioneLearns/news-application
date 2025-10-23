"""
News application views handling articles, newsletters, and user management.

This module contains all view functions for:
- Article creation, approval, and management
- Newsletter creation, approval, and management
- User authentication and role-based access
- Email notifications and Twitter integration
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from .models import CustomUser, Article, Publisher, Newsletter
from .forms import ArticleForm, NewsletterForm
from .twitter import post_to_twitter

def home(request):
    """
    Display the application's homepage with featured content.
    
    Renders the main landing page showing recent published articles,
    system statistics, and navigation to key application sections.
    
    Args:
        request: Standard HTTP request object
        
    Returns:
        HttpResponse: Rendered homepage template with context
    """
    articles = Article.objects.filter(is_approved=True).order_by('-created_at')[:10]
    newsletters = Newsletter.objects.filter(is_approved=True).order_by('-created_at')[:5]
    return render(request, 'home.html', {
        'articles': articles, 
        'newsletters': newsletters
    })

def all_newsletters(request):
    """
    Display all approved newsletters to readers.
    
    Retrieves both sent and scheduled newsletters from the database
    for public browsing or subscriber access.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Newsletter catalog page with all newsletters
    """
    newsletters = Newsletter.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'news_app/all_newsletters.html', {'newsletters': newsletters})

@login_required
def create_article(request):
    """
    Handle article creation by journalists with role-based validation.
    
    Processes article submission forms, validates journalist permissions,
    and creates new article drafts awaiting editorial approval.
    
    Args:
        request: HTTP request object with form data
        
    Returns:
        HttpResponse: Article creation form or redirect with status message
    """
    if request.user.role == 'editor':
        messages.error(request, "Editors cannot create articles.")
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created successfully! Waiting for editor approval.')
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'news_app/create_article.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'editor')
def approve_articles(request):
    """
    Display articles pending editorial approval to editors.
    
    Shows a queue of unapproved articles for editorial review
    with options to approve or manage content.
    
    Args:
        request: HTTP request object (editor role required)
        
    Returns:
        HttpResponse: Approval interface with pending articles
    """
    pending_articles = Article.objects.filter(is_approved=False)
    return render(request, 'news_app/approve_articles.html', {'articles': pending_articles})

@login_required
@user_passes_test(lambda u: u.role == 'editor')
def approve_article(request, article_id):
    """
    Process article approval with notification workflows.
    
    Handles editorial approval of articles, sends email notifications
    to subscribers, and integrates with Twitter for publication
    announcements. Includes comprehensive debug logging.
    
    Args:
        request: HTTP request object
        article_id (int): Primary key of article to approve
        
    Returns:
        HttpResponseRedirect: Redirect to approval queue with status
    """
    article = get_object_or_404(Article, id=article_id)
    
    print(f"DEBUG: Approve article view called for article ID: {article_id}")
    print(f"DEBUG: Article title: {article.title}")
    print(f"DEBUG: Article currently approved: {article.is_approved}")
    
    if not article.is_approved:
        article.is_approved = True
        article.save()
        
        print("DEBUG: Article saved as approved")
        
        subscribers = CustomUser.objects.filter(role='reader')
        subject = f'New Article Published: {article.title}'
        
        print(f"DEBUG: Found {subscribers.count()} subscribers")
        
        email_count = 0
        for subscriber in subscribers:
            print(f"DEBUG: Preparing email for {subscriber.email}")
            
            message = render_to_string('news_app/email/new_article.html', {
                'subscriber': subscriber,
                'article': article,
                'site_url': 'http://localhost:8000'
            })
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    html_message=message,
                    fail_silently=False,
                )
                email_count += 1
                print(f"DEBUG: Sent email to {subscriber.email}")
            except Exception as e:
                print(f"DEBUG: Failed to send email to {subscriber.email}: {e}")
        
        print("DEBUG: Calling Twitter integration")
        twitter_result = post_to_twitter(article)
        print(f"DEBUG: Twitter result: {twitter_result}")
        
        messages.success(request, f'Article "{article.title}" approved successfully! Notifications sent to {email_count} subscribers.')
        print(f"DEBUG: Success message set for {email_count} subscribers")
    else:
        messages.info(request, f'Article "{article.title}" was already approved.')
        print("DEBUG: Article was already approved, no notifications sent")
    
    return redirect('approve_articles')

@login_required
def my_articles(request):
    """
    Display articles authored by the current journalist user.
    
    Provides journalists with a personalized view of their
    article portfolio across all publication statuses.
    
    Args:
        request: HTTP request object with user session
        
    Returns:
        HttpResponse: Personal article management dashboard
    """
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'news_app/my_articles.html', {'articles': articles})

@login_required
def update_article(request, article_id):
    """
    Handle article updates with permission validation.
    
    Allows authors and editors to modify existing articles
    with proper access control and form validation.
    
    Args:
        request: HTTP request object
        article_id (int): Primary key of article to update
        
    Returns:
        HttpResponse: Edit form or redirect after save
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.author and request.user.role != 'editor':
        return HttpResponseForbidden("You don't have permission to edit this article.")

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news_app/update_article.html', {'form': form, 'article': article})

@login_required
def delete_article(request, article_id):
    """
    Handle article deletion with authorization checks.
    
    Allows authors and editors to remove articles from the system
    after confirming ownership or editorial privileges.
    
    Args:
        request: HTTP request object
        article_id (int): Primary key of article to delete
        
    Returns:
        HttpResponse: Confirmation page or redirect after deletion
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.author and request.user.role != 'editor':
        return HttpResponseForbidden("You don't have permission to delete this article.")

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('dashboard')

    return render(request, 'news_app/delete_article.html', {'article': article})

@login_required
def dashboard(request):
    """
    Display role-appropriate user dashboard with content management.
    
    Provides customized dashboards for journalists (personal articles)
    and editors (all system articles) with relevant content and actions.
    
    Args:
        request: HTTP request object with user context
        
    Returns:
        HttpResponse: Role-specific dashboard interface
    """
    user = request.user
    if user.role == 'journalist':
        articles = Article.objects.filter(author=user).order_by('-created_at')
    elif user.role == 'editor':
        articles = Article.objects.all().order_by('-created_at')
    else:
        return redirect('home')

    return render(request, 'news_app/dashboard.html', {'articles': articles})

@login_required
def edit_article(request, article_id):
    """
    Handle article editing with simplified form processing.
    
    Provides article modification interface for authors and editors
    with basic form handling and redirect flow.
    
    Args:
        request: HTTP request object
        article_id (int): Primary key of article to edit
        
    Returns:
        HttpResponse: Edit form or redirect to dashboard
    """
    article = get_object_or_404(Article, id=article_id)
    if request.user != article.author and request.user.role != 'editor':
        return redirect('dashboard')
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news_app/edit_article.html', {'form': form, 'article': article})

@login_required
def subscribe_journalist(request, journalist_id):
    """
    Handle journalist subscription for reader users.
    
    Allows readers to subscribe to specific journalists
    for personalized content recommendations and updates.
    
    Args:
        request: HTTP request object
        journalist_id (int): Primary key of journalist to subscribe to
        
    Returns:
        HttpResponseRedirect: Redirect to homepage with status message
    """
    if request.user.role != 'reader':
        return redirect('home')
    
    journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')
    request.user.subscribed_journalists.add(journalist)
    messages.success(request, f"Subscribed to {journalist.username}!")
    return redirect('home')

@login_required
def subscribe_publisher(request, publisher_id):
    """
    Handle publisher subscription for reader users.
    
    Enables readers to subscribe to publishing organizations
    for content from specific sources and editorial teams.
    
    Args:
        request: HTTP request object
        publisher_id (int): Primary key of publisher to subscribe to
        
    Returns:
        HttpResponseRedirect: Redirect to homepage with status message
    """
    if request.user.role != 'reader':
        return redirect('home')
    
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscribed_publishers.add(publisher)
    messages.success(request, f"Subscribed to {publisher.name}!")
    return redirect('home')

@login_required
def create_newsletter(request):
    """
    Handle newsletter creation by journalist users.
    
    Processes newsletter submission forms with journalist
    validation and creates draft newsletters for editorial review.
    
    Args:
        request: HTTP request object with form data
        
    Returns:
        HttpResponse: Newsletter creation form or redirect with status
    """
    if request.user.role != 'journalist':
        messages.error(request, 'Only journalists can create newsletters.')
        return redirect('home')
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, 'Newsletter created successfully! Waiting for editor approval.')
            return redirect('home')
    else:
        form = NewsletterForm()
    
    return render(request, 'news_app/create_newsletter.html', {'form': form})

@login_required
def my_newsletters(request):
    """
    Display newsletters created by the current journalist.
    
    Provides journalists with management interface for their
    newsletter portfolio across all approval statuses.
    
    Args:
        request: HTTP request object with user session
        
    Returns:
        HttpResponse: Personal newsletter management dashboard
    """
    newsletters = Newsletter.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'news_app/my_newsletters.html', {'newsletters': newsletters})

@login_required
@user_passes_test(lambda u: u.role == 'editor')
def approve_newsletters(request):
    """
    Display newsletters pending editorial approval.
    
    Shows queue of unapproved newsletters to editors for
    review and publication decisions.
    
    Args:
        request: HTTP request object (editor role required)
        
    Returns:
        HttpResponse: Newsletter approval interface
    """
    pending_newsletters = Newsletter.objects.filter(is_approved=False)
    return render(request, 'news_app/approve_newsletters.html', {'newsletters': pending_newsletters})

@login_required
@user_passes_test(lambda u: u.role == 'editor')
def approve_newsletter(request, newsletter_id):
    """
    Process newsletter approval with subscriber notifications.
    
    Handles editorial approval of newsletters, sends email
    notifications to readers, and integrates with social media
    for publication announcements.
    
    Args:
        request: HTTP request object
        newsletter_id (int): Primary key of newsletter to approve
        
    Returns:
        HttpResponseRedirect: Redirect to approval queue with status
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    
    if not newsletter.is_approved:
        newsletter.is_approved = True
        newsletter.save()
        
        # Send email notifications to subscribers
        subscribers = CustomUser.objects.filter(role='reader')
        subject = f'New Newsletter: {newsletter.title}'
        
        email_count = 0
        for subscriber in subscribers:
            try:
                message = render_to_string('news_app/email/new_newsletter.html', {
                    'subscriber': subscriber,
                    'newsletter': newsletter,
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
                print(f'Newsletter email failed for {subscriber.email}: {e}')
        
        # Post to Twitter
        try:
            twitter_result = post_to_twitter(newsletter)
            print(f'Newsletter Twitter post: {twitter_result}')
        except Exception as e:
            print(f'Newsletter Twitter failed: {e}')
        
        messages.success(request, f'Newsletter \"{newsletter.title}\" approved! Notifications sent to {email_count} subscribers.')
    else:
        messages.info(request, f'Newsletter \"{newsletter.title}\" was already approved.')
    
    return redirect('approve_newsletters')

@login_required
def edit_newsletter(request, newsletter_id):
    """
    Handle newsletter updates with permission validation.
    
    Allows authors and editors to modify existing newsletters
    with proper access control and form processing.
    
    Args:
        request: HTTP request object
        newsletter_id (int): Primary key of newsletter to edit
        
    Returns:
        HttpResponse: Edit form or redirect to newsletter list
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    if request.user != newsletter.author and request.user.role != 'editor':
        return redirect('my_newsletters')
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated successfully!')
            return redirect('my_newsletters')
    else:
        form = NewsletterForm(instance=newsletter)
    
    return render(request, 'news_app/edit_newsletter.html', {'form': form, 'newsletter': newsletter})

@login_required
def delete_newsletter(request, newsletter_id):
    """
    Handle newsletter deletion with authorization checks.
    
    Allows authors and editors to remove newsletters from
    the system after confirming ownership or privileges.
    
    Args:
        request: HTTP request object
        newsletter_id (int): Primary key of newsletter to delete
        
    Returns:
        HttpResponse: Confirmation page or redirect after deletion
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    if request.user != newsletter.author and request.user.role != 'editor':
        return redirect('my_newsletters')
    
    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter deleted successfully!')
        return redirect('my_newsletters')
    
    return render(request, 'news_app/delete_newsletter.html', {'newsletter': newsletter})

def article_detail(request, article_id):
    """
    Display detailed view of individual approved articles.
    
    Shows complete article content to readers with proper
    formatting and related information display.
    
    Args:
        request: HTTP request object
        article_id (int): Primary key of article to display
        
    Returns:
        HttpResponse: Article detail page with full content
    """
    article = get_object_or_404(Article, id=article_id, is_approved=True)
    return render(request, 'news_app/article_detail.html', {'article': article})