from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
from playwright.async_api import async_playwright
import requests
import json
import re
from JoblifyBackend import settings
from urllib.parse import urlparse


class FetchJobInfoView(APIView):

    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "Job URL is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job_info = asyncio.run(self.extract_job_data(url))
            return Response(job_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def extract_job_data(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            content = await page.content()
            visible_text = await page.inner_text('body')
            await browser.close()

        # Send to Gemini
        gemini_response = self.call_gemini(visible_text)

        return gemini_response
    
    
    

    def call_gemini(self, text):
        GEMINI_API_KEY = settings.env('GEMINI_API_KEY')
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        headers = {
            "Content-Type": "application/json",
        }

        prompt = f"""
        Extract the following information from this job listing text:
        - Job Title
        - Company Name
        - Job Description
        - Platform (e.g. LinkedIn, Indeed)

        Format the result as JSON like:
        {{
            "title": "...",
            "company": "...",
            "platform": "..."
        }}

        Text:
        {text}
        """

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        params = {"key": GEMINI_API_KEY}

        response = requests.post(endpoint, headers=headers, params=params, json=payload)
        data = response.json()



        try:
            text_output = data["candidates"][0]["content"]["parts"][0]["text"]

            # Remove triple backticks and everything between if present
            cleaned_text = re.sub(r"```json|```", "", text_output).strip()

            # Convert string to dict safely
            parsed = json.loads(cleaned_text)

            # Only return needed fields
            return {
                "title": parsed.get("title"),
                "company": parsed.get("company"),
                "platform": parsed.get("platform"),
            }

        except Exception as e:
            return {
                "error": "Failed to parse Gemini output",
                "details": str(e),
                "raw": text_output,
            }
