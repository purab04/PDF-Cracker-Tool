# pdf_cracker_tool.py

import pikepdf
from pikepdf import PasswordError
from tqdm import tqdm
import itertools
import string
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_passwords(chars, min_length=1, max_length=4):
    """
    Generate all possible passwords with given characters and length range.
    """
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(chars, repeat=length):
            yield ''.join(combo)

def load_passwords(wordlist_file):
    """
    Load passwords line-by-line from a wordlist file.
    """
    try:
        with open(wordlist_file, 'r') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_file}' not found.")
        return

def try_password(pdf_file, password):
    """
    Attempt to open the PDF with the given password.
    Return the password if successful, else None.
    """
    try:
        with pikepdf.open(pdf_file, password=password):
            return password
    except PasswordError:
        return None
    except Exception as e:
        print(f"Unexpected error with password '{password}': {e}")
        return None

def decrypt_pdf(pdf_file, passwords, max_workers=10):
    """
    Try passwords in parallel using threads, return the correct password if found.
    """
    found_password = None
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(try_password, pdf_file, pw): pw for pw in passwords}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Cracking PDF"):
            result = future.result()
            if result:
                found_password = result
                # Cancel all remaining tasks once password is found
                for fut in futures:
                    fut.cancel()
                break
    return found_password

def main():
    parser = argparse.ArgumentParser(description="PDF Cracker Tool")
    parser.add_argument("pdf_file", help="Path to the password-protected PDF file")
    parser.add_argument("--wordlist", help="Path to password wordlist file")
    parser.add_argument("--generate", action="store_true", help="Generate passwords (brute force)")
    parser.add_argument("--chars", default=string.ascii_lowercase + string.digits,
                        help="Characters to use for password generation (default: lowercase letters + digits)")
    parser.add_argument("--min_length", type=int, default=1, help="Minimum password length (default: 1)")
    parser.add_argument("--max_length", type=int, default=4, help="Maximum password length (default: 4)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for cracking (default: 10)")
    args = parser.parse_args()

    if args.wordlist:
        passwords = list(load_passwords(args.wordlist))
        if not passwords:
            print("No passwords loaded from wordlist. Exiting.")
            return
    elif args.generate:
        passwords = list(generate_passwords(args.chars, args.min_length, args.max_length))
        if not passwords:
            print("No passwords generated. Check parameters. Exiting.")
            return
    else:
        print("Error: You must specify either --wordlist or --generate.")
        parser.print_help()
        return

    print(f"Starting PDF cracking on '{args.pdf_file}' using {len(passwords)} passwords...")
    found = decrypt_pdf(args.pdf_file, passwords, max_workers=args.threads)

    if found:
        print(f"\nSuccess! Password found: {found}")
    else:
        print("\nFailed to find the password.")

if __name__ == "__main__":
    main()
