# GX HOF Creator

A comprehensive tool for creating and editing HOF files for buses in the OMSI (Omnibus Simulator) bus simulator. This application is specifically designed for managing Hanover destination display (GX7767) HOFs and provides an intuitive graphical interface for handling most aspects of HOF file creation and management.

## ✨ Features

- **🎯 Create and Edit HOF files:** Start from scratch or modify existing HOF files with full validation
- **💾 Database support:** Save and load your work in SQLite `.db` format for project management
- **🖥️ A GUI:** A graphical interface built with PySide6/Qt6
- **📊 Comprehensive Management:**
  - **Termini:** Define route destinations and terminus information
  - **Bus Stops:** Configure stop names, announcements, and timing
  - **DDU:** Set up fare information and pricing
  - **Routes:** Create and manage Infosystem trips and route definitions
- **🚀 Export to HOF:** Generate valid HOF files ready for OMSI integration
- **✅ Validation:** Built-in checks for data integrity and HOF format compliance

## 📋 Requirements

- **Python 3.12+** (tested on Python 3.12)
- **PySide6** (Qt6 framework for GUI)
- **SQLite3** (included with Python)

## Installation

### Option 1: Download Binary

1. Go to the [Releases](https://github.com/FreeHK-Lunity/GX_hof_creator/releases) page
2. Download the latest release binary
3. Run the executable

### Option 2: From Source

1. **Clone or download this repository:**

   ```bash
   git clone https://github.com/FreeHK-Lunity/GX_hof_creator.git
   cd GX_hof_creator
   ```

2. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python3 mainwindow.py
   ```

### Linux build

Build Linux executable on Linux; PyInstaller does not cross-compile:

```bash
python3 -m pip install -r requirements.txt pyinstaller
python3 build.py
./dist/MainWindow
```

## 🚀 Quick Start

1. **Launch the application** by running `python mainwindow.py`
2. **Choose an option:**
   - **Create New HOF:** Start with a blank project
   - **Open HOF File:** Load an existing GX7767 Hanover `.hof` file
   - **Open Database:** Load a saved project from `.db` file
3. **Add your data:**
   - Define bus stops and their properties
   - Set up route destinations (termini)
   - Configure pricing information (DDU)
   - Create route definitions (Infosystem)
4. **Export:** Generate your final `.hof` file for use in OMSI

## 📁 Project Structure

```text
GX_hof_creator/
├── mainwindow.py           # Main application entry point and GUI logic
├── HOF.py                  # Core HOF data structures and file handling
├── converter.py            # Qt UI to python conversion utility
├── mapParser.py           # Map data parsing functionality
├── requirements.txt       # Python dependencies
├── *.ui                   # Qt Designer interface files
├── ui_*.py               # Generated Python UI files
└── __pycache__/          # Python cache files
```

### Key Components

- **`mainwindow.py`**: Contains the main application logic, window management, and user interface handlers
- **`HOF.py`**: Defines the core data structures for HOF files including bus stops, routes, destinations, and pricing
- **`ui_*.py`**: Auto-generated files from Qt Designer `.ui` files - do not edit manually

## 📝 File Formats

### HOF Format

The application generates standard Hanover HOF files compatible with OMSI bus simulator.

### Database Format

Projects are saved in SQLite format for easy backup and version control.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 📄 License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/FreeHK-Lunity/GX_hof_creator/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, operating system, and steps to reproduce

---

Made with ❤️ for the OMSI community
