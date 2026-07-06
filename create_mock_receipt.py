from PIL import Image, ImageDraw, ImageFont
import os

def generate_image(filename, items, subtotal, tax, total):
    img = Image.new('RGB', (400, 600), color='white')
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
        title_font = font

    d.text((120, 20), "BISTRO CAFE", fill="black", font=title_font)
    d.text((20, 80), "Date: 2026-06-20", fill="black", font=font)
    d.text((20, 110), "Server: John Doe (Phone: 555-0199)", fill="black", font=font)
    
    d.text((20, 160), "--------------------------------", fill="black", font=font)
    
    y_pos = 190
    for item in items:
        d.text((20, y_pos), item, fill="black", font=font)
        y_pos += 30
        
    d.text((20, y_pos), "--------------------------------", fill="black", font=font)
    y_pos += 40
    
    d.text((20, y_pos), f"Subtotal:           ${subtotal:.2f}", fill="black", font=font)
    y_pos += 30
    d.text((20, y_pos), f"Tax:                ${tax:.2f}", fill="black", font=font)
    y_pos += 40
    d.text((20, y_pos), f"TOTAL:              ${total:.2f}", fill="black", font=title_font)
    
    y_pos += 60
    d.text((20, y_pos), "Paid via Visa ending in 1234", fill="black", font=font)
    
    img.save(filename)
    print(f"Generated: {filename}")

if __name__ == "__main__":
    # 1. Valid Receipt (Under $50, no alcohol)
    valid_items = [
        "1x Coffee            $4.50",
        "1x Sandwich          $12.50",
        "1x Salad             $9.00"
    ]
    generate_image("receipt_valid.jpg", valid_items, 26.00, 2.08, 28.08)
    
    # 2. Violation Receipt (Over $50 AND contains Alcohol)
    violation_items = [
        "1x Steak             $45.00",
        "2x Craft Beer        $16.00",
        "1x Dessert           $12.00"
    ]
    generate_image("receipt_violation.jpg", violation_items, 73.00, 5.84, 78.84)
