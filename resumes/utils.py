# import io
# from pdfminer.high_level import extract_text
# import google.generativeai as genai
# from django.conf import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)

# def extract_text_from_pdf(file):
#     file_stream = io.BytesIO(file.read())
#     text = extract_text(file_stream)
#     print(text)
#     return text

# def analyze_resume_with_gemini(resume_text):
#     prompt = f"""
#     Extract the following from this resume:
#     - Full Name
#     - Job Title
#     - Skills
#     - Experience Summary

#     Resume Text:
#     {resume_text}
#     """

#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     return response.text.strip()


# import io
# from pdfminer.high_level import extract_text
# import google.generativeai as genai
# from django.conf import settings
# import json
# import re

# genai.configure(api_key=settings.GEMINI_API_KEY)

# def extract_text_from_pdf(file):
#     file_stream = io.BytesIO(file.read())
#     text = extract_text(file_stream)
#     return text.strip()

# def analyze_resume_with_gemini(resume_text):
#     prompt = f"""
# You are a resume parser. Analyze the resume text below and return ONLY a valid JSON object in this format:

# {{
#   "Name": "",
#   "Position": "",
#   "Country": "",
#   "ShortBio": "",
#   "Skills": ["", "", "..."],
#   "Experience": [
#     {{
#       "Company": "",
#       "Position": "",
#       "Duration": "",
#       "Responsibilities": ""
#     }}
#   ],
#    "Education": [
#     {{
#       "Degree": "",
#       "Institution": "",
#       "Duration": ""
#     }}
#   ],
#   "Certifications": [
#     {{
#       "Title": "",
#       "Issuer": "",
#       "Date": ""
#     }}
#   ]
# }}

# Requirements:
# - Include **all** relevant skills (languages, tools, frameworks, etc).
# - For **Experience**, list each job with a short summary of responsibilities   .
# - If the candidate has more than one **education** entry, include all.
# - If there are **certifications**, extract them too.
# - Respond with **only valid JSON**. Do not include explanations, titles, or anything outside the JSON.

# Resume Text:
# \"\"\"
# {resume_text}
# \"\"\"
# """

#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)
#     content = response.text.strip()

#     # Optional: extract JSON from noisy response using regex
#     try:
#         json_match = re.search(r'\{.*\}', content, re.DOTALL)
#         if json_match:
#             return json.loads(json_match.group())
#         else:
#             return {"error": "JSON not found in Gemini response", "raw_response": content}
#     except Exception as e:
#         return {"error": str(e), "raw_response": content}



# import io
# import re
# import json
# from pdfminer.high_level import extract_text
# import google.generativeai as genai
# from django.conf import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)

# def extract_text_from_pdf(file):
#     file_stream = io.BytesIO(file.read())
#     text = extract_text(file_stream)
#     #print(text)
#     return text

# def analyze_resume_with_gemini(resume_text):
#     prompt = f"""
# You are a resume parser. From the resume text below, extract structured JSON in the following format:

# ALL descriptions must be written in **first person** (e.g., "I built...", "I developed...", "I collaborated...").

# {{
#   "Name": "",
#   "Position": "",
#   "Country": "",
#   "ShortBio": "",
#   "Skills": ["", "", "..."],
#   "Experience": [
#     {{
#       "Company": "",
#       "Position": "",
#       "Duration": "",
#       "Overview": "A brief paragraph describing the company.",
#       "Details": [
#         "a detailed paragraph explaining the first bullet point from the resume.",
#         "a detailed paragraph explaining the second bullet point.",
#         "... and so on for all bullet points listed."
#       ]
#     }}
#   ],
#   "Education": [
#     {{
#       "Degree": "",
#       "Institution": "",
#       "Duration": ""
#     }}
#   ],
#   "Certifications": [
#     {{
#       "Title": "",
#       "Issuer": "",
#       "Date": ""
#     }}
#   ]
# }}

# Instructions:
# - The short bio should be exactly what is on the resume, if there is no bio, create one based on the information you have about the person.
# - Do not limit the number of skills; extract all listed.
# - For each job:
#   - Include the **Company**, **Position**, and **Duration**.
#   - Start with an **Overview** of the project or company focus.
#   - Then, for each bullet point or listed responsibility, create a **separate paragraph summary** under "Details".
# - Include all education and certifications available.
# - Respond only with **valid JSON**.

# Resume Text:
# \"\"\"
# {resume_text}
# \"\"\"
# """

#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)
#     content = response.text.strip()

#     try:
#         json_match = re.search(r'\{.*\}', content, re.DOTALL)
#         if json_match:
#             return json.loads(json_match.group())
#         else:
#             return {"error": "JSON not found in Gemini response", "raw_response": content}
#     except Exception as e:
#         return {"error": str(e), "raw_response": content}


import io
import re
import json
from pdfminer.high_level import extract_text
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def extract_text_from_pdf(file):
    file_stream = io.BytesIO(file.read())
    text = extract_text(file_stream)
    #print(text)
    return text

def analyze_resume_with_gemini(resume_text):
    prompt = f"""
You are a resume parser. From the resume text below, extract structured JSON in the following format:

ALL descriptions must be written in **first person** (e.g., "I built...", "I developed...", "I collaborated...").
{
    {
  "Name": "",
  "Location": "",
  "avatar": "",
  "Position": "",
  "ShortBio": "",
  "Linkedin": "",
  "Github": "",
  "Whatsapp": "",
  "Resume": "",
  "Skills": ["","","..."],
  "Experience": [
    {
      "Company": "",
      "Position": "",
      "Duration": "",
      "Img": "",
      "AboutCompany": "",
      "Link": "",
      "WhatIDid": ""
    },

  ],
  "Education": {
    "Degree": "",
    "Institution": "",
    "Duration": "",
    "Img": ""
  }
}

}

Instructions:
- incase there is no about company just come up with something brief
- incase there is no position look through the skills and add the position that fits it
- The short bio should be exactly what is on the resume, if there is no bio, create one based on the information you have about the person.
- Do not limit the number of skills; extract all listed.
- Respond with **only valid JSON**. Do not include explanations, titles, or anything outside the JSON..

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    content = response.text.strip()

    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"error": "JSON not found in Gemini response", "raw_response": content}
    except Exception as e:
        return {"error": str(e), "raw_response": content}
