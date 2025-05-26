#WORKING WELL WITHOUT THE SERIOUS WEB SCRAPPING TOOLS, JUST HAVING MINOR ISSUES WITH GEMINI AND ALL

# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from JoblifyBackend import settings
# import json

# class FetchJobInfoView(APIView):
#     def post(self, request):
#         url = request.data.get("url", "")
#         if not url:
#             return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Step 1: Scrape page HTML
#         try:
#             resp = requests.get(url, timeout=10)
#             resp.raise_for_status()
#         except requests.RequestException:
#             return Response({"error": "Failed to fetch the URL"}, status=status.HTTP_400_BAD_REQUEST)

#         soup = BeautifulSoup(resp.text, "html.parser")

#         # Step 2: Remove unwanted tags to reduce noise
#         for tag in soup(["script", "style", "header", "footer", "nav", "form", "aside", "img", "button"]):
#             tag.decompose()

#         # Step 3: Extract visible text content for Gemini prompt
#         text_content = soup.get_text(separator="\n", strip=True)
#         # Limit to first 1500 chars to keep prompt efficient
#         text_content = text_content[:1500]
#         print(text_content)

#         # Step 4: Build Gemini prompt - concise, token efficient
#         prompt = f"""
# Extract the following job info from this text:

# Title:
# Company:
# Platform:

# Only return a JSON with keys "title", "company", and "platform".
# If data is not found, leave value empty string.

# Text:
# {text_content}
# """

#         # Step 5: Call Gemini API
#         gemini_data = self.call_gemini(prompt)

#         # Step 6: Handle fallback for platform - use domain if Gemini returns empty or null
#         platform = gemini_data.get("platform", "")
#         if not isinstance(platform, str) or platform.strip().lower() in ["", "unknown", "n/a", "none"]:
#             domain = urlparse(url).netloc
#             platform = domain.lower()

#         # Final cleaned response
#         response_data = {
#             "title": gemini_data.get("title", "") or "",
#             "company": gemini_data.get("company", "") or "",
#             "platform": platform or "",
#         }

#         return Response(response_data)

#     def call_gemini(self, prompt: str) -> dict:
#         GEMINI_API_KEY = settings.env('GEMINI_API_KEY')
#         endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

#         headers = {
#             "Content-Type": "application/json",
#             #"Authorization": f"Bearer {GEMINI_API_KEY}"
#         }

#         payload = {
#             "prompt": {"text": prompt},
#             "temperature": 0,
#             "candidateCount": 1,
#             "maxOutputTokens": 200,
#             "topP": 1,
#             "topK": 40
#         }

#         try:
#             response = requests.post(endpoint, headers=headers, json=payload)
#             response.raise_for_status()
#             data = response.json()
#             output_text = data['candidates'][0]['output']

#             # Parse Gemini's output as JSON
#             return json.loads(output_text)
#         except Exception:
#             # If anything fails, return empty dict
#             return {}

























































# BASIC SCRAPER MOSTLY WORKS WITH LINKEDIN, VERY BAD WITH OTHER SITES



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse


# class FetchJobInfoView(APIView):

#     def post(self, request):
#         url = request.data.get("url")
#         if not url:
#             return Response({"error": "Job URL is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             job_info = self.scrape_job_info(url)
#             return Response(job_info, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def scrape_job_info(self, url):
#         headers = {
#             "User-Agent": "Mozilla/5.0 (compatible; JobScraper/1.0; +https://yourdomain.com)"
#         }
#         resp = requests.get(url, headers=headers, timeout=15)
#         if resp.status_code != 200:
#             raise Exception(f"Failed to fetch page, status code {resp.status_code}")

#         soup = BeautifulSoup(resp.text, "html.parser")

#         # Extract Job Title
#         title = (
#             soup.find("h1") or
#             soup.find("h2") or
#             soup.find("title")
#         )
#         title_text = title.get_text(strip=True) if title else "Title not found"

#         # Extract Company Name
#         company = (
#             soup.find(class_="company") or
#             soup.find("span", {"class": "companyName"}) or
#             soup.find("div", {"class": "company"}) or
#             soup.find("a", {"class": "company"})
#         )
#         company_text = company.get_text(strip=True) if company else "Company not found"

#         # Extract Job Description
#         description = (
#             soup.find("div", {"class": "jobDescription"}) or
#             soup.find("div", {"id": "jobDescriptionText"}) or
#             soup.find("section", {"class": "job-description"}) or
#             soup.find("div", {"class": "description"})
#         )
#         description_text = description.get_text(separator="\n", strip=True) if description else "Description not found"

#         # Extract Platform (from URL hostname)
#         platform = self.extract_platform_from_url(url)

#         return {
#             "title": title_text,
#             "company": company_text,
#             "description": description_text,
#             "platform": platform
#         }

#     def extract_platform_from_url(self, url):
#         try:
#             parsed_url = urlparse(url)
#             hostname = parsed_url.hostname or ""
#             if hostname.startswith("www."):
#                 hostname = hostname[4:]
#             parts = hostname.split(".")
#             if len(parts) >= 2:
#                 return parts[-2].capitalize()
#             return parts[0].capitalize()
#         except Exception:
#             return "Unknown"

















































# THE ORIGINAL SCRAPER, NOT USING IT CAUSE ITS NOT WORKING WITH RENDERS FREE PLAN WORKS PERFECTLY




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
