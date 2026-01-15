# 🎙️ Kaminski Whisper Desktop (Local AI Transcriber)

> **A simple, privacy-focused tool to transcribe sensitive meetings offline using your local GPU.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 The Context: Why I built this?
As a Senior Data Scientist and Policy Consultant working with international organizations and government bodies, I often deal with **sensitive recordings** that cannot be uploaded to cloud-based transcription services due to strict data sovereignty and privacy regulations.

I needed a tool that was:
1.  **Secure:** 100% Offline (Air-gapped ready).
2.  **Powerful:** Using state-of-the-art models (OpenAI Whisper Large-v3).
3.  **Simple:** A quick GUI drag-and-drop, no command line needed for daily use.

This project is a **byproduct of my daily workflow**. It's not complex enterprise software, but a practical utility to solve a real-world bottleneck for researchers, policymakers, and privacy-conscious professionals.

## ✨ Features
* **Zero Data Leaks:** Everything runs locally on your hardware.
* **Powered by `faster-whisper`:** Utilizing CTranslate2 for up to 4x speedup compared to original Whisper.
* **NVIDIA GPU Acceleration:** Optimized for CUDA (requires NVIDIA drivers).
* **Auto-Save:** Automatically saves your transcript to the disk to prevent data loss.

## ⚙️ System Requirements
Since this runs a Large Language Model locally, hardware matters:
* **GPU (Recommended):** NVIDIA RTX card with at least **4GB VRAM** (8GB+ recommended for `large-v3` model).
* **CPU (Fallback):** Possible, but transcription will be significantly slower.
* **RAM:** 16GB+ recommended.

## ⚙️ Prerequisites (Read This First)

This tool runs a powerful AI model locally on your computer. Unlike a simple `.exe` file, it requires a specific environment to function correctly.

Before proceeding, ensure you have:

1.  **NVIDIA GPU (Highly Recommended):**
    * To transcribe quickly, you need an NVIDIA card with CUDA support.
    * *Note: It can run on CPU, but it will be significantly slower.*
2.  **Python Installed:**
    * You must have **Python 3.10** or newer installed on your system.
    * [Download Python Here](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation).
3.  **Conda Manager (Preferred):**
    * We strongly recommend using **Miniconda** or **Anaconda** to create a clean isolated environment. This prevents conflicts with other software on your PC.

---

## 🛠️ Installation Guide

### Step 1: Set up the Environment (The "Conda" Way)
Open your terminal (Anaconda Prompt or PowerShell) and run the following commands one by one:

```bash
# 1. Create a specific environment for this tool (forces Python 3.10)
conda create -n whisper-desktop python=3.10

# 2. Activate the environment
conda activate whisper-desktop

# Install core libraries
pip install faster-whisper tk

# CRITICAL FOR WINDOWS USERS: Install NVIDIA drivers linkage
# This ensures the AI can "talk" to your graphics card.
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12

> **A simple, privacy-focused tool to transcribe sensitive meetings offline using your local GPU.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 The Context: Why I built this?
As a Senior Data Scientist and Policy Consultant working with international organizations (like OECD) and government bodies, I often deal with **sensitive recordings** that cannot be uploaded to cloud-based transcription services due to strict data sovereignty and privacy regulations.

I needed a tool that was:
1.  **Secure:** 100% Offline (Air-gapped ready).
2.  **Powerful:** Using state-of-the-art models (OpenAI Whisper Large-v3).
3.  **Simple:** A quick GUI drag-and-drop, no command line needed for daily use.

This project is a **byproduct of my daily workflow**. It's not complex enterprise software, but a practical utility to solve a real-world bottleneck for researchers, policymakers, and privacy-conscious professionals.

## ✨ Features
* **Zero Data Leaks:** Everything runs locally on your hardware.
* **Powered by `faster-whisper`:** Utilizing CTranslate2 for up to 4x speedup compared to original Whisper.
* **NVIDIA GPU Acceleration:** Optimized for CUDA (requires NVIDIA drivers).
* **Auto-Save:** Automatically saves your transcript to the disk to prevent data loss.

## ⚙️ System Requirements
Since this runs a Large Language Model locally, hardware matters:
* **GPU (Recommended):** NVIDIA RTX card with at least **4GB VRAM** (8GB+ recommended for `large-v3` model).
* **CPU (Fallback):** Possible, but transcription will be significantly slower.
* **RAM:** 16GB+ recommended.


## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/whisper-desktop.git](https://github.com/YOUR_USERNAME/whisper-desktop.git)
cd whisper-desktop

2. Create the Environment
We use environment.yml to ensure all system dependencies (like FFmpeg and Python 3.10) are installed correctly.

Bash

conda env create -f environment.yml
3. Activate the Environment
Bash

conda activate whisper-desktop
🚀 Usage
Once the environment is active, simply run the main script:

Bash

python main.py
Select Media: Click to choose your audio or video file (MP3, MP4, WAV, MKV, etc.).

Select Model:

small / medium: Faster, lower resource usage.

large-v3: State-of-the-art accuracy (requires more VRAM).

Start: The transcription will begin. The output .txt file is automatically saved to the project directory upon completion.

⚠️ Notes
First Run: The application will download the model weights automatically on the first usage. This may take a few minutes depending on your connection.

Hardware Fallback: If no GPU is detected, the application will default to CPU, which may be significantly slower.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
