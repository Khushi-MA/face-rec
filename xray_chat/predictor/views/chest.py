from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import logging
from django.http import JsonResponse
# from ...apicall import send_scan_to_roboflow_chest  # Import the API function


logger = logging.getLogger(__name__)


# Separate chat keywords dictionaries for each result type
chest_abnormal = {
    "Will I need a CT scan?":
        "A CT scan may be recommended if your X-ray is inconclusive, if multiple ribs are suspected to be fractured, or if there is concern about damage to internal organs like the lungs. It provides more detailed images than standard X-rays.",

    "Is it safe to use a rib belt for support?":
        "Rib belts or binders are generally *not recommended* for routine rib fractures as they can restrict breathing and increase the risk of pneumonia. Breathing exercises and pain management are preferred for recovery.",

    "Can a rib fracture cause long-term problems?":
        "Most rib fractures heal without long-term issues, but complications can include chronic pain, poor healing (nonunion), or organ injury if the break was severe. Proper rest, pain control, and breathing exercises reduce risks.",

    "Can I drive with a rib fracture?":
        "Driving is generally not advised in the early days after a rib fracture due to pain and limited motion, which can affect your ability to react. You should only drive once pain is manageable and you can safely control the vehicle.",

    "When can I resume sports?":
        "You can typically return to sports in 6–8 weeks, depending on pain, healing, and the intensity of the activity. Contact sports should be avoided until your doctor confirms the rib has fully healed.",

    "How long does it take for a rib fracture to heal?":
        "Most rib fractures heal within 6 weeks. Pain management and avoiding activities that strain the chest are key during recovery. Deep breathing exercises help prevent lung complications.",

    "Can I sleep normally with a rib fracture?":
        "You may need to sleep in an upright or semi-reclined position for comfort. Using extra pillows and avoiding pressure on the injured side can help reduce pain while sleeping.",

    "Do I need antibiotics for a rib fracture?":
        "Not usually. Rib fractures are bone injuries and don’t typically require antibiotics unless there's a related lung infection or open wound.",

    "Should I avoid deep breaths or coughing?":
        "No—while it may hurt, you *should* take deep breaths and cough regularly to prevent lung infections. Using a pillow to brace your chest while doing so can reduce pain.",

    "Is it normal to feel short of breath with a rib fracture?":
        "Mild shortness of breath can occur due to pain. However, if you experience severe or worsening breathlessness, seek immediate medical attention to rule out lung complications like pneumothorax (collapsed lung)."
}

chest_rib_fracture = {
    "Will I need a CT scan?":
        "A CT scan may be recommended if your X-ray is inconclusive, if multiple ribs are suspected to be fractured, or if there is concern about damage to internal organs like the lungs. It provides more detailed images than standard X-rays.",

    "Is it safe to use a rib belt for support?":
        "Rib belts or binders are generally *not recommended* for routine rib fractures as they can restrict breathing and increase the risk of pneumonia. Breathing exercises and pain management are preferred for recovery.",

    "Can a rib fracture cause long-term problems?":
        "Most rib fractures heal without long-term issues, but complications can include chronic pain, poor healing (nonunion), or organ injury if the break was severe. Proper rest, pain control, and breathing exercises reduce risks.",

    "Can I drive with a rib fracture?":
        "Driving is generally not advised in the early days after a rib fracture due to pain and limited motion, which can affect your ability to react. You should only drive once pain is manageable and you can safely control the vehicle.",

    "When can I resume sports?":
        "You can typically return to sports in 6–8 weeks, depending on pain, healing, and the intensity of the activity. Contact sports should be avoided until your doctor confirms the rib has fully healed.",

    "How long does it take for a rib fracture to heal?":
        "Most rib fractures heal within 6 weeks. Pain management and avoiding activities that strain the chest are key during recovery. Deep breathing exercises help prevent lung complications.",

    "Can I sleep normally with a rib fracture?":
        "You may need to sleep in an upright or semi-reclined position for comfort. Using extra pillows and avoiding pressure on the injured side can help reduce pain while sleeping.",

    "Do I need antibiotics for a rib fracture?":
        "Not usually. Rib fractures are bone injuries and don’t typically require antibiotics unless there's a related lung infection or open wound.",

    "Should I avoid deep breaths or coughing?":
        "No—while it may hurt, you *should* take deep breaths and cough regularly to prevent lung infections. Using a pillow to brace your chest while doing so can reduce pain.",

    "Is it normal to feel short of breath with a rib fracture?":
        "Mild shortness of breath can occur due to pain. However, if you experience severe or worsening breathlessness, seek immediate medical attention to rule out lung complications like pneumothorax (collapsed lung)."
}

# General keywords for any result
chest_general_keywords = {
     "how to use chatbot for x-ray": "Upload a clear X-ray image of the chest area. The AI will then analyze and report if it's 'normal', shows a 'rib fracture', or detects an 'abnormal rib'.",
    "can i self diagnose using chatbot": "No, the chatbot provides preliminary analysis and must not be used for self-diagnosis. Always consult a doctor.",
    "how accurate is the ai": "AI accuracy depends on its training data and model performance. It's a helpful tool but not a replacement for a doctor.",
    "help": "I can help explain your scan results. Please ask about specific elements you see.",
    "explain": "Your scan shows color patterns that indicate different health conditions.",
    "what does this mean": "The color in your scan helps identify specific conditions or states.",
    "doctor": "Always consult with your doctor for professional medical advice regarding your results."
}

@login_required
def chest(request):
    # Render the chatbot page
    return render(request, 'chest.html')

def chatbot_api_chest(request):
    user_input = request.GET.get("message", "").lower().strip()
    
    # Get the current analysis result from session
    analysis_result_chest = request.session.get("analysis_result_chest", "")
    print(analysis_result_chest)
    
    # Select the appropriate keywords dictionary based on analysis result
    if analysis_result_chest == "fracture":
        keywords = {**chest_abnormal, **chest_general_keywords}
    elif analysis_result_chest == "rib fracture":
        keywords = {**chest_rib_fracture, **chest_general_keywords}
    else:
        # If no result yet or unknown result, use only general keywords
        keywords = chest_general_keywords
    
    # Find matching response
    response = "Sorry, I don't have specific information about that. Try asking about elements related to your scan result."
    for keyword, answer in keywords.items():
        if keyword in user_input:
            response = answer
            break

    # Include the current result type in the response
    result_info = f"Based on your {analysis_result_chest} scan result: " if analysis_result_chest else ""
    
    return JsonResponse({"response": f"{result_info}{response}"})

@login_required
def upload_image_api_chest(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        image_path = f"temp/{image.name}"  # Save the uploaded image temporarily

        # Save the image to a temporary location
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Call the API function
        result = send_scan_to_roboflow_chest(image_path)
        predictions = result.get("predictions", [])
        api_result_chest = predictions[0].get("class") if predictions else "No abnormality detected"

        # Delete the temporary file after processing
        os.remove(image_path)
        
        # Store the result in the session for the chatbot to access
        request.session["analysis_result_chest"] = api_result_chest
        print("=" * 50)
        print(f"ANALYSIS RESULT HAND: {api_result_chest}")
        print("=" * 50)
        # Render the chest page with the API result
        return render(request, 'chest.html', {'api_result_chest': api_result_chest})

    return render(request, 'chest.html')