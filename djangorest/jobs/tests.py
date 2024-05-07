from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Job

class JobSearchViewTest(TestCase):
    def setUp(self):
        # Create some job entries to test with
        Job.objects.create(url="http://example.com/job1", title="Software Engineer", company_name="ExampleTech", skills="Python, Java, Linux")
        Job.objects.create(url="http://example.com/job2", title="Data Scientist", company_name="DataCorp", skills="Python, R, SQL")
        Job.objects.create(url="http://example.com/job3", title="System Administrator", company_name="SysAdmin Inc.", skills="Linux, Bash, AWS")
        self.client = APIClient()

    def test_search_jobs_by_skills(self):
        # Search for jobs that require Python or Linux skills
        response = self.client.post('/jobs/search/', {'skills': 'Python, Linux'}, format='json')

        # Check if the response status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the response data
        self.assertEqual(len(response.data), 3)
        titles = {job['title'] for job in response.data}
        self.assertIn("Software Engineer", titles)
        self.assertIn("System Administrator", titles)

    def test_search_jobs_no_skills_provided(self):
        # Search without providing skills
        response = self.client.post('/jobs/search/', {'skills': ''}, format='json')
        
        # Expect a bad request response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class JobCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job_data = {
            'url': "http://example.com/job123",
            'html_content': "Example content",
            'skills': "Python, Django",
            'compatibility': 5,
            'title': "Backend Developer",
            'company_name': "Tech Inc.",
            'location': "Remote",
            'has_applied': 0
        }
        self.response = self.client.post(
            '/jobs/create/',
            self.job_data,
            format="json"
        )

    def test_create_job(self):
        """Ensure we can create a new job object."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        job = Job.objects.get()
        self.assertEqual(job.title, "Backend Developer")
        self.assertEqual(job.skills, "Python, Django")

    def test_create_job_bad_request(self):
        """Test creating a job with incomplete data to ensure it fails."""
        incomplete_data = {
            'url': "http://example.com/job124",
            # Missing other required fields
        }
        response = self.client.post(
            '/jobs/create/',
            incomplete_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        