from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# Separate chat keywords dictionaries for each result type
hand_fracture = {
    "what does fracture mean": "If the chatbot indicates 'fracture,' it means the AI has detected a potential break or crack in one or more of the bones in the hand as seen in the X-ray. This requires further review by a medical professional.",
    "what to do if fracture detected": "If a fracture is detected, seek immediate medical attention from a doctor or visit an emergency room for diagnosis and treatment.",
    "can ai tell severity of fracture": "The chatbot detects if a fracture exists but doesn't determine its severity (e.g., hairline or displaced). A doctor must interpret the result.",
    "can it differentiate types of fractures": "The model likely detects presence of any fracture but not specific types like spiral or compound fractures.",
    "can it show location of fracture or peen": "This depends on the chatbot interface. Some advanced interfaces highlight the region on the X-ray image."
}

hand_normal = {
    "what does normal mean": "Normal indicates that the AI analysis of the X-ray image suggests there are no visible signs of bone fractures or foreign metallic objects (like a peen). The bones appear to be intact and healthy.",
    "is my hand okay if it says normal": "A 'normal' result suggests no immediate signs of fracture or a 'peen,' but AI is a preliminary tool. Always consult a doctor if you're in pain.",
    "hand hurts but normal result": "X-rays show bones, not soft tissue. Pain might come from soft tissue injuries, so consult a doctor for further evaluation."
}

hand_peen = {
    "what is peen": "In the context of these X-ray results, 'peen' likely refers to the detection of a foreign metallic object, possibly a fragment from a tool or other source, visible in the hand X-ray.",
    "what to do if peen detected": "If a 'peen' (foreign object) is detected, consult a medical professional as it may require removal to avoid complications.",
    "can it tell what peen is made of": "The chatbot can detect dense objects like metal in the X-ray but cannot determine the material composition.",
    "what kind of peen detected": "It can detect radio-opaque (dense) foreign objects like metal, but not reliably detect less dense materials.",
    "can it show location of fracture or peen": "This depends on the chatbot interface. Some advanced interfaces highlight the region on the X-ray image."
}

# General keywords for any result
general_keywords = {
    "how to use chatbot for x-ray": "Upload a clear X-ray image of the hand. The AI will then analyze and report if it's 'normal', shows a 'fracture', or detects a 'peen'.",
    "can i self diagnose using chatbot": "No, the chatbot provides preliminary analysis and must not be used for self-diagnosis. Always consult a doctor.",
    "how accurate is the ai": "AI accuracy depends on its training data and model performance. It's a helpful tool but not a replacement for a doctor.",
    "help": "I can help explain your scan results. Please ask about specific elements you see.",
    "explain": "Your scan shows color patterns that indicate different health conditions.",
    "what does this mean": "The color in your scan helps identify specific conditions or states.",
    "doctor": "Always consult with your doctor for professional medical advice regarding your results."
}


# 001
img001 = {
    "what is this": "An intact wedge fracture means a wedge-shaped bone break has occurred but the surrounding bone remains relatively stable.",
    "how long to heal": "Healing time is around 6 to 10 weeks, though it may vary based on location and care.",
    "does it need casting or surgery": "Often managed with a cast or brace if stable; surgery is only needed if it becomes displaced.",
    "can AI tell if it's stable or not": "AI can flag fracture patterns but cannot determine stability. A doctor must review the full imaging.",
    "can AI locate this": "This depends on the software used. Some platforms may highlight the suspected fragment."
}
# 002
img002 = {
    "what is this": "An oblique fracture occurs when the break runs diagonally across the bone, often caused by an angled blow or twisting force.",
    "how long to heal": "Typically 6 to 12 weeks, depending on severity and location.",
    "can AI detect the angle of fracture": "AI may detect an oblique pattern but precise angle measurement requires radiological analysis.",
    "does this need surgery": "Some require surgery if the bone is unstable or displaced; otherwise, a cast or brace may suffice.",
    "is an this serious": "It can be serious if displaced, but many cases heal well with appropriate care."
}
# 003
img003 = {
    "what is this": "A fragmented wedge fracture means a wedge-shaped fragment of bone has broken off, often due to twisting or indirect force.",
    "how long to heal": "It typically takes 2 to 4 months to heal, depending on the extent of fragmentation and the treatment plan.",
    "do we need surgery": "Not always. Some cases are managed with immobilization, but displaced wedges may require surgical fixation.",
    "can AI detect wedge shape": "The AI may detect irregular fracture lines consistent with a wedge, but radiological review is necessary for confirmation.",
    "can AI determine if it's displaced": "No, AI detection indicates presence of fracture but not displacement. A radiologist must assess this."
}
# 004
img004 = {
    "what is this": "A spiral fracture wraps around the bone like a corkscrew, typically caused by twisting injuries.",
    "how long to heal": "Healing can take 2 to 4 months, depending on age, health, and treatment.",
    "can AI identify spiral patterns": "AI may suggest a spiral-type fracture, but exact classification must be confirmed by a radiologist.",
    "is a spiral painful": "Yes, it often causes significant pain due to the nature of the twist and possible tissue damage.",
    "always need surgery": "Not always. Stable spiral fractures may be managed conservatively, though surgery is common for displaced cases."
}

# Define image classification structure
IMAGE_CLASSIFICATIONS = {
    'hand': {
        'normal': hand_normal,
        'fracture': hand_fracture,
        'peen': hand_peen,
    },
    'leg': {
        'img001': img001,
        'img002': img002, 
        'img003': img003,
        'img004': img004,
    }
}

@login_required
def hand(request):
    # Render the chatbot page
    return render(request, 'hand.html')

@login_required
def upload_image_api_hand(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Get the filename and convert to lowercase for comparison
        image_name = image.name.lower().split('.')[0]  # Remove file extension
        
        # Find classification and specific type
        classification = None
        specific_type = None
        
        # Check if image name starts with any classification prefix
        if image_name.startswith('hand_'):
            classification = 'hand'
            specific_type = image_name.replace('hand_', '')
        elif image_name.startswith('img'):
            classification = 'leg'
            specific_type = image_name
        
        # If no match found in our structure, mark as unidentified
        if not classification or specific_type not in IMAGE_CLASSIFICATIONS.get(classification, {}):
            classification = 'unidentified'
            specific_type = 'unknown'
        
        # Store full result information in session
        result_info = {
            'classification': classification,
            'specific_type': specific_type
        }
        request.session["analysis_result_hand"] = result_info
        
        # For logging
        print("=" * 50)
        print(f"ANALYSIS RESULT: {classification} - {specific_type}")
        print("=" * 50)

        # Render with both classification and specific type for display
        return render(request, 'hand.html', {
            'api_result_hand': specific_type,
            'classification': classification
        })

    return render(request, 'hand.html')

def chatbot_api_hand(request):
    user_input = request.GET.get("message", "").lower().strip()
    
    # Get the current analysis result from session
    result_info = request.session.get("analysis_result_hand", {})
    if isinstance(result_info, str):  # Handle old session format for backward compatibility
        classification = 'unknown'
        specific_type = result_info
    else:
        classification = result_info.get('classification', 'unknown')
        specific_type = result_info.get('specific_type', 'unknown')
    
    # Select the appropriate keywords dictionary based on classification and type
    if classification in IMAGE_CLASSIFICATIONS and specific_type in IMAGE_CLASSIFICATIONS[classification]:
        keywords = {**IMAGE_CLASSIFICATIONS[classification][specific_type], **general_keywords}
    else:
        keywords = general_keywords
    
    # Find matching response
    response = "Sorry, I don't have specific information about that. Try asking about elements related to your scan result."
    for keyword, answer in keywords.items():
        if keyword in user_input:
            response = answer
            break

    # Include the classification info in the response for context
    result_display = f"{classification} - {specific_type}" if classification != 'unknown' else ""
    result_info = f"Based on your {result_display} scan result: " if result_display else ""
    
    return JsonResponse({"response": f"{result_info}{response}"})