from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import extract_text_from_pdf, analyze_resume_with_gemini

class ResumeUploadView(APIView):
    def post(self, request):
        pdf_file = request.FILES.get('resume')
        if not pdf_file:
            return Response({'error': 'No resume uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            text = extract_text_from_pdf(pdf_file)
            result = analyze_resume_with_gemini(text)
            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
