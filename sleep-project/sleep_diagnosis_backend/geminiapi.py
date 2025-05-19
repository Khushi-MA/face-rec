from google.generativeai import GenerativeModel, Part

# Assuming you have your API key configured
model = GenerativeModel('gemini-pro') # Or a more suitable model

sleep_time = "11:00 PM to 7:00 AM"
snoring = "Frequent and loud"
other_info = "Feels tired during the day, has morning headaches"

prompt = f"""Analyze the following sleep information and provide a potential diagnosis or assessment of a possible sleep disorder:

Sleep Time: {sleep_time}
Snoring: {snoring}
Other Information: {other_info}
"""

response = model.generate_content(prompt)
diagnosis = response.text
print(diagnosis)

# Send the 'diagnosis' back to the frontend