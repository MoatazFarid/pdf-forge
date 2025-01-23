import unittest
import os
import tempfile
from PIL import Image
from img_to_pdf import convert_image_to_pdf

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
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)
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
        default_output = os.path.splitext(self.test_image_path)[0] + '.pdf'
        self.assertTrue(result)
        self.assertTrue(os.path.exists(default_output))
        os.remove(default_output)  # Clean up

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

if __name__ == '__main__':
    unittest.main()
