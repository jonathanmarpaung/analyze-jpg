import argparse
import sys
import time
from pathlib import Path
import requests

def parse_arguments():
    parser = argparse.ArgumentParser(description="Bulk Image Downloader CLI")
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of samples (default: 10)')
    parser.add_argument('-s', '--size', type=int, default=1000, help='Image dimension SxS (default: 1000)')
    parser.add_argument('-o', '--output', type=str, default='./samples', help='Output directory (default: ./samples)')
    parser.add_argument('-f', '--force', action='store_true', help='Force regenerate/overwrite existing files')
    return parser.parse_args()

def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

def download_file(url: str, dest: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception:
        return False

def main():
    args = parse_arguments()
    output_dir = Path(args.output)
    
    # Ensure directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Target: {args.number} images | Size: {args.size}x{args.size} | Dir: {output_dir}")
    
    print_progress(0, args.number, prefix='Progress:', suffix='Starting...', length=40)

    for i in range(1, args.number + 1):
        filename = f"sample_{i}.jpg"
        file_path = output_dir / filename
        url = f"https://picsum.photos/{args.size}/{args.size}"

        # Skip logic
        if file_path.exists() and not args.force:
            print_progress(i, args.number, prefix='Progress:', suffix=f'Skipped {filename}    ', length=40)
            continue

        # Download logic
        success = download_file(url, file_path)
        status_msg = f"Done {filename}" if success else f"Error {filename}"
        
        print_progress(i, args.number, prefix='Progress:', suffix=f'{status_msg:<20}', length=40)
        
        # Simple rate limiting
        time.sleep(0.1)

    print(f"\nBatch operation completed.")

if __name__ == "__main__":
    main()