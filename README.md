# SET-Detector

A card recognition and SET-solving application developed using **C++ and Python**.

## Overview

SET-Detector is a project designed to automatically recognize cards from the board game [SET](https://en.wikipedia.org/wiki/Set_(card_game)) and identify valid combinations.

The application uses computer vision techniques to detect and classify cards from an image, then processes their attributes to find all valid SET combinations.

## How It Works

The application is divided into two main components:

- **Card Recognition (Python):** Uses OpenCV to process images, detect individual cards and identify their attributes.
- **SET Solver (C++):** Receives the recognized cards and finds all valid SET combinations.

The detected cards are represented using four attributes:

| Attribute | Possible values |
|---|---|
| Color | Red, Green, Purple |
| Shape | Diamond, Squiggle, Oval |
| Shading | Solid, Striped, Empty |
| Number | 1, 2, 3 |

A valid SET consists of three cards where, for each attribute, the values are either all identical or all different.

## Technologies

- **C++** – SET detection algorithm and combination processing.
- **Python** – Image processing and card recognition.
- **OpenCV** – Computer vision and image analysis.

## Project Structure

```text
SET-Detector/
├── C++/
│   └── ...
├── Python/
│   └── ...
└── README.md
```

## Features

- Automatic card detection from images.
- Recognition of the four card attributes.
- Efficient identification of valid SET combinations.
- Integration of computer vision and algorithmic problem solving.

## Purpose

This project combines computer vision and algorithm design to solve a real-world problem through image processing and efficient computation.
