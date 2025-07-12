import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NSFWDetector:
    def __init__(self, model_path="models/mobilenet_v2_140_224"):
        self.model_path = model_path
        self.model = None
        self.classes = ["drawings", "hentai", "neutral", "porn", "sexy"]
        self.input_size = (224, 224)
        self.load_model()
    
    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = keras.layers.TFSMLayer(self.model_path, call_endpoint='serving_default')
                logger.info(f"Model loaded successfully: {self.model_path}")
            else:
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image_path):
        try:
            if isinstance(image_path, str):
                image = Image.open(image_path)
            else:
                image = image_path
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image = image.resize(self.input_size)
            image_array = np.array(image)
            image_array = image_array.astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Image preprocessing error: {e}")
            raise
    
    def predict(self, image_path):
        try:
            processed_image = self.preprocess_image(image_path)
            predictions = self.model(processed_image)
            
            if isinstance(predictions, dict):
                pred_array = next(iter(predictions.values()))
            else:
                pred_array = predictions
            
            if hasattr(pred_array, 'numpy'):
                pred_array = pred_array.numpy()
            
            results = {}
            for i, class_name in enumerate(self.classes):
                results[class_name] = float(pred_array[0][i])
            
            max_class = max(results, key=results.get)
            max_score = results[max_class]
            
            nsfw_classes = ["hentai", "porn", "sexy"]
            is_nsfw = max_class in nsfw_classes
            
            return {
                "is_nsfw": is_nsfw,
                "predicted_class": max_class,
                "confidence": max_score,
                "scores": results
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def predict_batch(self, image_paths):
        results = []
        for image_path in image_paths:
            try:
                result = self.predict(image_path)
                result["image_path"] = image_path
                results.append(result)
            except Exception as e:
                logger.error(f"Prediction error for image {image_path}: {e}")
                results.append({
                    "image_path": image_path,
                    "error": str(e)
                })
        
        return results

_detector = None

def get_detector():
    global _detector
    if _detector is None:
        _detector = NSFWDetector()
    return _detector

class predict:
    
    @staticmethod
    def load_model(model_path="models/mobilenet_v2_140_224"):
        return NSFWDetector(model_path)
    
    @staticmethod
    def classify(model_or_path, image_input):
        if isinstance(model_or_path, str):
            detector = NSFWDetector(model_or_path)
        else:
            detector = model_or_path
        
        results = {}
        
        if isinstance(image_input, str):
            if os.path.isdir(image_input):
                supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
                image_files = []
                for file in os.listdir(image_input):
                    if any(file.lower().endswith(ext) for ext in supported_extensions):
                        image_files.append(os.path.join(image_input, file))
                
                for image_path in image_files:
                    try:
                        result = detector.predict(image_path)
                        results[os.path.basename(image_path)] = result['scores']
                    except Exception as e:
                        results[os.path.basename(image_path)] = {"error": str(e)}
            else:
                try:
                    result = detector.predict(image_input)
                    results[os.path.basename(image_input)] = result['scores']
                except Exception as e:
                    results[os.path.basename(image_input)] = {"error": str(e)}
        
        elif isinstance(image_input, list):
            for image_path in image_input:
                try:
                    result = detector.predict(image_path)
                    results[os.path.basename(image_path)] = result['scores']
                except Exception as e:
                    results[os.path.basename(image_path)] = {"error": str(e)}
        
        return results
    
    @staticmethod
    def get_nsfw_score(scores):
        if "error" in scores:
            return 0.0
        
        nsfw_classes = ["hentai", "porn", "sexy"]
        nsfw_score = sum(scores.get(cls, 0) for cls in nsfw_classes)
        return nsfw_score
    
    @staticmethod
    def is_nsfw(scores, threshold=0.5):
        if "error" in scores:
            return False
        
        nsfw_score = predict.get_nsfw_score(scores)
        return nsfw_score >= threshold

if __name__ == "__main__":
    detector = NSFWDetector()
    
    test_image = "test_image.jpg"
    if os.path.exists(test_image):
        try:
            result = detector.predict(test_image)
            print("Test results:")
            print(f"NSFW: {result['is_nsfw']}")
            print(f"Class: {result['predicted_class']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print("All scores:")
            for class_name, score in result['scores'].items():
                print(f"  {class_name}: {score:.4f}")
        except Exception as e:
            print(f"Test error: {e}")
    else:
        print(f"Test image not found: {test_image}") 