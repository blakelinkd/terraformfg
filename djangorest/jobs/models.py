from django.db import models

class Job(models.Model):
    url = models.TextField(unique=True, null=False)
    html_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    compatibility = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=False, blank=True)
    company_name = models.TextField(null=False, blank=True)
    location = models.TextField(null=True, blank=True, db_column='location')  # Explicit column name due to Python keyword conflict
    has_applied = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = 'jobs'  # Explicit table name to match your SQL schema

    def __str__(self):
        return f"{self.title} at {self.company_name}"
