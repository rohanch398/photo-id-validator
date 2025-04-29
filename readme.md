# Photo ID Validator

## Overview

This project provides a **Photo ID Validator** built using **Streamlit** and **Docker**. It validates whether a user-uploaded photo complies with common official ID photo requirements, such as correct dimensions, white background, visible face, neutral expression, and no accessories.

The application uses **MediaPipe** for face detection, **FER** for emotion recognition, and **OpenCV** for image processing.

## Setup Instructions

### Prerequisites

To run this project locally, you need:

  * **Docker**: [Install Docker](https://www.docker.com/get-started)
  * **Git**: [Install Git](https://git-scm.com/)
  * **Streamlit**: Streamlit will be installed automatically inside the Docker container.

### Steps to Run Locally with Docker

1.  **Clone the Repository**

    Open your terminal and run the following command to clone the repository:

    ```bash
    git clone [https://github.com/rohanch398/photo-id-validator.git](https://github.com/rohanch398/photo-id-validator.git)
    cd photo-id-validator
    ```

2.  **Build the Docker Image**

    In your terminal, run the following command to build the Docker image:

    ```bash
    docker build -t photo-id-validator .
    ```

3.  **Run the Docker Container**

    Start the container by running:

    ```bash
    docker run -p 8501:8501 photo-id-validator
    ```

    This will start a local instance of Streamlit on port 8501.

    **Access the Application**

    Open your browser and visit:
    [http://localhost:8501](http://localhost:8501)
    You can now upload photos and check if they meet the required criteria for an official photo ID.

## Approach

The Photo ID Validator works by running several checks on the uploaded image. The image is analyzed for:

  * **Dimensions**: The image must be 413x531 pixels (standard ID photo size).
  * **Background**: The background must be white with at least 30% white pixels.
  * **Face Positioning**: The person must be looking directly at the camera, with no obstructions.
  * **Shoulders Visible**: The person's shoulders should be visible in the image (i.e., the face should not occupy the entire image).
  * **Ears Unobstructed**: The person’s ears should not be covered by accessories (like glasses or hats).
  * **Expression**: The expression must be neutral (no smiles, frowns, or other facial expressions).
  * **Accessories**: The photo should not contain accessories like glasses or head coverings.

**These checks are done using various Python libraries:**

  * MediaPipe for face detection
  * FER for emotion recognition
  * OpenCV for image manipulation and processing

## Time Expectation

  * **Initial Setup**: \~5 minutes to clone the repo, build the Docker image, and run the container.
  * **Photo Validation**: \~2-3 seconds per uploaded image, depending on the size of the photo.

## Description of Components

1.  **IPP.py**

    This is the main Python script where the logic resides. It includes:

      * Image upload functionality using Streamlit
      * Validation functions like checking dimensions, background color, facial expression, and more.
      * Integration with MediaPipe and FER for image and emotion detection.
      * Results displayed in a clean, user-friendly interface via Streamlit.

2.  **requirements.txt**

    This file lists the Python dependencies required to run the project:

      * streamlit
      * opencv-python
      * mediapipe
      * fer
      * numpy
      * Pillow (for image handling)

    These dependencies are installed automatically when the Docker container is built.

3.  **Dockerfile**

    The Dockerfile defines how the application is containerized. It:

      * Uses the official Python 3.9 slim image as the base
      * Installs required system dependencies like libgl1-mesa-glx and libglib2.0-0 for MediaPipe
      * Copies the project files and installs Python dependencies from requirements.txt
      * Exposes port 8501 for Streamlit

4.  **images/ Folder**

    This folder contains example images that you can use to test the Photo ID Validator. These sample photos include a mix of valid and invalid ID photos to help you evaluate how well the application performs its validation checks.

5.  **README.md**

    This file — explaining how to set up and run the application.

## Known Limitations

  * **Expression Recognition**: The FER library used for emotion detection may not always accurately identify the exact expression, especially for subtle ones.
  * **Background Detection**: The current algorithm checks for white pixels but could miss slight shades of white (e.g., off-white or slightly colored backgrounds).
  * **Accessories Detection**: The current accessory detection is based on the presence of glasses and does not cover other potential accessories like hats or scarves.

## Future Improvements

  * **Enhanced Background Detection**: Improve detection of backgrounds that are close to white but not exactly 255,255,255.
  * **Multiple Face Detection**: Currently, the app only works for images with a single face. A future improvement could be to handle multiple faces in the frame.
  * **Head Covering Detection**: Integrating a better model for detecting head coverings, such as hats or scarves, to improve validation accuracy.
  * **Facial Expression Variability**: Enhance emotion recognition to handle a broader range of facial expressions beyond just "neutral" or "smiling."

## References

  * [https://www.youtube.com/watch?v=kSqxn6zGE0c](https://www.youtube.com/watch?v=kSqxn6zGE0c)
  * [https://www.youtube.com/watch?v=mPCZLOVTEc4](https://www.youtube.com/watch?v=mPCZLOVTEc4)
  * [Face Detection Using Cascade Classifier using OpenCV Python](https://www.geeksforgeeks.org/face-detection-using-cascade-classifier-using-opencv-python/)
  * [Efficient way to detect white background in image](https://stackoverflow.com/questions/64304446/efficient-way-to-detect-white-background-in-image)

## License
This project is licensed under the MIT License - see the LICENSE file for details.