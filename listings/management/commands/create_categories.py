from django.core.management.base import BaseCommand
from listings.models import Category

class Command(BaseCommand):
    help = 'ایجاد دسته‌بندی‌های اولیه'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'وبسایت', 'platform': 'website'},
            {'name': 'اینستاگرام', 'platform': 'instagram'},
            {'name': 'تلگرام', 'platform': 'telegram'},
            {'name': 'یوتیوب', 'platform': 'youtube'},
        ]
        
        for cat in categories:
            Category.objects.get_or_create(
                platform=cat['platform'],
                defaults={'name': cat['name']}
            )
        
        self.stdout.write(self.style.SUCCESS('دسته‌بندی‌ها با موفقیت ایجاد شدند'))
