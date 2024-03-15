# AutoMind-Glide

This Python script implements a self-driving car system using computer vision techniques and IoT capabilities. It captures real-time images from a Raspberry Pi camera module, processes them to detect lane markings, objects, and traffic signs, and makes driving decisions accordingly. The system utilizes OpenCV for image processing and RPi.GPIO for controlling GPIO pins for external devices.

## Features

- Real-time image processing
- Lane detection and tracking
- Object detection
- Traffic sign detection
- Automatic driving decisions based on detected objects and lane markings
- IoT integration for controlling external devices (e.g., motors, lights)

## Prerequisites

- Python 3.x
- OpenCV
- picamera library
- RPi.GPIO library

## Installation

1. Clone this repository:

```bash
git clone https://github.com/username/repo.git
```
2. The script will start capturing and processing images in real-time.

3. Detected objects, lane markings, and driving decisions will be displayed on the screen.

## Code Structure

- `self_driving_car.py`: Main Python script containing the self-driving car logic.
- `README.md`: This file providing information about the project.
- `cascade_files/`: Directory containing XML files for object detection using Haar cascades.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the OpenCV and Raspberry Pi communities for their contributions.
- Inspired by advancements in autonomous driving technology.
```

