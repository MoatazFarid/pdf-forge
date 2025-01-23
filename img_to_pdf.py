import argparse
from PIL import Image
import os
import sys

def convert_image_to_pdf(image_path, output_path=None):
    try:
        # Open the image
        with Image.open(image_path) as image:
            # If no output path specified, use the same name as input with .pdf extension
            if output_path is None:
                output_path = os.path.splitext(image_path)[0] + '.pdf'
            
            # Convert image to RGB if it's not
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save as PDF
            image.save(output_path, 'PDF', resolution=100.0)
            print(f"Successfully converted {image_path} to {output_path}")
            return True
    except Exception as e:
        print(f"Error converting image: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert an image to PDF')
    parser.add_argument('image_path', help='Path to the input image file')
    parser.add_argument('-o', '--output', help='Path for the output PDF file (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file '{args.image_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    success = convert_image_to_pdf(args.image_path, args.output)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
