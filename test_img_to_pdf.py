import unittest
import os
import tempfile
from PIL import Image
import re
from img_to_pdf import convert_image_to_pdf, convert_images_from_folder

class TestImageToPDF(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test image
        self.test_image_path = os.path.join(self.test_dir, 'test_image.jpg')
        self.create_test_image(self.test_image_path)
        
        # Define output PDF path
        self.output_pdf = os.path.join(self.test_dir, 'output.pdf')

    def tearDown(self):
        # Clean up test files
        for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")
        os.rmdir(self.test_dir)

    def create_test_image(self, path, mode='RGB'):
        # Create a simple test image
        image = Image.new(mode, (100, 100), 'white')
        image.save(path)

    def test_successful_conversion(self):
        """Test basic image to PDF conversion"""
        result = convert_image_to_pdf(self.test_image_path, self.output_pdf)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_pdf))
        self.assertTrue(os.path.getsize(self.output_pdf) > 0)

    def test_default_output_name(self):
        """Test conversion without specifying output path"""
        result = convert_image_to_pdf(self.test_image_path)
        self.assertTrue(result)
        
        # Find the generated PDF file
        pdf_files = [f for f in os.listdir(self.test_dir) if f.endswith('.pdf')]
        self.assertEqual(len(pdf_files), 1)
        
        # Verify filename format
        pdf_file = pdf_files[0]
        self.assertTrue(re.match(r'test_image_\d{8}_\d{6}\.pdf', pdf_file))
        
        # Verify file content
        pdf_path = os.path.join(self.test_dir, pdf_file)
        self.assertTrue(os.path.getsize(pdf_path) > 0)

    def test_non_rgb_image(self):
        """Test conversion of non-RGB image"""
        rgba_image_path = os.path.join(self.test_dir, 'rgba_image.png')
        self.create_test_image(rgba_image_path, mode='RGBA')
        result = convert_image_to_pdf(rgba_image_path, self.output_pdf)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_pdf))
        os.remove(rgba_image_path)

    def test_nonexistent_input(self):
        """Test handling of nonexistent input file"""
        result = convert_image_to_pdf('nonexistent.jpg', self.output_pdf)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.output_pdf))

    def test_folder_conversion(self):
        """Test combining multiple images from a folder"""
        # Create multiple test images
        image_names = ['test1.jpg', 'test2.png', 'test3.jpg']
        for name in image_names:
            path = os.path.join(self.test_dir, name)
            self.create_test_image(path)
            
        # Add a non-image file to test filtering
        with open(os.path.join(self.test_dir, 'not_an_image.txt'), 'w') as f:
            f.write('This is not an image')
            
        result = convert_images_from_folder(self.test_dir)
        self.assertTrue(result)
        
        # Find the generated PDF file
        pdf_files = [f for f in os.listdir(self.test_dir) if f.endswith('.pdf')]
        self.assertEqual(len(pdf_files), 1)
        
        # Verify filename format
        pdf_file = pdf_files[0]
        folder_name = os.path.basename(self.test_dir)
        self.assertTrue(re.match(f'combined_{folder_name}_\\d{{8}}_\\d{{6}}\\.pdf', pdf_file))
        
        # Verify file content
        pdf_path = os.path.join(self.test_dir, pdf_file)
        self.assertTrue(os.path.getsize(pdf_path) > 0)
        
        # Clean up additional test files
        for name in image_names:
            os.remove(os.path.join(self.test_dir, name))
        os.remove(os.path.join(self.test_dir, 'not_an_image.txt'))

    def test_empty_folder(self):
        """Test handling of folder with no valid images"""
        # Create a folder with no images
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir)
        
        result = convert_images_from_folder(empty_dir, self.output_pdf)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.output_pdf))
        
        os.rmdir(empty_dir)

if __name__ == '__main__':
    unittest.main()
