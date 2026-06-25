# 🚦Traffic Density Detection System

This project implements a real-time traffic density detection system using TensorFlow Lite and OpenCV. It detects vehicles from webcam or video input, estimates traffic density based on detected vehicles, and displays the results in real time.

The lightweight TensorFlow Lite model makes the application suitable for deployment on edge devices where computational resources are limited.

## Features

* 🚗 Real-time vehicle detection
* 📹 Video processing using OpenCV
* 🤖 TensorFlow Lite inference
* 📊 Traffic density estimation
* ⚡ Lightweight and suitable for edge devices

## Technologies Used

* Python
* TensorFlow Lite
* OpenCV
* NumPy

## Project Structure

```text
src/
models/
sample_images/
sample_videos/
outputs/
README.md
requirements.txt
```

## Installation

```bash
git clone https://github.com/Rajary293/Traffic-Density-Detection-System.git

cd Traffic-Density-Detection-System

pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python src/main.py
```

## Results

The system detects vehicles from video frames and estimates traffic density in real time.



## Future Improvements

* Vehicle tracking (SORT/DeepSORT)
* Lane detection
* Traffic congestion prediction
* Web dashboard using Streamlit
* Support for multiple camera feeds

## Author

**Raj Aryan SIngh**
