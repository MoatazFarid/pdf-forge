# Image to PDF Converter

A simple command-line tool to convert images to PDF format.

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python img_to_pdf.py path/to/image.jpg
```

Specify output file:
```bash
python img_to_pdf.py path/to/image.jpg -o output.pdf
```

## Supported Image Formats

The tool supports various image formats including:
- JPEG/JPG
- PNG
- BMP
- TIFF
- and more (any format supported by Pillow)
