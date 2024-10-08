
from django.shortcuts import render
from django.http import HttpResponse
import google.generativeai as genai
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
from django.shortcuts import render, redirect


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
        "French Toast\n\n**Ingredients:**\n\n* 4 slices of bread\n* 1 egg\n* 1/4 cup milk\n* 1 teaspoon sugar\n* 1/2 teaspoon vanilla extract\n* Butter or cooking spray, for greasing\n\n**Instructions:**\n\n1. In a shallow dish, whisk together the egg, milk, sugar, and vanilla extract.\n2. Dip each slice of bread into the egg mixture, making sure it's fully coated.\n3. Heat a skillet or griddle over medium heat and grease with butter or cooking spray.\n4. Cook the bread for 2-3 minutes per side, or until golden brown and cooked through. \n5. Serve immediately with your favorite toppings, such as syrup, fruit, whipped cream, or powdered sugar.\n\nDo you have any other questions? \n",
      ],
    },
  ]
)

'''loggedIn = False
def login(request):
    return render(request, 'login.html')
    
'''

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Home page with the chatbot after login
@login_required
@csrf_exempt

def home(request):
    """
    Displays the homepage with the chat interface. Requires login.
    """
    return render(request, 'navbar.html')  # Render the home template

def login_view(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')
    

def logout_view(request):
    """
    Logs out the user and redirects them to the login page.
    """
    auth_logout(request)
    return redirect('login')

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
                response = chat_session.send_message(prompt)  # Call the AI model
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