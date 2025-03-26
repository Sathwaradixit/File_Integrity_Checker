## Overview

**File Integrity Checker and Monitor** is a Python application that allows users to verify the integrity of files by calculating and comparing their hashes. The program also monitors the file for any changes in real-time, alerting the user when modifications are detected. This application uses various hashing algorithms (e.g., `sha256`, `md5`, `sha1`, `sha512`) and leverages the `watchdog` library to monitor file changes.

## Features

- **File Integrity Check**: Compare a file's hash against a known hash to ensure it hasn't been tampered with.
- **File Monitoring**: Automatically monitor the selected file for any modifications, and alert the user if the file is changed.
- **GUI Interface**: Easy-to-use graphical interface using `tkinter` that allows users to:
  - Select a file to check.
  - Input a known hash for comparison.
  - Choose the hashing algorithm.
  - Start integrity check and monitoring.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Sathwaradixit/File_Integrity_Checker.git
   cd file-integrity-checker
