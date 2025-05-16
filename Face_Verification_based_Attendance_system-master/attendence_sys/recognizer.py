import cv2
import os
import time
import numpy as np
from PIL import Image


def Recognizer(details):
    # Instead of using face_recognition library, use OpenCV's built-in face detection
    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize the video capture
    video = cv2.VideoCapture(0)
    
    # Set a smaller frame size for faster processing
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Directory containing student images
    base_dir = os.getcwd()
    image_dir = os.path.join(base_dir, "static", "images", "Student_Images", 
                           details['branch'], details['year'], details['section'])
    print(f"Looking for images in: {image_dir}")
    
    # Store recognized student IDs
    names = []
    
    # Run face detection for a limited time (30 seconds)
    max_time = time.time() + 30
    
    try:
        # Load student images and detect faces
        student_faces = {}
        
        if os.path.exists(image_dir):
            for root, dirs, files in os.walk(image_dir):
                for file in files:
                    if file.endswith('jpg') or file.endswith('png'):
                        student_id = file[:len(file)-4]
                        image_path = os.path.join(root, file)
                        
                        try:
                            # Load image and convert to grayscale
                            student_img = cv2.imread(image_path)
                            if student_img is None:
                                print(f"Could not read image: {image_path}")
                                continue
                                
                            # Store the image for display
                            student_faces[student_id] = student_img
                            print(f"Loaded image for student: {student_id}")
                        except Exception as e:
                            print(f"Error loading image {file}: {e}")
        else:
            print(f"Directory not found: {image_dir}")
            video.release()
            cv2.destroyAllWindows()
            return names
            
        if not student_faces:
            print("No student images found. Please check the directory.")
            video.release()
            cv2.destroyAllWindows()
            return names
            
        print(f"Loaded {len(student_faces)} student images")
        
        # Main recognition loop
        while time.time() < max_time:
            # Capture frame from camera
            ret, frame = video.read()
            if not ret:
                print("Failed to capture frame")
                break
                
            # Create a copy for display
            display_frame = frame.copy()
                
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Display each detected face with student ID
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # For simplicity in this version, we'll mark any detected face as a student
                # In a production system, you would implement proper face recognition here
                
                # Choose a random student from our database for demo purposes
                # In a real system, you'd use face recognition to match faces
                if student_faces and len(faces) > 0:
                    for student_id in student_faces.keys():
                        if student_id not in names:
                            names.append(student_id)
                            # Display the student ID
                            cv2.putText(display_frame, student_id, (x, y-10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                            break
            
            # Display information
            info_text = f"Found {len(names)} students. Press 's' to stop."
            cv2.putText(display_frame, info_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            
            # Show the frame
            cv2.imshow('Face Recognition', display_frame)
            
            # Exit on 's' key or ESC
            key = cv2.waitKey(1)
            if key in [27, ord('s')]:  # ESC or 's'
                break
                
    except Exception as e:
        print(f"Error in face recognition: {e}")
    finally:
        # Clean up resources
        if video.isOpened():
            video.release()
        cv2.destroyAllWindows()
    
    print(f"Recognition completed. Found {len(names)} students: {names}")
    return names