import easyocr
import re
import os

def process_meter_image(image_path):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en', 'ru']) # English and Russian for store names and digits
    
    # Read text from image
    results = reader.readtext(image_path)
    
    full_text = []
    potential_readings = []
    
    for (bbox, text, prob) in results:
        full_text.append(text)
        # Look for meter readings (e.g., 007364.26 or 7364.26)
        # We look for strings that have 5+ digits, possibly with a decimal point
        clean_text = text.replace(' ', '').replace(',', '.')
        if re.search(r'\d{4,}', clean_text):
            # Extract the first float-like number found
            num_match = re.search(r'\d+(\.\d+)?', clean_text)
            if num_match:
                potential_readings.append(float(num_match.group()))
    
    print(f"Extracted Text: {' | '.join(full_text)}")
    print(f"Potential Readings: {potential_readings}")
    
    return full_text, potential_readings

if __name__ == "__main__":
    # Test with the provided images
    img1 = "upload/IMG_4500(5).jpeg" # PANTERA
    img2 = "upload/IMG_4570(2).jpeg" # NAVROUZ
    
    if os.path.exists(img1):
        print(f"--- Processing {img1} ---")
        process_meter_image(img1)
        
    if os.path.exists(img2):
        print(f"\n--- Processing {img2} ---")
        process_meter_image(img2)
