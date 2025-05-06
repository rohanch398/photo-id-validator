## Photo ID Validator

### Overview

This project provides a **Photo ID Validator** built using **Streamlit** and **Docker**. It validates whether a user-uploaded photo complies with common official ID photo requirements, such as correct dimensions, white background, visible face, neutral expression, and no accessories.

The application leverages a combination of powerful libraries for robust analysis: **MediaPipe** for efficient face detection, **Dlib** for precise facial landmarking enabling advanced accessory detection, **FER** for emotion recognition to ensure a neutral expression, and **OpenCV** for fundamental image processing tasks. Containerization with **Docker** ensures consistent and straightforward deployment across different environments.

### Setup Instructions

#### Prerequisites

To run this project locally, you need:

  * **Docker**: [Install Docker](https://www.docker.com/get-started)
  * **Git**: [Install Git](https://git-scm.com/)
  * **Streamlit**: Streamlit will be installed automatically inside the Docker container.

#### Steps to Run Locally with Docker

1.  **Clone the Repository**

    Open your terminal and run the following command to clone the repository:

    ```bash
    git clone [https://github.com/rohanch398/photo-id-validator.git](https://github.com/rohanch398/photo-id-validator.git)
    cd photo-id-validator
    ```

2.  **Build the Docker Image**

    In your terminal, run the following command to build the Docker image. Can take upto 10-15 minutes:

    ```bash
    docker build -t photo-id-validator .
    ```

3.  **Run the Docker Container**

    Start the container by running:

    ```bash
    docker run -p 8501:8501 photo-id-validator
    ```

    This will start a local instance of Streamlit, accessible on port 8501.

    **Access the Application**

    Open your web browser and navigate to:
    [http://localhost:8501](http://localhost:8501)
    You can now upload your photo and receive instant feedback on its suitability for an official ID.

### Approach

The Photo ID Validator employs a multi-faceted approach to assess the uploaded image against standard ID photo criteria:

  * **Dimensions Check**: Verifies if the image resolution matches the required 413x531 pixels.
  * **Background Analysis**: Determines if the background is predominantly white (at least 30% white pixels with a defined tolerance).
  * **Face Detection and Positioning**: Utilizes MediaPipe for initial face detection, ensuring a face is present and oriented towards the camera.
  * **Shoulder Visibility**: Estimates if the shoulders are visible by analyzing the relative size of the detected face within the image.
  * **Ear Obstruction Assessment**: Checks if the ears are likely unobstructed based on the width of the detected face.
  * **Expression Recognition**: Employs the FER library to analyze facial expressions and confirm a neutral demeanor.
  * **Accessory Detection**: Implements an advanced method using **Dlib** for precise facial landmark detection. By analyzing the nasal bridge area, the application can effectively identify the presence of glasses.

**Key Libraries Used:**

  * **Streamlit**: For creating an interactive and user-friendly web application.
  * **OpenCV (cv2)**: For fundamental image manipulation, such as color space conversions and Gaussian blurring.
  * **MediaPipe**: For fast and efficient face detection.
  * **Dlib**: For high-accuracy facial landmark detection, crucial for refined accessory (glasses) detection.
  * **FER (Facial Expression Recognition)**: For analyzing facial expressions.
  * **NumPy**: For efficient numerical operations on image data.
  * **Pillow (PIL)**: For handling image loading and manipulation.

### Time Expectation

  * **Initial Setup**: Approximately 20 minutes to clone the repository, build the Docker image, and run the container.
  * **Photo Validation**: Around 2-3 seconds per uploaded image, depending on the image size and processing complexity.

### Description of Components

1.  **IPP.py**: The core Python script containing the entire application logic:
    * Image uploading via Streamlit's file uploader.
    * Implementation of all validation functions (dimensions, background, face positioning, etc.).
    * Integration of MediaPipe for face detection.
    * Utilization of Dlib for detailed facial landmark analysis and improved glasses detection.
    * Application of the FER library for emotion analysis.
    * Clear display of validation results and feedback using Streamlit's markdown and status elements.

2.  **requirements.txt**: Lists all the necessary Python packages and their versions required to run the application. Docker uses this file to install dependencies within the container:
    * streamlit
    * opencv-python
    * mediapipe
    * fer
    * numpy
    * Pillow
    * dlib

3.  **Dockerfile**: Defines the steps to create a Docker image for the application. It sets up the environment, installs dependencies, and specifies how to run the Streamlit application:
    * Uses a lightweight Python 3.9 base image.
    * Installs system-level dependencies required by MediaPipe and Dlib.
    * Copies project files into the container.
    * Installs Python dependencies from `requirements.txt`.
    * Exposes port 8501 for accessing the Streamlit application.
    * Sets the entry point to run the Streamlit app.

4.  **images/ Folder**: Contains example images (both valid and invalid ID photos) that users can use to test the functionality of the Photo ID Validator.

5.  **README.md**: This file, providing comprehensive information about the project, setup instructions, approach, and other relevant details.

### Known Limitations

  * **Subtle Expression Recognition**: The FER library's accuracy might be limited for very subtle facial expressions.
  * **Near-White Backgrounds**: The background detection relies on a white pixel threshold and might not perfectly identify backgrounds that are very close to white but not exact.
  * **Comprehensive Accessory Detection**: While glasses detection is enhanced using Dlib, the application does not currently have robust detection for other accessories like hats, scarves, or jewelry.

### Future Improvements

  * **Refined Background Analysis**: Implement more sophisticated background detection techniques to handle variations of white and potentially identify colored backgrounds more accurately.
  * **Multi-Face Support**: Extend the application to handle images containing multiple faces.
  * **Expanded Accessory Detection**: Integrate more advanced models or techniques to detect a wider range of accessories, including head coverings and other obstructions.
  * **Enhanced Expression Analysis**: Explore more advanced facial expression recognition models for improved accuracy and the ability to detect a broader range of non-neutral expressions.
  * **User Interface Enhancements**: Further improve the user interface for better clarity and user experience.

### References

  * [Face Detection Using Cascade Classifier using OpenCV Python](https://www.geeksforgeeks.org/face-detection-using-cascade-classifier-using-opencv-python/)
  * [Efficient way to detect white background in image](https://stackoverflow.com/questions/64304446/efficient-way-to-detect-white-background-in-image)
  * [Glasses-Detection GitHub Repository](https://github.com/siddh30/Glasses-Detection/tree/main) - Inspiration and techniques for improved glasses detection using facial landmarks.
  * [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker) - Documentation for MediaPipe's face landmarking solution, providing context for its capabilities.
  * [Dlib Documentation](http://dlib.net/) - Comprehensive documentation for the Dlib C++ library, which includes powerful tools for facial landmark detection.
  * [FER - Facial Emotion Recognition Library](https://pypi.org/project/fer/) - Information about the FER library used for emotion analysis.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
