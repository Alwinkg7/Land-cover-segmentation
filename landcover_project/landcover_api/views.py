from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import torch
import numpy as np
import cv2
import segmentation_models_pytorch as smp
from segmentation_models_pytorch.decoders.unet.model import Unet  # Import Unet
from torch.serialization import add_safe_globals
from PIL import Image
import base64
from io import BytesIO

# Allowlist Unet for safe loading
add_safe_globals([Unet])

# Define class labels and colors
CLASS_LABELS = {
    0: 'Background',
    1: 'Road',
    2: 'Water',
    3: 'Woodlands',
    4: 'Buildings',
}

CLASS_COLORS = {
    0: (0, 0, 0),       # Black - Background
    1: (255, 0, 0),     # Red - Road
    2: (0, 0, 255),     # Blue - Water
    3: (0, 255, 0),     # Green - Woodlands
    4: (255, 255, 0),   # Yellow - Buildings
}

# Define encoder and preprocessing function
ENCODER = 'efficientnet-b0'
ENCODER_WEIGHTS = 'imagenet'
preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

# Load the saved model
MODEL_PATH = 'trained_landcover_unet_efficientnet-b0_epochs18_patch512_batch16.pth'
try:
    model = torch.load(MODEL_PATH, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'), weights_only=False)
    model.eval()
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise e

def preprocess_image(image):
    """
    Preprocess the input image for the model.
    """
    try:
        print("ℹ️ Preprocessing image...")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0
        image = preprocessing_fn(image)
        image = image.transpose(2, 0, 1).astype(np.float32)
        return image
    except Exception as e:
        print(f"❌ Error during image preprocessing: {e}")
        raise e

def predict(image):
    """
    Perform prediction on the input image.
    """
    try:
        print("🔄 Running model prediction...")
        preprocessed_image = preprocess_image(image)
        input_tensor = torch.from_numpy(preprocessed_image).unsqueeze(0).to('cuda' if torch.cuda.is_available() else 'cpu')
        
        with torch.no_grad():
            prediction = model(input_tensor)
        
        predicted_mask = prediction.squeeze().cpu().numpy()
        predicted_mask = np.argmax(predicted_mask, axis=0)

        print("✅ Prediction completed. Unique values in mask:", np.unique(predicted_mask))
        return predicted_mask
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        raise e

def classify_mask(predicted_mask):
    unique_classes = np.unique(predicted_mask)
    detected_classes = {int(cls): CLASS_LABELS.get(int(cls), 'Unknown') for cls in unique_classes}
    return detected_classes

def mask_to_base64(mask):
    print("🎨 Converting mask to color image...")
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    for cls, color in CLASS_COLORS.items():
        color_mask[mask == cls] = color

    # Debugging: Save the mask to check output
    cv2.imwrite("debug_mask.png", color_mask)
    print("✅ Saved debug_mask.png for verification.")

    pil_image = Image.fromarray(color_mask)
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    
    base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    print(f"✅ Mask converted to base64. Length: {len(base64_string)}")
    
    return base64_string

def image_to_base64(image):
    """
    Convert the input image to a base64 string.
    """
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

class PredictLandCover(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("📩 Received image for prediction.")
        if request.FILES.get('image'):
            file = request.FILES['image']
            npimg = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            
            if image is not None:
                print("✅ Image loaded successfully.")
                image = cv2.resize(image, (512, 512))

                # Convert input image to base64
                input_image_base64 = image_to_base64(image)

                # Debugging: Save original image
                cv2.imwrite("debug_original.png", image)
                print("✅ Saved debug_original.png for verification.")

                image = cv2.resize(image, (512, 512))
                predicted_mask = predict(image)
                classified_classes = classify_mask(predicted_mask)
                
                # Convert mask to base64
                mask_base64 = mask_to_base64(predicted_mask)

                return JsonResponse({
                    'status': 'success',
                    'classes': classified_classes,
                    'mask_image': mask_base64,
                    'input_image': input_image_base64
                })
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
