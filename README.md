# AI Virtual Painter

AI Virtual Painter is an interactive application that allows users to draw on their screen using hand gestures captured by their webcam. This project utilizes computer vision techniques to track hand movements and convert them into digital drawings in real-time.

## Features

- Real-time hand tracking using webcam
- Multiple color options for drawing
- Eraser functionality
- Intuitive gesture-based controls
- Live preview of drawings overlaid on webcam feed

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-painter.git
   cd ai-virtual-painter
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install opencv-python mediapipe numpy
   ```

## Usage

1. Run the Virtual Painter:
   ```bash
   python VirtualPainter.py
   ```

2. Use your hand to control the painter:
   - Raise your index finger to draw
   - Raise both index and middle fingers to select colors or the eraser
   - Move your hand to draw on the screen

3. Press 'q' to quit the application

## Project Structure

- `VirtualPainter.py`: Main script to run the AI Virtual Painter
- `HandTrackingModule.py`: Module containing the hand tracking functionality
- `Header/`: Folder containing images for the color selection header

## How it Works

1. The application uses your webcam to capture video input.
2. MediaPipe is used to detect and track hand landmarks in each frame.
3. Based on the positions of your fingers, the program determines whether you're in drawing mode or selection mode.
4. In drawing mode, the movement of your index finger tip is tracked to create lines on the canvas.
5. In selection mode, you can choose different colors or the eraser by moving your hand to different sections of the header.
6. The drawing is overlaid on the webcam feed in real-time, providing immediate visual feedback.

## Customization

You can customize various aspects of the painter:
- Adjust `brushThickness` and `eraserThickness` in `VirtualPainter.py` to change the size of the drawing tools.
- Modify the color options by changing the color values in the color selection logic.
- Add new functionalities by implementing new gestures and corresponding actions.

## Troubleshooting

- Ensure your webcam is properly connected and functioning.
- Make sure you have a well-lit environment for better hand detection.
- If you encounter performance issues, try lowering the resolution of the webcam capture.

## Contributing

Contributions to improve AI Virtual Painter are welcome. Please feel free to submit a Pull Request.
