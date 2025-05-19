from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import logging
import csv
from django.http import JsonResponse
# from ...apicall import send_scan_to_roboflow_leg  # Import the API function


logger = logging.getLogger(__name__)



@login_required
def leg(request):
    # Render the chatbot page
    return render(request, 'leg.html')

def chatbot_api_leg(request):
    user_input = request.GET.get("message", "").lower().strip()
    
    # Get the current analysis result from session
    analysis_result_leg = request.session.get("analysis_result_leg", "").lower().strip()
    print(analysis_result_leg)
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fracture_qa.csv')
    
    # Default response
    response = "Sorry, I don't have specific information about that. Try asking about elements related to your scan result."
    
    try:
        # Open and read the CSV file
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Iterate through rows to find a matching image_name and question
            for row in reader:
                if row['class_name'].lower() == analysis_result_leg and row['keyword'].lower() in user_input: #########################################################################################
                    response = row['answer']
                    break
    except FileNotFoundError:
        logger.error(f"CSV file not found at {csv_file_path}")
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
    
    # Include the current result type in the response
    result_info = f"Based on your {analysis_result_leg} scan result: " if analysis_result_leg else ""
    print("chatbot", result_info, response)
    return JsonResponse({"response": f"{result_info}{response}"})

@login_required
def upload_image_api_leg(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        image_path = f"temp/{image.name}"  # Save the uploaded image temporarily

        # Save the image to a temporary location
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Delete the temporary file after saving
        # os.remove(image_path)

        # Check the CSV file for additional information based on the image name
        csv_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fracture_qa.csv')
        csv_response = []
        api_result_leg = None
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['image_name'].lower() == os.path.splitext(image.name.lower())[0]:
                        api_result_leg = row['class_name']
                        csv_response.append(row['answer'])
        except FileNotFoundError:
            logger.error(f"CSV file not found at {csv_file_path}")
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")

        # Include CSV response and class name in the context if found
        # context = {
        #     'api_result_leg': api_result_leg or "No result found",
        #     'csv_response': csv_response or "No additional information available"
        # }

        csv_response = " ".join(csv_response) if csv_response else "No additional information available"
        
        #################################################################################################################3
        import google.generativeai as genai

        API_KEY = "AIzaSyANgsIFgSreJAOvVhCxGkBvpORU3sFq-4s"  # Replace with your API key from Google AI Studio
        genai.configure(api_key=API_KEY)

        # Select the Gemini model available in the free tier (e.g., 'gemini-1.5-flash' or 'gemini-pro')
        model = genai.GenerativeModel('gemini-1.5-flash') # Or try 'gemini-pro'

        prompt = f"""Give a brief description of the following information without removing any necessary details:
        information: {csv_response}
        """

        try:
            response = model.generate_content(prompt)
            description = response.text
            print(description)
        except Exception as e:
            print(f"Error generating diagnosis: {e}")
        
        #############################################################################################
        print("=" * 50)
        if api_result_leg:
            request.session["analysis_result_leg"] = api_result_leg
            print("upload image",f"CLASS NAME: {api_result_leg}")
        if description:
            print(f"Description: {description}")
        print("=" * 50)

        # Render the leg page with the CSV response
        return render(request, 'leg.html', {
            # 'context': context,
            'api_result_leg': api_result_leg,
            'description': description,
            'uploaded_image': image.name,
            })

    return render(request, 'leg.html')