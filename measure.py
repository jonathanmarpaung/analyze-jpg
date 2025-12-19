import argparse
import csv
import sys
from pathlib import Path
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser(description="JPEG Compression Analysis Tool with Auto-Normalization")
    parser.add_argument('-i', '--input', type=str, default='./samples', help='Input directory')
    parser.add_argument('-p', '--prefix', type=str, default='sample_', help='File prefix filter')
    parser.add_argument('-o', '--output', type=str, default='./out', help='Output directory')
    parser.add_argument('-c', '--csv', type=str, default='result.csv', help='Output CSV filename')
    parser.add_argument('-r', '--resize', type=int, default=1000, help='Force resize images to NxN (default: 1000)')
    return parser.parse_args()

def print_progress(current: int, total: int, length: int = 40):
    percent = current / total * 100
    filled = int(length * current // total)
    bar = '█' * filled + '-' * (length - filled)
    sys.stdout.write(f'\rProgress |{bar}| {percent:.1f}%')
    sys.stdout.flush()

def get_target_files(input_dir: Path, prefix: str) -> list[Path]:
    valid_exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    return sorted([
        f for f in input_dir.iterdir() 
        if f.is_file() and f.name.startswith(prefix) and f.suffix.lower() in valid_exts
    ])

def process_image_loop(img: Image.Image, name: str, original_fmt: str, writer, output_path: Path):
    """
    Handles the 1-100 quality loop for a single image object.
    """
    # Ensure RGB for JPEG compatibility
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    dim_str = f"{width}x{height}"

    for q in range(1, 101):
        temp_filename = f"temp_{name}_{q}.jpg"
        temp_path = output_path / temp_filename
        
        # Compress
        img.save(temp_path, "JPEG", quality=q)
        
        # Measure
        size_kb = temp_path.stat().st_size / 1024
        
        # Write Record: Name, Format, Quality, Size, Dimensions
        writer.writerow([name, original_fmt, q, round(size_kb, 2), dim_str])
        
        # Cleanup
        temp_path.unlink()

def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    csv_file = output_path / args.csv

    if not input_path.exists():
        print(f"Error: Input directory '{input_path}' not found.")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)
    
    files = get_target_files(input_path, args.prefix)
    if not files:
        print(f"No files matching '{args.prefix}*' found in {input_path}")
        sys.exit(1)

    print(f"Target: {len(files)} images | Resize: {args.resize}x{args.resize} | Output: {csv_file}")

    total_ops = len(files) # We track progress per image to avoid spamming the console
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image_Name', 'Original_Format', 'Quality', 'Size_KB', 'Dimensions'])

        for i, file_path in enumerate(files, 1):
            try:
                with Image.open(file_path) as img:
                    # Automation: Force Resize
                    if args.resize:
                        img = img.resize((args.resize, args.resize), Image.Resampling.LANCZOS)
                    
                    # Run the compression loop
                    process_image_loop(img, file_path.name, file_path.suffix, writer, output_path)
                    
                print_progress(i, total_ops)

            except Exception as e:
                print(f"\n[Error] Failed processing {file_path.name}: {e}")

    print("\n\nAnalysis completed successfully.")

if __name__ == "__main__":
    main()