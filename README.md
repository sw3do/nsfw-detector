# 🔥 NSFW Detector

A Python library and REST API for detecting NSFW (Not Safe For Work) content in images using TensorFlow/Keras.

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

</div>

## ✨ Features

- **🎯 5-Class Detection**: drawings, hentai, neutral, porn, sexy
- **📸 Single Image Analysis**: Quickly analyze individual images
- **📁 Batch Processing**: Process multiple images simultaneously
- **🔄 Directory Scanning**: Automatically scan entire folders
- **🌐 REST API**: HTTP endpoints for easy integration
- **📊 NSFW Score**: Probability score from 0-1
- **⚙️ Flexible Threshold**: Customizable NSFW threshold values

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Model Setup

Place your H5 model file at `models/mobilenet_v2_140_224/saved_model.h5`

### Basic Usage

```python
from nsfw_detector import predict

# Load model
model = predict.load_model('models/mobilenet_v2_140_224/saved_model.h5')

# Single image prediction
result = predict.classify(model, 'image.jpg')
print(result)

# Get NSFW score
scores = result['image.jpg']
nsfw_score = predict.get_nsfw_score(scores)  # 0.148
is_nsfw = predict.is_nsfw(scores)  # False (threshold: 0.5)
```

## 📡 API Server

### Start the Server

```bash
python api_server.py
```

Server runs on `http://localhost:5000`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/stats` | Model statistics |
| `POST` | `/predict` | Upload file for prediction |
| `POST` | `/predict_url` | Predict from image URL |
| `POST` | `/predict_batch` | Batch prediction |

### Example Usage

**Upload File**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/predict
```

**Predict from URL**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"url":"https://example.com/image.jpg"}' \
     http://localhost:5000/predict_url
```

**Batch Processing**
```bash
curl -X POST -F "files=@img1.jpg" -F "files=@img2.jpg" \
     http://localhost:5000/predict_batch
```

## 📋 API Response Format

```json
{
  "success": true,
  "filename": "image.jpg",
  "result": {
    "is_nsfw": false,
    "nsfw_score": 0.1481,
    "predicted_class": "drawings",
    "confidence": 0.8514,
    "scores": {
      "drawings": 0.85139805,
      "hentai": 0.14751932,
      "neutral": 0.00026579,
      "porn": 0.00077335,
      "sexy": 0.00004345
    }
  }
}
```

## 🏗️ Project Structure

```
nsfw-detector/
├── nsfw_detector.py        # Main detector module
├── api_server.py           # Flask REST API
├── requirements.txt        # Python dependencies
├── models/                 # Model files
│   └── mobilenet_v2_140_224/
│       └── saved_model.h5  # TensorFlow model
└── README.md              # This file
```

## 🎨 Classification Classes

| Class | Description | NSFW |
|-------|-------------|------|
| `drawings` | Drawings/animations | ❌ |
| `hentai` | Hentai content | ✅ |
| `neutral` | Neutral/normal content | ❌ |
| `porn` | Pornographic content | ✅ |
| `sexy` | Sexy/suggestive content | ✅ |

**NSFW Score**: Sum of `hentai + porn + sexy` scores

## ⚙️ Configuration

### Custom Threshold

```python
# More sensitive (detects more NSFW)
is_nsfw = predict.is_nsfw(scores, threshold=0.3)

# More tolerant (detects less NSFW)
is_nsfw = predict.is_nsfw(scores, threshold=0.8)
```

### Change API Port

```python
# In api_server.py
app.run(host='0.0.0.0', port=8080, debug=False)
```

## 🔧 Development

### Testing

```bash
# Test the detector module
python nsfw_detector.py

# Start API in debug mode
python api_server.py
```

### Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Model Information

- **Architecture**: MobileNet V2 (140, 224)
- **Input Size**: 224x224 pixels
- **Classes**: 5 (drawings, hentai, neutral, porn, sexy)
- **Framework**: TensorFlow 2.13.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TensorFlow team for the excellent ML framework
- MobileNet architecture for efficient mobile deployment
- Open source community for inspiration and tools

## ⚠️ Important Notes

- This tool is designed for content moderation purposes only
- 100% accuracy is not guaranteed
- Human review is recommended for critical applications
- Model performance may vary based on image quality and content type

## 📞 Support

For questions and support, please [open an issue](https://github.com/sw3do/nsfw-detector/issues) on GitHub.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/sw3do">sw3do</a>
</div> 