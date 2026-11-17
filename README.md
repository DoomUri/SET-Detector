# SET-Detector

A card recognition and SET-solving application developed using **C++ and Python**.

## Overview

SET-Detector is a project designed to automatically recognize cards from the board game [SET](https://en.wikipedia.org/wiki/Set_(card_game)) and identify valid combinations.

The application uses computer vision techniques to detect and classify cards from an image, then processes their attributes to find all valid SET combinations.

## How It Works

The application is divided into two main components:

- **Card Recognition (Python):** Uses OpenCV to process images, detect individual cards and identify their attributes.
- **SET Solver (C++):** Receives the recognized cards and finds all valid SET combinations.

The detected cards are represented using four attributes: shape, color, texture and number. A valid SET consists of three cards where, for each attribute, 
the values are either all identical or all different.

## Technologies

- **C++** – SET detection algorithm and combination processing.
- **Python** – Image processing and card recognition.
- **OpenCV** – Computer vision and image analysis.

## Features

- Automatic card detection from images.
- Recognition of the four card attributes.
- Efficient identification of valid SET combinations.
- Integration of computer vision and algorithmic problem solving.

## Execution

Make sure **Python** is installed on your system before running the application.

1. Open `test.py` and specify the path to the image you want to process.
2. Run the following command from the project directory:

   ```bash
   python test.py
   ```

3. The detected SET combinations and processing results will be saved in the `Sets/` directory.

## Future Improvements

One of the main goals for future development is to create a dedicated application with a user-friendly interface, allowing users to take or upload a picture of a SET board and automatically detect all valid combinations without having to run the Python script manually.

The aim is to make the project more accessible and provide a complete, interactive experience.
