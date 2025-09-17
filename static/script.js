// This event listener ensures that the JavaScript code only runs
// after the entire HTML document has been loaded and is ready.
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Element References ---
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-btn');
    const analyzeButton = document.getElementById('analyze-btn');
    const uploadButton = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const previewImage = document.getElementById('preview-img');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const confidenceText = document.getElementById('confidence-text');
    const loader = document.getElementById('loader');
    const cameraContainer = document.getElementById('camera-container');
    const errorMessageDiv = document.getElementById('error-message');
    const useCameraButton = document.getElementById('use-camera-btn');
    const uploadSection = document.getElementById('upload-section');
    const startOverButton = document.getElementById('start-over-btn'); // New button

    let stream; // To hold the camera stream

    // --- UI State Management ---
    function resetUI() {
        // Hide all conditional elements
        cameraContainer.classList.add('hidden');
        imagePreview.classList.add('hidden');
        captureButton.classList.add('hidden');
        analyzeButton.classList.add('hidden');
        resultDiv.classList.add('hidden');
        errorMessageDiv.classList.add('hidden');
        loader.classList.add('hidden');

        // Show the initial upload/camera choice
        uploadSection.classList.remove('hidden');

        // Stop camera stream if it's running
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }

    // --- Camera Functions ---
    async function startCamera() {
        resetUI();
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            video.srcObject = stream;
            cameraContainer.classList.remove('hidden');
            captureButton.classList.remove('hidden');
            uploadSection.classList.add('hidden');
        } catch (err) {
            console.error("Error accessing camera:", err);
            let userMessage = "Could not access camera. Please ensure it is connected and you have granted permission.";
            if (err.name === "NotAllowedError") {
                userMessage = "Camera access was denied. Please allow camera access in your browser settings.";
            }
            displayError(userMessage);
        }
    }

    function captureImage() {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        previewImage.src = canvas.toDataURL('image/jpeg');
        imagePreview.classList.remove('hidden');
        analyzeButton.classList.remove('hidden');
        captureButton.classList.add('hidden');
        cameraContainer.classList.add('hidden');

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }

    // --- Image Analysis Functions ---
    async function analyzeImage() {
        loader.classList.remove('hidden');
        analyzeButton.classList.add('hidden');
        errorMessageDiv.classList.add('hidden');
        resultDiv.classList.add('hidden');

        const blob = await (await fetch(previewImage.src)).blob();
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error analyzing image:', error);
            displayError(error.message || "An unknown error occurred.");
            startOverButton.classList.remove('hidden'); // Show start over even on error
        } finally {
            loader.classList.add('hidden');
        }
    }

    function displayResults(data) {
        resultText.textContent = `Prediction: ${data.prediction}`;
        confidenceText.textContent = `Confidence: ${data.confidence.toFixed(2)}%`;
        resultDiv.classList.remove('hidden');
    }

    function displayError(message) {
        errorMessageDiv.textContent = `Error: ${message}`;
        errorMessageDiv.classList.remove('hidden');
        // Also show the start over button when an error occurs
        resultDiv.classList.remove('hidden');
        resultText.textContent = 'Analysis Failed';
        confidenceText.textContent = '';
    }

    // --- Event Listeners ---
    useCameraButton.addEventListener('click', startCamera);
    captureButton.addEventListener('click', captureImage);
    analyzeButton.addEventListener('click', analyzeImage);
    uploadButton.addEventListener('click', () => fileInput.click());
    startOverButton.addEventListener('click', resetUI); // New listener

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                resetUI();
                previewImage.src = e.target.result;
                imagePreview.classList.remove('hidden');
                analyzeButton.classList.remove('hidden');
                uploadSection.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    // Initial state setup
    resetUI();
});

