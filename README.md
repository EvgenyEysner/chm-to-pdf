# CHM to PDF Converter

A Python utility to convert CHM (Compiled HTML Help) files into PDF documents.

## Features

- Extracts content from CHM files using 7-Zip
- Preserves the original document structure based on the CHM table of contents
- Converts HTML pages to PDF format
- Merges all pages into a single PDF document

## Prerequisites

- Python 3.11+
- 7-Zip installed and available in the system PATH
- Required Python packages:
    - PyPDF2
    - beautifulsoup4
    - weasyprint

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/EvgenyEysner/chm-to-pdf.git
    cd chm-to-pdf
    ```
2. Install the required packages using [uv](https://github.com/astral-sh/uv):
    ```bash
    uv pip install PyPDF2 beautifulsoup4 weasyprint
    ```

## Usage

```bash
  python main.py input_file.chm output_file.pdf
```