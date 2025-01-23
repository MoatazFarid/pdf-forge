# PDFForge

[![Python Tests](https://github.com/MoatazFarid/pdf-forge/actions/workflows/python-tests.yml/badge.svg)](https://github.com/MoatazFarid/pdf-forge/actions/workflows/python-tests.yml)

A powerful command-line tool for converting images to PDF format with advanced features.

## Features

- Convert single images to PDF
- Combine multiple images from a folder into a single PDF
- Automatic timestamp in output filenames for unique identification
- Support for various image formats (JPEG, PNG, BMP, TIFF, GIF)
- Automatic RGB color space conversion
- Smart file ordering when combining multiple images

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/PDFForge.git
cd PDFForge
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Convert a Single Image

Basic usage:
```bash
python img_to_pdf.py -i path/to/image.jpg
```

This will create a PDF with a timestamp in the name (e.g., `image_20250123_152351.pdf`)

Specify output file:
```bash
python img_to_pdf.py -i path/to/image.jpg -o output.pdf
```

### Combine Multiple Images

Convert all images in a folder:
```bash
python img_to_pdf.py -f path/to/folder
```

This will create a combined PDF with a timestamp (e.g., `combined_foldername_20250123_152351.pdf`)

Specify output for combined PDF:
```bash
python img_to_pdf.py -f path/to/folder -o combined_output.pdf
```

## Supported Image Formats

- JPEG/JPG
- PNG
- BMP
- TIFF
- GIF

## Development

### Running Tests

```bash
python -m unittest test_img_to_pdf.py -v
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
