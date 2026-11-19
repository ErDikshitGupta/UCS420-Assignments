"""
Cognitive Computing Assignment - Question 1
Medicine Bottle Label Reader using OCR

Install Python packages:
    pip install opencv-python pytesseract pillow

Also install the Tesseract OCR application:
    Windows: https://github.com/UB-Mannheim/tesseract/wiki

If Tesseract is not in PATH, uncomment and edit the line below.
"""
import re
from pathlib import Path

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from tkinter import Tk, filedialog

# For Windows, edit this path if Tesseract is not detected:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def select_image():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Choose a medicine bottle label image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
    )
    root.destroy()
    return path


def preprocess_image(path):
    """Enlarge and improve the label image before OCR."""
    image = Image.open(path).convert("RGB")
    if image.width < 1400:
        ratio = 1400 / image.width
        image = image.resize((1400, int(image.height * ratio)))
    image = ImageEnhance.Contrast(image).enhance(1.7)
    image = ImageEnhance.Sharpness(image).enhance(1.5)
    image = image.convert("L")
    return image.filter(ImageFilter.MedianFilter(size=3))


def extract_details(text):
    """Find common medicine-label fields from the OCR text."""
    patterns = {
        "Expiry date": r"(?:exp(?:iry)?\.?\s*(?:date)?|use\s*before)\s*[:\-]?\s*([A-Za-z]{3,9}\s*[-/]?\s*\d{2,4}|\d{1,2}[/-]\d{2,4})",
        "Manufacturing date": r"(?:mfg|manufactured)\.?\s*(?:date)?\s*[:\-]?\s*([A-Za-z]{3,9}\s*[-/]?\s*\d{2,4}|\d{1,2}[/-]\d{2,4})",
        "Batch number": r"(?:batch\s*(?:no\.?|number)?|b\.?\s*no\.?)\s*[:\-]?\s*([A-Z0-9/-]+)",
        "Strength / dosage": r"\b(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|%))\b",
    }

    details = {}
    for label, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        details[label] = match.group(1).strip() if match else "Not detected"

    # OCR cannot reliably identify the medicine name in every label.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    possible_name = "Not confidently identified"
    excluded = ("composition", "dosage", "store", "warning", "manufactured",
                "batch", "expiry", "each tablet", "keep")
    for line in lines:
        if len(line) >= 3 and not any(word in line.lower() for word in excluded):
            possible_name = line
            break
    details["Possible medicine name (verify)"] = possible_name
    return details


def main():
    print("MEDICINE BOTTLE LABEL READER")
    print("--------------------------------")
    image_path = select_image()
    if not image_path:
        print("No image selected.")
        return

    try:
        processed = preprocess_image(image_path)
        extracted_text = pytesseract.image_to_string(
            processed, config="--oem 3 --psm 6"
        )

        print("\nTEXT READ FROM LABEL:\n")
        print(extracted_text if extracted_text.strip() else "No text detected.")

        print("\nINFORMATION DETECTED:\n")
        details = extract_details(extracted_text)
        for key, value in details.items():
            print(f"{key}: {value}")

        report_path = Path(image_path).with_name(
            Path(image_path).stem + "_medicine_report.txt"
        )
        with open(report_path, "w", encoding="utf-8") as report:
            report.write("MEDICINE BOTTLE LABEL READER REPORT\n\n")
            report.write("OCR TEXT:\n" + extracted_text + "\n\n")
            report.write("EXTRACTED DETAILS:\n")
            for key, value in details.items():
                report.write(f"{key}: {value}\n")

        print(f"\nReport saved at: {report_path}")
        print("\nSafety: OCR may make mistakes. Verify all details on the actual")
        print("medicine packaging and ask a pharmacist/doctor before use.")
    except pytesseract.TesseractNotFoundError:
        print("Tesseract OCR was not found. Install Tesseract and add it to PATH.")
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
