# Mass Scanner

A Python application for batch scanning documents using TWAIN interface. Designed to work with EPSON ES-865 and other TWAIN-compatible scanners.

## Features

- Automatic document scanning from ADF (Automatic Document Feeder)
- Support for duplex scanning
- Configurable DPI and color mode settings
- Automatic file naming with timestamps
- No UI interaction required - fully automated scanning

## Requirements

- Python 3.x
- TWAIN-compatible scanner
- Windows OS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ZacharyLeahan/scanner.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to start scanning:
```bash
python main.py
```

The script will:
1. Detect available TWAIN scanners
2. Configure scanner settings (300 DPI, color mode)
3. Start scanning all pages in the ADF
4. Save scanned images to the `scanned_documents` directory
