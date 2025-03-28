# Landcover Project

This repository contains a landcover classification project, which includes a Django-based backend (`landcover_project`) and a frontend (`landcover-frontend`). The backend provides APIs for landcover data processing, while the frontend offers a user interface for interacting with the system.

## Project Structure

landcover_project/ ├── db.sqlite3 # SQLite database file ├── debug_mask.png # Debugging image (mask) ├── debug_original.png # Debugging image (original) ├── manage.py # Django management script ├── trained_landcover_unet_efficientnet-b0_epochs18_patch512_batch16.pth # Pre-trained model ├── landcover_api/ # Django app for the API │ ├── init.py │ ├── admin.py │ ├── apps.py │ ├── models.py # Database models │ ├── serializers.py # API serializers │ ├── tests.py # Unit tests │ ├── urls.py # API routes │ ├── views.py # API views │ ├── migrations/ # Database migrations │ └── pycache/ # Compiled Python files └── landcover_project/ # Django project settings and configurations

landcover-frontend/ ├── .gitignore # Git ignore file ├── package.json # Frontend dependencies ├── README.md # Frontend-specific README ├── public/ # Static files └── src/ # Frontend source code

lcss/ ├── pyvenv.cfg # Python virtual environment configuration ├── Include/ # Virtual environment include files ├── Lib/ # Virtual environment libraries ├── Scripts/ # Virtual environment scripts └── share/ # Shared files


## Features

- **Backend**: A Django-based API for landcover classification.
- **Frontend**: A React-based user interface for interacting with the backend.
- **Pre-trained Model**: Includes a pre-trained U-Net model with EfficientNet-B0 for landcover classification.
- **Database**: SQLite database for storing application data.

## Prerequisites

- Python 3.11
- Node.js and npm
- Virtual environment (optional)

## Setup Instructions

### Backend

1. Navigate to the backend directory:
   ```bash
   cd landcover_project
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv lcss
   source lcss/Scripts/activate  # On Windows
   source lcss/bin/activate      # On macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run database migrations:
   ```
   python manage.py migrate
   ```
7. Start the development server:
   ```
   python manage.py runserver
   ```

###Frontend

1. Navigate to the frontend directory:
   ```
   cd landcover-frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
5. Start the development server:
   ```
   npm start
   ```



###Usage
Access the backend API at http://127.0.0.1:8000/.
Access the frontend at http://localhost:3000/.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

##License
This project is licensed under the MIT License. See the LICENSE file for details.







   
