#  Scaling Range 📏

A simple and intuitive GUI application for linear scaling of 3D coordinates.

## 🚀 Functionality

This application provides a user-friendly interface for scaling 3D coordinates. It's designed to be a simple and efficient tool for developers, engineers, and anyone who needs to perform linear scaling calculations.

### ✨ Features

*   **Real-time Scaling:** The application calculates the scaled values in real-time as you type, providing immediate feedback.
*   **Flexible Input:** You can choose to scale based on `X`, `Y`, or `Z` coordinates, and the other two coordinates will be calculated automatically.
*   **Hexadecimal Support:** The `Z` coordinate can be entered in hexadecimal format, which is useful for certain applications.
*   **Error Handling:** The application has built-in error handling to prevent crashes from invalid input, such as non-numeric values or division by zero.

## ⚠️ Limitations

While this application is a useful tool for simple linear scaling, it has some limitations:

*   **No Support for Non-Linear Scaling:** The application only supports linear scaling. It cannot be used for non-linear scaling, such as logarithmic or exponential scaling.
*   **No Support for Batch Processing:** The application can only process one set of coordinates at a time. It does not support batch processing of multiple sets of coordinates.
*   **No Support for Saving and Loading Configurations:** The application does not have the ability to save and load scaling configurations. You will need to re-enter the scaling parameters every time you use the application.

## 🤖 How it Works

The application uses a linear scaling algorithm to calculate the corresponding `Y` and `Z` coordinates for a given `X` coordinate, and vice-versa. The scaling is based on a defined range, which is set by two reference points: `(X1, Y1, Z1)` and `(X2, Y2, Z2)`.

The core of the calculation is the `_calculate_scaled_value` method, which takes an input value and scales it to a new range. The method uses the following formula to calculate the scaled value:

```
scaled_value = slope * input_value + intercept
```

where:

*   `slope = (output_end - output_start) / (input_end - input_start)`
*   `intercept = output_start - (slope * input_start)`

## 📦 Dependencies

*   `customtkinter`

## 🏃‍♀️ How to Run

1.  Clone the repository.
2.  Install the dependencies:
    ```
    pip install customtkinter
    ```
3.  Run the application:
    ```
    python scaling.py
    ```

## 🛠️ How to Build

To build the executable, you will need `pyinstaller`.

1.  Install `pyinstaller`:
    ```
    pip install pyinstaller
    ```
2.  Build the executable:
    ```
    pyinstaller --onefile --windowed --icon=logo.ico scaling.py
    ```

## 🐳 How to Use the Dockerfile

To build and run the application with Docker, you will need to have Docker installed on your system.

1.  Build the Docker image:
    ```
    docker build -t scaling-app .
    ```
2.  Run the Docker container:
    ```
    docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix scaling-app
    ```
