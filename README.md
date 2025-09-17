🥥 CocoNUTS - AI-Powered Coconut Health Analyzer
A web-based application that leverages deep learning to detect common diseases in coconut palm trees. Users can analyze the health of a coconut leaf in real-time using their device's camera or by uploading an image. This tool is designed to provide farmers and agricultural professionals with a quick, accessible way to diagnose potential issues.



✨ Key Features
Live Camera Analysis: Use your mobile or desktop camera to get an instant diagnosis in the field.

Image Upload: Analyze existing photos of coconut leaves from your device.

AI-Powered Detection: Utilizes a Convolutional Neural Network (CNN) trained on the MobileNetV2 architecture to accurately identify 5 different types of coconut diseases.

Responsive Design: A clean, intuitive, and mobile-first interface for easy use on any device.

Containerized & Deployable: Fully containerized with Docker for consistent, reliable deployment on cloud services like Render.

🛠️ Technology Stack
Backend: Python, Flask

AI / Machine Learning: TensorFlow, Keras (with MobileNetV2 for transfer learning)

Frontend: HTML5, CSS3, JavaScript

Deployment: Docker, Gunicorn, Render

Development Tools: Git, Git LFS

📂 Project Structure
The project is organized into a unified Flask application that serves both the frontend and the AI backend.

/CocoNUTS/
|-- app.py                  # Main Flask server (handles frontend, API, and AI)
|-- model_trainer.py        # Script to train the AI model
|-- prepare_dataset.py      # Script to split the dataset for training
|-- requirements.txt        # Python dependencies
|-- Dockerfile              # Instructions for building the Docker container
|-- README.md               # You are here!
|-- static/                 # All frontend files
    |-- index.html
    |-- style.css
    |-- script.js
|-- Coconut_Tree_Disease_Dataset/   # The raw image dataset (ignored by Git)
|-- Coconut_Dataset_Split/          # The split dataset (ignored by Git)
|-- coconut_disease_model.h5        # The trained model file (tracked by Git LFS)

🚀 Setup and Installation Guide
Follow these steps to set up and run the project on your local machine.

Prerequisites
Python 3.9+

Git

Git LFS (Large File Storage) - Download & Install

Step 1: Clone the Repository
First, clone the project from GitHub. The --clone flag for LFS will ensure the large model file is downloaded correctly.

# Initialize Git LFS on your machine (only needs to be done once)
git lfs install

# Clone the repository
git clone [https://github.com/YOUR_USERNAME/CocoNUTS.git](https://github.com/YOUR_USERNAME/CocoNUTS.git)
cd CocoNUTS

Step 2: Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

Step 3: Install Dependencies
Install all the required Python libraries.

pip install -r requirements.txt

Step 4: Download the Dataset (Optional - For Retraining)
If you want to retrain the model yourself, you need to download the dataset.

Download the "Coconut Tree Disease Dataset" from Mendeley Data.

Unzip the file and ensure the disease folders (Bud_Rot, Gray_Leaf_Spot, etc.) are placed directly inside a folder named Coconut_Tree_Disease_Dataset in the project root.

Step 5: Prepare and Train the Model (Optional)
If you have downloaded the dataset, you can run these scripts to generate a new coconut_disease_model.h5 file.

# 1. Split the dataset into training and validation sets
python prepare_dataset.py

# 2. Train the new, optimized model
python model_trainer.py

Step 6: Run the Application
Start the Flask server.

python app.py

You will see a message in your terminal confirming the server has started.

ใช้งาน Usage
Once the server is running, open your web browser.

Navigate to the following address:
http://127.0.0.1:5000

Use the on-screen buttons to either start your camera or upload an image file.

Click "Analyze" to get a prediction from the AI model.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
