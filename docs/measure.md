# Image Compression Analysis Tool

A robust Python utility designed for statistical analysis of JPEG compression algorithms. It automates the process of batch-processing images, normalizing their dimensions, and measuring file size variations across the full spectrum of JPEG quality settings (1-100).

## Features

* **Auto-Normalization**: Automatically resizes all input images to a standard dimension (default: ) to ensure valid statistical comparison.
* **Format Standardization**: Auto-converts various color modes (CMYK, RGBA, P) to RGB before processing.
* **Iterative Measurement**: Generates 100 data points per image (Quality 1 to 100).
* **Progress Tracking**: Real-time CLI visual feedback.
* **Data Export**: Outputs a structured CSV file ready for regression analysis or visualization.

## Requirements

* Python 3.8+
* Pillow (PIL Fork)

```bash
pip install Pillow

```

## Usage

Basic execution using default settings (looks for images in `./samples` starting with `sample_`):

```bash
python measure.py

```

### Command Line Arguments

| Flag | Long Flag | Description | Default |
| --- | --- | --- | --- |
| `-i` | `--input` | Directory containing source images. | `./samples` |
| `-p` | `--prefix` | Filename prefix filter to select specific files. | `sample_` |
| `-o` | `--output` | Directory to save the resulting CSV. | `./out` |
| `-c` | `--csv` | Filename of the output CSV. | `result.csv` |
| `-r` | `--resize` | **[Important]** Force resize images to  pixels. | `1000` |

## Examples

**1. Standard Analysis**
Process images in `./samples`, resize to 1000px, and save to `./out/result.csv`.

```bash
python measure.py

```

**2. High-Resolution Analysis**
Analyze images at 2048x2048 resolution.

```bash
python measure.py -r 2048

```

**3. Custom Directory & Prefix**
Analyze images in `./raw_data` that start with `img_`.

```bash
python measure.py -i ./raw_data -p img_ -o ./analysis

```

## Output Data Structure

The generated CSV file contains the following columns:

| Column | Description |
| --- | --- |
| `Image_Name` | The filename of the source image. |
| `Original_Format` | The original extension (e.g., .png, .jpg). |
| `Quality` | The JPEG quality setting used (1-100). |
| `Size_KB` | The resulting file size in Kilobytes. |
| `Dimensions` | The dimensions used for compression (e.g., 1000x1000). |

---

### Workflow Recommendation

1. **Generate Data**: Use `sample.py` to fetch raw images.
2. **Measure**: Run `measure.py` to normalize and measure compression curves.
3. **Analyze**: Import the resulting CSV into Python (Pandas), R, or Excel to perform Linear Regression or plot scatter graphs.