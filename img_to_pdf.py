import argparse
from PIL import Image
import os
import sys
from datetime import datetime

def get_timestamped_filename(base_path, prefix=''):
    """Generate a unique filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    directory = os.path.dirname(base_path) or '.'
    base_name = os.path.basename(base_path)
    name, _ = os.path.splitext(base_name)  # Ignore original extension
    
    # Always use .pdf extension for output
    return os.path.join(directory, f"{prefix}{name}_{timestamp}.pdf")

def convert_image_to_pdf(image_path, output_path=None):
    try:
        # Open the image
        with Image.open(image_path) as image:
            # If no output path specified, use the same name as input with timestamp
            if output_path is None:
                output_path = get_timestamped_filename(image_path)
            
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

def convert_images_from_folder(folder_path, output_path=None):
    try:
        # Get all image files from the folder
        image_files = []
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')
        
        for file in os.listdir(folder_path):
            if file.lower().endswith(valid_extensions):
                image_files.append(os.path.join(folder_path, file))
        
        if not image_files:
            print(f"No valid image files found in {folder_path}", file=sys.stderr)
            return False
            
        # Sort files to ensure consistent ordering
        image_files.sort()
        
        # If no output path specified, use the folder name with timestamp
        if output_path is None:
            folder_name = os.path.basename(folder_path.rstrip('/\\'))
            output_path = get_timestamped_filename(
                os.path.join(folder_path, folder_name),
                prefix='combined_'
            )
        
        images = []
        # Open and convert all images
        for img_path in image_files:
            with Image.open(img_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Create a copy of the image to avoid closure issues
                images.append(img.copy())
        
        # Save all images to PDF
        if images:
            images[0].save(output_path, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])
            print(f"Successfully combined {len(image_files)} images into {output_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error combining images: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert image(s) to PDF')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--image', help='Path to the input image file')
    group.add_argument('-f', '--folder', help='Path to folder containing images to combine')
    parser.add_argument('-o', '--output', help='Path for the output PDF file (optional)')
    
    args = parser.parse_args()
    
    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file '{args.image}' does not exist", file=sys.stderr)
            sys.exit(1)
        success = convert_image_to_pdf(args.image, args.output)
    else:
        if not os.path.exists(args.folder):
            print(f"Error: Folder '{args.folder}' does not exist", file=sys.stderr)
            sys.exit(1)
        success = convert_images_from_folder(args.folder, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
