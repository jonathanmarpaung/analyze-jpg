import argparse
import sys
from pathlib import Path
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser(description="Dataset Integrity & Consistency Checker")
    parser.add_argument('-i', '--input', type=str, default='./samples', help='Directory to check')
    parser.add_argument('-n', '--number', type=int, default=30, help='Expected total number of samples')
    parser.add_argument('-p', '--prefix', type=str, default='sample_', help='Filename prefix (default: sample_)')
    parser.add_argument('-e', '--extension', type=str, default='.jpg', help='Expected file extension (default: .jpg)')
    parser.add_argument('--no-integrity', action='store_true', help='Skip deep integrity check (opening files)')
    return parser.parse_args()

def get_file_index(filename: str, prefix: str) -> int:
    """Extracts integer index from filename (e.g., 'sample_15.jpg' -> 15)"""
    try:
        stem = Path(filename).stem # sample_15
        if stem.startswith(prefix):
            return int(stem.replace(prefix, ''))
    except ValueError:
        return -1
    return -1

def main():
    args = parse_args()
    input_dir = Path(args.input)

    if not input_dir.exists():
        print(f"Error: Directory '{input_dir}' not found.")
        sys.exit(1)

    print(f"Checking dataset in '{input_dir}'...")
    print(f"Expected range: 1 to {args.number} | Prefix: '{args.prefix}'")
    print("-" * 50)

    # 1. Scanning Files
    found_files = list(input_dir.glob(f"{args.prefix}*{args.extension}"))
    found_indices = set()
    corrupted_files = []

    print(f"Found {len(found_files)} files matching pattern.")

    # 2. Integrity & Indexing Loop
    for file_path in found_files:
        idx = get_file_index(file_path.name, args.prefix)
        
        if idx != -1:
            found_indices.add(idx)

        # Integrity Check (Try to open image)
        if not args.no_integrity:
            try:
                with Image.open(file_path) as img:
                    img.verify() # Fast check without decoding whole image
            except Exception as e:
                print(f"[CORRUPT] {file_path.name}: {e}")
                corrupted_files.append(file_path.name)

    # 3. Analyze Missing Sequence
    expected_indices = set(range(1, args.number + 1))
    missing_indices = sorted(list(expected_indices - found_indices))
    extra_indices = sorted(list(found_indices - expected_indices))

    print("-" * 50)
    print("REPORT:")
    
    # Report Missing
    if missing_indices:
        print(f"❌ MISSING IDs ({len(missing_indices)}): {missing_indices}")
    else:
        print("✅ No missing IDs in sequence.")

    # Report Corrupted
    if corrupted_files:
        print(f"❌ CORRUPTED FILES ({len(corrupted_files)}): {corrupted_files}")
        print("   (These files exist but cannot be processed)")
    elif not args.no_integrity:
        print("✅ All files passed integrity check.")

    # Report Extras
    if extra_indices:
        print(f"⚠️ EXTRA FILES (Outside range 1-{args.number}): {extra_indices}")

    # Final Verdict
    if not missing_indices and not corrupted_files:
        print("\nDataset STATUS: HEALTHY")
    else:
        print("\nDataset STATUS: INCOMPLETE / DAMAGED")

if __name__ == "__main__":
    main()