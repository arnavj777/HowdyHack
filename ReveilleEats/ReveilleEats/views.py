from django.http import HttpResponse
from django.shortcuts import render

import google.generativeai as genai
import os

API_KEY="AIzaSyBePnJjq6UcQIwgWoAAFtp6tbOK_G8tzDY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def home(request):
    return render(request, 'home.html')

def search(request):
    # Check if the request is a POST request
    if request.method == "POST":
        title = request.POST.get("q")
        
        # Generate content using the AI model
        if title:
            response = model.generate_content(title)
            # Check if response has valid content
            if response:
                # Render the results on a page or return as plain text (adjust as necessary)
                return HttpResponse(response.text)
        return HttpResponse("No input provided or model error.")
    
    # Return an empty response or render the search form page if it's a GET request
    return render(request, 'search.html')


