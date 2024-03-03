# Installation Instructions for Ovecell Data Pipeline Application

A new data pipeline application for Ovecell to analyze user account data from their games "Wild Wild Chords" and "HarmonicaBots". This document provides instructions for installing and running the application either via Docker or directly from a development environment.

## Running with Docker

To run the data pipeline application using Docker, follow these steps:

1. **Build the Docker Image**

    First, build the Docker image for the application using the following command:

    ```bash
    docker build -t data_loader .
    ```

    This command builds a Docker image named `data_loader` based on the Dockerfile in the current directory.

2. **Run the Docker Container**

    After building the image, you can run the application as a Docker container. To load data for a specific game on a specific date, use one of the following commands:

    - For "Wild Wild Chords":

        ```bash
        docker run -v ./data:/data data_loader wwc 2021-04-28
        ```
        and
        ```bash
        docker run -v ./data:/data data_loader wwc 2021-04-29
        ```

    - For "HarmonicaBots":

        ```bash
        docker run -v ./data:/data data_loader hb 2021-04-28
        ```

    These commands run the `data_loader` container, mounting the local `./data` directory to the `/data` directory inside the container. Replace `2021-04-29` or `2021-04-28` with the desired date to process the corresponding data.

## Running from the Development Environment

For developers working directly in the development environment, follow these steps:

1. **Install Pipenv**

    Ensure that Pipenv is installed on your system. If not, you can install it using pip:

    ```bash
    pip install pipenv
    ```

2. **Install Dependencies**

    Next, install the project dependencies within a virtual environment managed by Pipenv:

    ```bash
    pipenv install -d
    ```

3. **Run the Script**

    Finally, run the data loading script for a specific game and date. For example, to load data for "HarmonicaBots" from April 28, 2021, use the following command:

    ```bash
    python src/load.py hb 2021-04-28
    ```

Replace `hb 2021-04-28` with `wwc 2021-04-29` to load data for "Wild Wild Chords" from April 29, 2021, or adjust the parameters as needed to process different data.
