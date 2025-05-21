# PDF Cracker Tool

A Python script to decrypt password-protected PDFs by trying passwords from a wordlist or by brute-force generation, using multithreading for faster cracking.

---

## Overview

The PDF Cracker Tool allows you to attempt to decrypt a password-protected PDF by testing passwords either from a provided wordlist or by generating possible passwords on the fly. It uses multithreading for efficiency, the `pikepdf` library for PDF handling, `tqdm` for progress display, and `argparse` for command-line arguments.

This tool simulates brute-force attacks on weak PDF encryption for educational and security testing purposes only. Always ensure you have permission to test the PDFs you work on.

---

## Prerequisites

You should be familiar with the following Python concepts to understand and extend this tool:

1. **File Input/Output (I/O)**  
   Reading and writing text files safely with context managers (`with open()`).

2. **Functions, Generators, and itertools**  
   Creating efficient generators for lazy password production using `yield` and `itertools.product`.

3. **Exception Handling**  
   Handling specific exceptions like `pikepdf._core.PasswordError` to catch wrong passwords without crashing.

4. **Command-Line Arguments (argparse)**  
   Parsing input arguments for file paths and options.

5. **Working with pikepdf**  
   Opening and attempting to decrypt PDFs with password support.

6. **Multithreading (concurrent.futures.ThreadPoolExecutor)**  
   Running password attempts in parallel to speed up cracking.

7. **Progress Tracking (tqdm)**  
   Displaying a progress bar during the cracking process.

---

## Installation

Install required packages with:

```bash
pip install pikepdf tqdm
