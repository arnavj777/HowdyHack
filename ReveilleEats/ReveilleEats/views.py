'''from django.http import HttpResponse
from django.shortcuts import render

import google.generativeai as genai
import os

API_KEY="AIzaSyBePnJjq6UcQIwgWoAAFtp6tbOK_G8tzDY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def home(request):
    
    return render(request, 'home.html')

def search(request):
    chatbot_response = None  # Initialize an empty variable for the chatbot response
    
    # Check if the request is a POST request
    if request.method == "POST":
        title = request.POST.get("q")
        
        # Generate content using the AI model
        if title:
            response = model.generate_content(title)
            # Check if response has valid content
            if response:
                chatbot_response = response.text
    
    # Render the same page with the chatbot response passed in context
    return render(request, 'navbar.html', {'chatbot_response': chatbot_response})'''
from django.shortcuts import render
from django.http import HttpResponse
import google.generativeai as genai

# Configure Google Generative AI with your API key
API_KEY = "AIzaSyBePnJjq6UcQIwgWoAAFtp6tbOK_G8tzDY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="I will input ingredients and you will output 1 recipe idea. The format will be dish name, ingredients needed, instructions and asking if user has more questions. If input is not about ingredients respons with please input ingredients",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "bread,sugar,vanilla, egg",
      ],
    },
    {
      "role": "model",
      "parts": [
        "##  French Toast\n\n**Ingredients:**\n\n* 4 slices of bread\n* 1 egg\n* 1/4 cup milk\n* 1 teaspoon sugar\n* 1/2 teaspoon vanilla extract\n* Butter or cooking spray, for greasing\n\n**Instructions:**\n\n1. In a shallow dish, whisk together the egg, milk, sugar, and vanilla extract.\n2. Dip each slice of bread into the egg mixture, making sure it's fully coated.\n3. Heat a skillet or griddle over medium heat and grease with butter or cooking spray.\n4. Cook the bread for 2-3 minutes per side, or until golden brown and cooked through. \n5. Serve immediately with your favorite toppings, such as syrup, fruit, whipped cream, or powdered sugar.\n\nDo you have any other questions? \n",
      ],
    },
  ]
)

'''loggedIn = False
def login(request):
    return render(request, 'login.html')
    
'''


def home(request):
    """
    Displays the homepage with the chat interface. No AI response yet.
    """
    #if loggedIn:
    return render(request, 'navbar.html')  # Render the home template

def search(request):
    """
    Handles the user's input and displays the chatbot's response on the same page.
    """
    chatbot_response = None  # Initialize the response variable

    if request.method == "POST":
        user_input = request.POST.get("q")  # Get the input from the form

        if user_input:
            prompt = f"{user_input}"
            try:
                response = model.generate_content(prompt)  # Call the AI model
                if response and response.text:
                    # Format the response to improve display in HTML
                    chatbot_response = format_recipe(response.text)
            except Exception as e:
                chatbot_response = f"Error: {e}"

    return render(request, 'navbar.html', {'chatbot_response': chatbot_response})


def format_recipe(text):
    """
    Custom function to format recipe output for better display.
    """
    # Example recipe response will contain ingredients and instructions
    # Remove unnecessary closing tags, like repeated </li></li>
    formatted_text = text.replace('</li></li>', '</li>')
    
    # Add proper headers for ingredients and instructions
    formatted_text = formatted_text.replace('**Ingredients:**', '<h3>Ingredients:</h3><ul>')
    formatted_text = formatted_text.replace('**Instructions:**', '</ul><h3>Instructions:</h3><ol>')

    # Convert list-like items into actual HTML list elements
    formatted_text = formatted_text.replace('* ', '<li>').replace('1.', '<li>').replace('2.', '</li><li>')
    formatted_text = formatted_text.replace('3.', '</li><li>').replace('4.', '</li><li>')
    formatted_text = formatted_text.replace('5.', '</li><li>').replace('6.', '</li><li>')
    formatted_text = formatted_text.replace('7.', '</li><li>').replace('8.', '</li><li>')

    # Ensure lists are closed properly
    formatted_text += '</ol>'
    
    return formatted_text