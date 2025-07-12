#!/usr/bin/env python3
"""
Example usage of NSFW Detector

This script demonstrates how to use the NSFW detector for:
- Single image classification
- Batch image processing
- Directory scanning
- Custom threshold settings
"""

import os
import sys
from nsfw_detector import predict

def main():
    print("🔥 NSFW Detector - Example Usage")
    print("="*50)
    
    # Load model
    try:
        model = predict.load_model()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("Make sure the model file is in the correct location:")
        print("models/mobilenet_v2_140_224/saved_model.h5")
        sys.exit(1)
    
    # Example 1: Single image classification
    print("\n📸 Example 1: Single Image Classification")
    print("-" * 40)
    
    # Create a test image path (you can replace this with your image)
    test_image = "test_image.jpg"
    
    if os.path.exists(test_image):
        try:
            result = predict.classify(model, test_image)
            
            if test_image in result:
                scores = result[test_image]
                if "error" not in scores:
                    print(f"Image: {test_image}")
                    print(f"Scores: {scores}")
                    
                    # Calculate NSFW score
                    nsfw_score = predict.get_nsfw_score(scores)
                    print(f"NSFW Score: {nsfw_score:.4f}")
                    
                    # Check if NSFW with default threshold
                    is_nsfw = predict.is_nsfw(scores)
                    print(f"Is NSFW (threshold=0.5): {is_nsfw}")
                    
                    # Check with custom threshold
                    is_nsfw_strict = predict.is_nsfw(scores, threshold=0.3)
                    print(f"Is NSFW (threshold=0.3): {is_nsfw_strict}")
                    
                    # Find highest scoring class
                    max_class = max(scores, key=scores.get)
                    print(f"Predicted class: {max_class} ({scores[max_class]:.4f})")
                else:
                    print(f"Error processing {test_image}: {scores['error']}")
            else:
                print(f"No results for {test_image}")
                
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Test image not found: {test_image}")
        print("Place a test image in the current directory to see this example.")
    
    # Example 2: Batch processing
    print("\n📁 Example 2: Batch Processing")
    print("-" * 40)
    
    # List of image files (replace with your images)
    image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]
    existing_files = [f for f in image_files if os.path.exists(f)]
    
    if existing_files:
        try:
            results = predict.classify(model, existing_files)
            
            for filename, scores in results.items():
                if "error" not in scores:
                    nsfw_score = predict.get_nsfw_score(scores)
                    is_nsfw = predict.is_nsfw(scores)
                    max_class = max(scores, key=scores.get)
                    
                    print(f"📄 {filename}:")
                    print(f"  NSFW Score: {nsfw_score:.4f}")
                    print(f"  Is NSFW: {is_nsfw}")
                    print(f"  Predicted: {max_class} ({scores[max_class]:.4f})")
                else:
                    print(f"📄 {filename}: Error - {scores['error']}")
                    
        except Exception as e:
            print(f"Error in batch processing: {e}")
    else:
        print("No image files found for batch processing.")
        print("Add some image files to the current directory to see this example.")
    
    # Example 3: Directory scanning
    print("\n🔍 Example 3: Directory Scanning")
    print("-" * 40)
    
    # Scan current directory for images
    current_dir = "."
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    image_files = []
    for file in os.listdir(current_dir):
        if any(file.lower().endswith(ext) for ext in supported_extensions):
            image_files.append(file)
    
    if image_files:
        print(f"Found {len(image_files)} image files in current directory:")
        for img in image_files[:5]:  # Show first 5
            print(f"  - {img}")
        
        if len(image_files) > 5:
            print(f"  ... and {len(image_files) - 5} more")
        
        try:
            results = predict.classify(model, current_dir)
            
            nsfw_count = 0
            for filename, scores in results.items():
                if "error" not in scores:
                    if predict.is_nsfw(scores):
                        nsfw_count += 1
            
            print(f"📊 Summary:")
            print(f"  Total images processed: {len(results)}")
            print(f"  NSFW images detected: {nsfw_count}")
            print(f"  Safe images: {len(results) - nsfw_count}")
            
        except Exception as e:
            print(f"Error scanning directory: {e}")
    else:
        print("No image files found in current directory.")
    
    # Example 4: Custom threshold examples
    print("\n⚙️ Example 4: Custom Threshold Examples")
    print("-" * 40)
    
    # Simulate some scores for demonstration
    demo_scores = {
        "drawings": 0.1,
        "hentai": 0.2,
        "neutral": 0.3,
        "porn": 0.15,
        "sexy": 0.25
    }
    
    print("Demo scores:", demo_scores)
    
    nsfw_score = predict.get_nsfw_score(demo_scores)
    print(f"NSFW Score: {nsfw_score:.3f}")
    
    thresholds = [0.3, 0.5, 0.7, 0.9]
    for threshold in thresholds:
        is_nsfw = predict.is_nsfw(demo_scores, threshold=threshold)
        print(f"  Threshold {threshold}: {'NSFW' if is_nsfw else 'Safe'}")
    
    print("\n🎉 Examples completed!")
    print("For more information, check the README.md file.")

if __name__ == "__main__":
    main() 