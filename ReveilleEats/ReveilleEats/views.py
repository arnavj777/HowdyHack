
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
  system_instruction="I will input ingredients and you will output 1 recipe idea ONLY. When I  input 'next' you will give the next recipe name. Then I will give you one of the recipe names you gave me and you will tell me how to make it.The format will be dish name, ingredients needed, instructions and asking if user has more questions. If input is not about ingredients respons with please input ingredients",
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
def screen4(request):
    return render(request,"screen4.html")

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
  
    if request.method == "POST":
        user_input = request.POST.get("q")  # Get the input from the form

        if user_input:
            prompt = f"{user_input}"
            try:
                # Get the AI-generated content
                recipe_1_response = model.generate_content(prompt)
                recipe_1 = recipe_1_response.candidates[0]['output']  # Access the actual text content

                recipe_2_response = chat_session.send_message("next")
                recipe_2 = recipe_2_response.candidates[0]['output']

                recipe_3_response = chat_session.send_message("next")
                recipe_3 = recipe_3_response.candidates[0]['output']

                recipe_4_response = chat_session.send_message("next")
                recipe_4 = recipe_4_response.candidates[0]['output']

                # Store the recipes in the session
                request.session['recipe_1'] = recipe_1
                request.session['recipe_2'] = recipe_2
                request.session['recipe_3'] = recipe_3
                request.session['recipe_4'] = recipe_4

            except Exception as e:
                chatbot_response = f"Error: {e}"

    context = {
        "recipe1": recipe_1,
        "recipe2": recipe_2,
        "recipe3": recipe_3,
        "recipe4": recipe_4,
    }

    return render(request, 'screen4.html', context)


def recipe_detail(request, variety):
    # Logic to determine which recipe was clicked
    if variety == 'A':
        recipe = request.session.get('recipe_1', '')
    elif variety == 'B':
        recipe = request.session.get('recipe_2', '')
    elif variety == 'C':
        recipe = request.session.get('recipe_3', '')
    elif variety == 'D':
        recipe = request.session.get('recipe_4', '')
    else:
        recipe = ''  # Default to an empty string if no valid variety is found

    chatbot_response = ''  # Initialize with a default value

    try:
        response = chat_session.send_message(recipe)  # Call the AI model
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            chatbot_response = format_recipe(response.candidates[0]['output'])  # Format the response
    except Exception as e:
        chatbot_response = f"Error: {e}"

    return render(request, 'navbar.html', {'chatbot_response': chatbot_response})

'''    
    # Logic to determine which recipe was clicked
    recipe_1 = request.session.get('recipe_1', '')
    recipe_2 = request.session.get('recipe_2', '')
    recipe_3 = request.session.get('recipe_3', '')
    recipe_4 = request.session.get('recipe_4', '')

    if variety == 'A':
        recipe = recipe_1
    elif variety == 'B':
        recipe = recipe_2
    # Add more conditions as needed for other recipes
    elif variety == 'C':
        recipe = recipe_3
    elif variety == 'D':
        recipe = recipe_4
    try:
        response = chat_session.send_message(recipe)  # Call the AI model
        if response and response.text:
            # Format the response to improve display in HTML
            chatbot_response = format_recipe(response)
    except Exception as e:
        chatbot_response = f"Error: {e}"

    return render(request, 'navbar.html', {'chatbot_response': chatbot_response})    

'''
'''def select(request):
    """
    Handles the user's input and displays the chatbot's response on the same page.
    """

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
'''

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