from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResumeUploadSerializer
from rest_framework import status
from .utils import extract_text_from_pdf, analyze_resume_with_gemini
from rest_framework.permissions import IsAuthenticated
from .models import ParsedResume
from datetime import date

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #todays upload count
        today = date.today()
        uploads_today = ParsedResume.objects.filter(
            user=request.user,
            created_at__date = today
        ).count()

        print(f"{request.user} has uploaded {uploads_today} resumes today.")


        # if uploads_today >= 3:
        #     return Response(
        #         {'error': 'Upload limit reached. You can only upload 3 resumes per day.'},
        #         status=status.HTTP_429_TOO_MANY_REQUESTS
        #     )

        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pdf_file = serializer.validated_data['resume']

        try:
            text = extract_text_from_pdf(pdf_file)
            result = analyze_resume_with_gemini(text)

            if not result:
                return Response({'error': 'Resume analysis failed or Gemini is unavailabe'}, status=503)
            
            #To automatically save to the DB
            ParsedResume.objects.create(user=request.user, raw_json=result)
            return Response({'result': result}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#To view a resume
class ResumeJsonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            latest_resume = ParsedResume.objects.filter(user=request.user).latest('-created_at')
            return Response({'resume': latest_resume.raw_json})
        except ParsedResume.DoesNotExist:
            return Response({'error': 'No Resume Found'}, status=404)
        

