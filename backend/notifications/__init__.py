"""
AfCFTA Notification System

Provides notification capabilities for the crawling system through multiple channels:
- Email notifications via SMTP
- Slack notifications via webhooks

Usage:
    from backend.notifications import NotificationManager
    
    manager = NotificationManager()
    await manager.notify_crawl_success(job_id="...", country_code="KE", stats={...})
"""

from backend.notifications.base_notifier import (
    BaseNotifier, 
    NotificationType, 
    NotificationSeverity,
    NotificationData,
)
from backend.notifications.email_notifier import EmailNotifier
from backend.notifications.slack_notifier import SlackNotifier
from backend.notifications.notification_manager import NotificationManager

__all__ = [
    "BaseNotifier",
    "NotificationType",
    "NotificationSeverity",
    "NotificationData",
    "EmailNotifier",
    "SlackNotifier",
    "NotificationManager",
]

__version__ = "1.0.0"
