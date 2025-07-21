
# Password Guardian Pro

**Password Guardian Pro** is a desktop application for checking password strength and security. It helps users evaluate passwords, detect common weaknesses, and check if passwords have been exposed in known data breaches.

## 📸 Screenshots

### 1. Launch Screen  
![Launch Screen](assets/screen%20shot%201.png)  
*Clean interface with intuitive input fields.*

### 2. Password Analysis  
![Password Analysis](assets/screen%20shot%202.png)  
*Breaks down password strength by length, character diversity, and repetition.*

### 3. Breach Detection Result  
![Breach Detection](assets/screen%20shot%204.png)  
*Checks if the password appears in known data breaches using online APIs.*

### 4. PDF Export Confirmation  
![PDF Export](assets/screen%20shot%203.png)  
*Generates a downloadable PDF report summarizing the analysis.*

> ✅ Make sure these image files are located in `assets/screenshots/` and named exactly as shown above. GitHub is case-sensitive and doesn’t like spaces in filenames.

## ✨ Features

- **Password Strength Checker:** Evaluates passwords for length, complexity, and common patterns  
- **Breach Detection:** Uses online services to check if a password has been compromised  
- **PDF Export:** Generates a PDF report of password analysis  
- **Simple GUI:** Built with FreeSimpleGUI for ease of use  
- **Custom Icons:** Uses branded logo and icons for a professional touch

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Windows OS (tested)
- Internet connection (for breach detection)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/HackRore/Password_Guardian_Pro.git
   ```

2. Run the build script to set up the environment and dependencies:
   ```sh
   build.bat
   ```

3. The executable will be available in the `dist` folder as `main.exe`.

### Running from Source

1. Install dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```

2. Run the application:
   ```sh
   python main.py
   ```

## 🧪 Usage

1. Launch the application  
2. Enter a password to analyze  
3. View strength, breach status, and export results as PDF

## 📁 Project Structure

| File / Folder       | Description                              |
|---------------------|------------------------------------------|
| `main.py`           | Main application logic and GUI           |
| `build.bat`         | Build script for packaging the app       |
| `requirements.txt`  | Python dependencies                      |
| `assets/`           | Icons, logo images, and screenshots      |
| `dist/`             | Output folder for built executables      |

## 📦 Dependencies

- [FreeSimpleGUI](https://pypi.org/project/PySimpleGUI/)
- [requests](https://pypi.org/project/requests/)
- [reportlab](https://pypi.org/project/reportlab/)

## 📄 License

This project is for **educational purposes only**.
