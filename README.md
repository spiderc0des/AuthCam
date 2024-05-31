# AuthCam

AuthCam is a camera application designed to verify the integrity of pictures. It uses a Django REST Framework backend and a Kivy-based frontend to provide a seamless and secure user experience.

## Technologies Used
- **Backend:** Django REST Framework
- **Frontend:** Kivy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following tools installed:
- Python
- Pipenv
- Kivy

### Setup and Running

1. **Activate the virtual environment:**
   ```
   pipenv shell
   ```

2. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Navigate to the kivy directory where the Kivy application is located and start the application:**
   ```
   python main.py
   ```
