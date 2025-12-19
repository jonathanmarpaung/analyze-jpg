# Bulk Image Downloader CLI

A lightweight Python command-line tool for batch downloading random images from [Lorem Picsum](https://picsum.photos). Designed for generating datasets for testing, compression analysis, or placeholder content.

## Features

* **Customizable Sample Size**: Define how many images to fetch.
* **Resolution Control**: Set specific dimensions (Square ).
* **Smart Caching**: Skips existing files by default to save bandwidth.
* **Force Mode**: Option to overwrite/regenerate existing samples.
* **Visual Feedback**: Real-time CLI progress bar.

## Prerequisites

Ensure you have Python 3.x installed.

```bash
pip install requests

```

## Usage

Basic usage with default settings (10 images, 1000x1000px, `./samples`):

```bash
python samples.py

```

### Command Line Arguments

| Flag | Long Flag | Description | Default |
| --- | --- | --- | --- |
| `-n` | `--number` | Number of images to download. | `10` |
| `-s` | `--size` | Image dimension in pixels (). | `1000` |
| `-o` | `--output` | Target directory for saved images. | `./samples` |
| `-f` | `--force` | Force overwrite existing files in the directory. | `False` |
| `-h` | `--help` | Show help message and exit. | - |

## Examples

**1. Download 50 images for a dataset:**

```bash
python samples.py -n 50 -o ./training_data

```

**2. Download low-resolution thumbnails (300x300):**

```bash
python samples.py -n 20 -s 300 -o ./thumbnails

```

**3. Regenerate/Overwrite existing dataset:**
If the images in the folder are corrupted or you need new random seeds:

```bash
python samples.py -n 10 -f

```

## Output Structure

The script generates files with sequential naming:

```text
./samples/
├── sample_1.jpg
├── sample_2.jpg
├── ...
└── sample_N.jpg

```