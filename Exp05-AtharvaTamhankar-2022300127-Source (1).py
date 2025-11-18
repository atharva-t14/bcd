# Atharva Tamhankar - 2022300127

import hashlib
import os
BLOCK_SIZE = 65536
def generate_hashes(file_path):
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()
    sha512_hash = hashlib.sha512()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(BLOCK_SIZE):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
                sha512_hash.update(chunk)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    return {
        'MD5': md5_hash.hexdigest(),
        'SHA-1': sha1_hash.hexdigest(),
        'SHA-256': sha256_hash.hexdigest(),
        'SHA-512': sha512_hash.hexdigest(),
    }
def create_hash_report(file_path, hashes):
    report_filename = r"C:\Users\tanis\Downloads\hash_report.txt"
    with open(report_filename, 'w') as f:
        f.write(f"Hash Report for file: {os.path.basename(file_path)}\n")
        f.write("=" * 50 + "\n")
        for algorithm, hash_value in hashes.items():
            f.write(f"{algorithm:<10}: {hash_value}\n")
    print(f"Successfully created hash report: {report_filename}")

def create_checksum_file(file_path, hash_algorithm='sha256'):
    checksum_filename = f"{file_path}.{hash_algorithm}"
    hasher = hashlib.new(hash_algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(BLOCK_SIZE):
                hasher.update(chunk)
    except FileNotFoundError:
        print(f"Error: Could not create checksum. File not found at {file_path}")
        return
    file_hash = hasher.hexdigest()
    filename = os.path.basename(file_path)
    with open(checksum_filename, 'w') as f:
        f.write(f"{file_hash}  {filename}")
    print(f"Successfully created checksum file: {checksum_filename}")
def verify_checksum(checksum_file_path):
    try:
        with open(checksum_file_path, 'r') as f:
            line = f.readline()
            stored_hash, original_filename = line.strip().split("  ", 1)
    except FileNotFoundError:
        print(f"Error: Checksum file not found at {checksum_file_path}")
        return
    except ValueError:
        print(f"Error: Checksum file '{checksum_file_path}' has incorrect format.")
        return
    hash_algorithm = checksum_file_path.split('.')[-1]
    hasher = hashlib.new(hash_algorithm)
    try:
        with open(original_filename, 'rb') as f:
            while chunk := f.read(BLOCK_SIZE):
                hasher.update(chunk)
        current_hash = hasher.hexdigest()
    except FileNotFoundError:
        print(f"Error: Original file '{original_filename}' not found for verification.")
        return
    print(f"Stored Hash  : {stored_hash}")
    print(f"Computed Hash: {current_hash}")
    if stored_hash == current_hash:
        print("Verification Result: Checksum OK (Authentic) ✅\n")
    else:
        print("Verification Result: Checksum FAILED (Tampered) ❌\n")

if __name__ == "__main__":
    input_file = r"C:\Users\tanis\Downloads\example.txt"
    with open(input_file, 'w') as f:
        f.write("The 2019 Cricket World Cup final at Lord's between England and New Zealand stands as a monumental event, not just in sports history.\n")
        f.write("The match concluded in a heart-stopping tie, with both teams scoring exactly 241 runs in their allotted 50 overs.\n")
        f.write("A tie in a high-stakes final is a statistically rare occurrence, setting the stage for an even more improbable conclusion.\n")
        f.write("The first tie-breaker was a 'Super Over,' a single-over eliminator where each team faces six balls to score as many runs as possible.\n")
        f.write("In a stunning display of symmetry, the Super Over also ended in a tie, with both England and New Zealand scoring 15 runs each.\n")
        f.write("The odds of a tie followed by a second tie in the eliminator are astronomically low, creating a scenario that the rulebook had barely anticipated.\n")
        f.write("\n") 
        f.write("With the scores level twice, the winner was decided by a controversial and now-defunct tie-breaker: the boundary countback rule.\n")
        f.write("The team that had scored more boundaries (fours and sixes) throughout their main 50-over innings and the Super Over would be declared the winner.\n")
        f.write("England had scored a total of 26 boundaries, while New Zealand had managed only 17.\n")
        f.write("Consequently, England was crowned the World Champion for the first time.\n")
        f.write("This method of victory was purely a product of a secondary statistical metric, one that had no direct bearing on the primary objective of scoring runs.\n")
        f.write("The decision sparked widespread debate about the fairness of a rule that felt arbitrary in such a critical moment\n")
        f.write("\n") 
        f.write("This match serves as a perfect text for integrity checks.\n")
        f.write("A single altered digit—changing the boundary count from 26 to 25, or the final score from 241 to 240—would fundamentally change the narrative and the outcome.\n")
        f.write("The integrity of these numbers is paramount.\n")
        f.write("The aftermath saw the International Cricket Council (ICC) scrap the boundary count rule for future tournaments.\n")
        f.write("This ensures that the primary skill of scoring runs, rather than a secondary statistic, determines the champion.\n")
        f.write("The 2019 final remains a testament to the razor-thin margins in elite sport and a powerful example of how data, rules.\n")

    print(f"--- Step 1: Generating Hashes for '{input_file}' ---")
    all_hashes = generate_hashes(input_file)
    if all_hashes:
        create_hash_report(input_file, all_hashes)
    print("-" * 50)
    print(f"\n--- Step 2: Creating Checksum File ---")
    checksum_algo = 'sha256'
    checksum_file = f"{input_file}.{checksum_algo}"
    create_checksum_file(input_file, checksum_algo)
    print("-" * 50)
    print(f"\n--- Step 3: Verification (Before Tampering) ---")
    verify_checksum(checksum_file)
    print("-" * 50)
    print(f"\n--- Step 4: Tampering Test ---")
    print(f"Modifying '{input_file}' by adding a new line...")
    with open(input_file, 'a') as f:
        f.write("\nThis line was added to tamper with the file.")
    print("File has been tampered with.")
    print("\n--- Re-running Verification (After Tampering) ---")
    verify_checksum(checksum_file)
    print("-" * 50)
