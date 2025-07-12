from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import io
import requests
from PIL import Image
import tempfile
import logging
from nsfw_detector import predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

MODEL_PATH = "models/mobilenet_v2_140_224/saved_model.h5"
model = None

def initialize_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = predict.load_model(MODEL_PATH)
            logger.info("Model loaded successfully!")
        else:
            logger.error(f"Model file not found: {MODEL_PATH}")
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

initialize_model()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_image_from_url(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            raise ValueError("URL does not point to an image file")
        
        image = Image.open(io.BytesIO(response.content))
        return image
        
    except Exception as e:
        logger.error(f"Error downloading image from URL: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "NSFW Detector API",
        "version": "1.0.0",
        "endpoints": {
            "POST /predict": "Upload file for NSFW prediction",
            "POST /predict_url": "Predict NSFW from image URL",
            "POST /predict_batch": "Batch prediction with multiple files",
            "GET /health": "Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    try:
        if model is None:
            return jsonify({"status": "error", "message": "Model not loaded"}), 503
        
        return jsonify({"status": "healthy", "message": "API is running"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file found"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image = Image.open(file.stream)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(tmp_file.name, 'JPEG')
            
            predictions = predict.classify(model, tmp_file.name)
            os.unlink(tmp_file.name)
            
            filename = os.path.basename(tmp_file.name)
            if filename in predictions:
                scores = predictions[filename]
                if "error" not in scores:
                    nsfw_score = predict.get_nsfw_score(scores)
                    is_nsfw = predict.is_nsfw(scores)
                    
                    max_class = max(scores, key=scores.get)
                    max_confidence = scores[max_class]
                    
                    result = {
                        "is_nsfw": is_nsfw,
                        "nsfw_score": nsfw_score,
                        "predicted_class": max_class,
                        "confidence": max_confidence,
                        "scores": scores
                    }
                else:
                    result = {"error": scores["error"]}
            else:
                result = {"error": "Prediction failed"}
            
            return jsonify({
                "success": True,
                "filename": file.filename,
                "result": result
            })
            
    except Exception as e:
        logger.error(f"File prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict_url', methods=['POST'])
def predict_url():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL required"}), 400
        
        url = data['url']
        image = download_image_from_url(url)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(tmp_file.name, 'JPEG')
            
            predictions = predict.classify(model, tmp_file.name)
            os.unlink(tmp_file.name)
            
            filename = os.path.basename(tmp_file.name)
            if filename in predictions:
                scores = predictions[filename]
                if "error" not in scores:
                    nsfw_score = predict.get_nsfw_score(scores)
                    is_nsfw = predict.is_nsfw(scores)
                    
                    max_class = max(scores, key=scores.get)
                    max_confidence = scores[max_class]
                    
                    result = {
                        "is_nsfw": is_nsfw,
                        "nsfw_score": nsfw_score,
                        "predicted_class": max_class,
                        "confidence": max_confidence,
                        "scores": scores
                    }
                else:
                    result = {"error": scores["error"]}
            else:
                result = {"error": "Prediction failed"}
            
            return jsonify({
                "success": True,
                "url": url,
                "result": result
            })
            
    except Exception as e:
        logger.error(f"URL prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files found"}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No files selected"}), 400
        
        results = []
        
        for file in files:
            try:
                if file.filename == '' or not allowed_file(file.filename):
                    results.append({
                        "filename": file.filename,
                        "error": "Invalid file"
                    })
                    continue
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    image = Image.open(file.stream)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(tmp_file.name, 'JPEG')
                    
                    predictions = predict.classify(model, tmp_file.name)
                    os.unlink(tmp_file.name)
                    
                    tmp_filename = os.path.basename(tmp_file.name)
                    if tmp_filename in predictions:
                        scores = predictions[tmp_filename]
                        if "error" not in scores:
                            nsfw_score = predict.get_nsfw_score(scores)
                            is_nsfw = predict.is_nsfw(scores)
                            
                            max_class = max(scores, key=scores.get)
                            max_confidence = scores[max_class]
                            
                            result = {
                                "is_nsfw": is_nsfw,
                                "nsfw_score": nsfw_score,
                                "predicted_class": max_class,
                                "confidence": max_confidence,
                                "scores": scores
                            }
                        else:
                            result = {"error": scores["error"]}
                    else:
                        result = {"error": "Prediction failed"}
                    
                    results.append({
                        "filename": file.filename,
                        "result": result
                    })
                    
            except Exception as e:
                logger.error(f"Prediction error for file {file.filename}: {e}")
                results.append({
                    "filename": file.filename,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "total_files": len(files),
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            "model_path": MODEL_PATH,
            "classes": ["drawings", "hentai", "neutral", "porn", "sexy"],
            "input_size": [224, 224],
            "model_loaded": model is not None,
            "version": "1.0.0"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File too large (maximum 16MB)"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting NSFW Detector API...")
    print("📡 Endpoints:")
    print("  POST /predict - Upload file for prediction")
    print("  POST /predict_url - Predict from image URL")
    print("  POST /predict_batch - Batch prediction")
    print("  GET /health - Health check")
    print("  GET /stats - Model statistics")
    print("  GET / - API information")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 