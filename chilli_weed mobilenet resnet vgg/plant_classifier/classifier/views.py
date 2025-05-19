from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import numpy as np
import os

# Paths for the models
models = {
    "MobileNet V2": load_model("C:/Users/HP/Documents/sudeepdocs/Haegl/plants.h5"),
    "ResNet 50": load_model("C:/Users/HP/Documents/sudeepdocs/Haegl/resnet_model.h5"),
    "VGG 16": load_model("C:/Users/HP/Documents/sudeepdocs/Haegl/vgg_model.h5")
}

# Class names
class_names = ["Alternanthera caracasana", "Holy basil", "Radish Sango", "Zoztera marina"]

# Function to classify the uploaded image
def classify_image(request):
    predictions = []
    file_url = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Save the uploaded file to the media directory
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image_file.name, image_file)
        file_url = fs.url(filename)

        # Load and preprocess the image
        img = load_img(os.path.join(settings.MEDIA_ROOT, filename), target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Generate predictions from all models
        for model_name, model in models.items():
            model_predictions = model.predict(img_array)
            predicted_class = class_names[model_predictions.argmax()]
            predictions.append({"model_name": model_name, "prediction": predicted_class})

    # Render the template with context
    return render(request, 'classifier.html', {
        'predictions': predictions,
        'file_url': file_url
    })
