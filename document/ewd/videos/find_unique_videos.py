import os
import hashlib

def file_hash(path, chunk_size=8192):
    """Return SHA-256 hash of a file in streaming chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def find_unique_videos(directory):
    """
    Scans a directory for .mp4 video files, detects duplicates by content,
    and returns a list of unique videos using the first filename encountered.
    """
    seen_hashes = {}
    unique_files = []
    duplicates = []

    for filename in sorted(os.listdir(directory)):
        if not filename.lower().endswith(".mp4"):
            continue

        full_path = os.path.join(directory, filename)

        # Calculate file content hash
        fhash = file_hash(full_path)

        if fhash not in seen_hashes:
            seen_hashes[fhash] = filename
            unique_files.append(filename)
        else:
            duplicates.append((filename, seen_hashes[fhash]))

    return unique_files, duplicates


if __name__ == "__main__":
    directory = input("Enter directory path: ").strip()

    unique, dupes = find_unique_videos(directory)

    print("\n=== UNIQUE VIDEO FILES ===")
    for u in unique:
        print(u)

    print("\n=== DUPLICATES FOUND ===")
    for dup, original in dupes:
        print(f"{dup}  -->  duplicate of  {original}")

    print("\nDone.")
