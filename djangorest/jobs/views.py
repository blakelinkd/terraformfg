from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from .tasks import debug_task

class JobScanView(APIView):
    def post(self, request, *args, **kwargs):
        input_string = request.data.get('search_string')
        if not input_string:
            return Response({'error': 'No search string provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Send the string to the Celery task
        result = debug_task.delay(input_string)
        
        # Respond with accepted status but do not wait for the task to complete
        return Response({'message': 'Processing started', 'task_id': result.task_id}, status=status.HTTP_202_ACCEPTED)


class JobSearchView(APIView):
    def post(self, request, *args, **kwargs):
        skills_query = request.data.get('skills', '')
        if not skills_query.strip():
            return Response({"error": "No skills provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        skills_list = [skill.strip() for skill in skills_query.split(',') if skill.strip()]

        query = Q()
        for skill in skills_list:
            query |= Q(skills__icontains=skill)

        jobs = Job.objects.filter(query)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobCreateView(APIView):
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)