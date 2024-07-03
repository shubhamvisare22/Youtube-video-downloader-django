# YouTube Downloader

**Django-based app to download single or multiple YouTube videos in various resolutions, supporting ZIP bundling and real-time notifications.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Introduction

This project provides a web-based interface for downloading YouTube videos either as individual files or bundled in a ZIP file. It supports selecting video resolutions and includes real-time notifications and loading indicators.

## Features

- Download single or multiple YouTube videos.
- Choose video resolution before downloading.
- ZIP multiple videos for bulk downloads.
- Real-time notifications for success and error messages.
- Loader overlay for indicating ongoing processes.

## Technologies Used

- **Django**: Web framework for the backend.
- **pytube**: For handling YouTube video downloads.
- **Bootstrap**: CSS framework for styling.
- **JavaScript**: For client-side functionality.
- **jQuery**: Simplifies JavaScript code.
- **Toastr**: For notifications.
- **SweetAlert2**: For beautiful alerts and modals.

## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/shubhamvisare22/YouTubeDownloader.git
   cd YouTubeDownloader
   ```
2. **Create and Activate Virtual Environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```
5. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```
6. **Access the Application:**
   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

1. **Home Page:**

   - Enter a YouTube video URL or multiple URLs separated by commas.
   - Select the desired video resolution.
   - Click the "Download" button.
2. **Download Confirmation:**

   - A success message will appear with a "Download" button.
   - Click the "Download" button to download the video or ZIP file.
3. **Notifications:**

   - Toastr notifications will provide real-time feedback on the download status.



## API Endpoints

- **`/download`**: Handles POST requests for downloading videos. Expects `link`, `resolution`, and `is_single` in the request body.
- **`/download_video`**: Handles POST requests for downloading the video file. Expects `filename` in the request body.

## Troubleshooting

- **CSRF Token Issues**: Ensure that the CSRF token is correctly included in AJAX requests. Check that it's extracted from the meta tag or input field as expected.
- **File Not Found**: Verify that the files are correctly saved in the specified directories and that paths are correctly configured in the Django settings.
- **Permission Issues**: Ensure that the application has the necessary permissions to read and write files in the `downloaded_videos` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
