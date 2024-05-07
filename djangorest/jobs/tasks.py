from celery import shared_task
@shared_task
def debug_task(self):
    # Your processing logic for the URL
    print(f'Request: {self.request!r}')
