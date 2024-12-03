# LocalDrop 🚀

A modern, feature-rich file sharing server with a beautiful web interface. Share files and folders across your local network with drag-and-drop support, dark mode, and more. Perfect for quick file transfers between devices on your network.

## ✨ Features

- 🎯 **Simple Setup**: Single executable, no installation required
- 📱 **Responsive Design**: Works on all devices and screen sizes
- 🌓 **Dark/Light Theme**: Easy on the eyes, day or night
- ⚡ **Fast Transfers**: Direct device-to-device file sharing
- 🔍 **File Management**:
  - Browse files and folders with intuitive navigation
  - Upload files with drag-and-drop support
  - Download files and folders as ZIP
  - View detailed file/folder information
  - Real-time updates
- 🔒 **Security**: Basic path traversal protection
- 🌐 **Network Access**: Share files with any device on your local network

## 🖥️ Screenshots

[Coming Soon]

## 🚀 Quick Start

### Option 1: Download and Run (Recommended)

1. Download the latest `LocalDrop.exe` from the [Releases](https://github.com/AdityaAdaki21/LocalDrop/releases) page

2. When you try to run the executable, you may see a Windows Security warning:
   - "Windows protected your PC" message will appear
   - This is normal for unsigned executables
   - To run anyway:
     1. Click "More info"
     2. Click "Run anyway"
     > Note: This warning appears because the app isn't signed with a Microsoft certificate. The source code is open and available for review.

3. Using the Executable:
   - **Standalone Use**: 
     - Place `LocalDrop.exe` in any folder you want to share
     - Double-click to run - it will share the folder it's placed in
   
   - **Creating a Shortcut** (Recommended):
     - Right-click `LocalDrop.exe` → Create Shortcut
     - Move the shortcut to your desktop/preferred location
     - Right-click shortcut → Properties
     - Set "Start in" to your preferred share folder
     - Now you can run LocalDrop from anywhere while sharing your chosen folder

4. When you run LocalDrop:
   - A console window will open showing the server status
   - Your default browser will automatically open
   - Other devices can connect using the displayed network URL
   - The shared folder will be the one containing the exe (or specified in shortcut)

### Security Notes 🔒

1. **Windows SmartScreen Warning**:
   - This warning appears because the executable isn't digitally signed
   - The application is open-source, and you can:
     - Review the source code
     - Build it yourself from source
     - Run from source code directly

2. **Safe Usage**:
   - Only run LocalDrop on trusted networks (like your home network)
   - Anyone on your network can access the shared folder
   - Close the console window to stop sharing
   - The application only shares the folder it's placed in (or specified in shortcut)

### Common Use Cases

1. **Quick File Sharing**:
   ```
   Documents/
   ├── LocalDrop.exe     # Place exe here
   └── Files_to_share/   # Files you want to share
   ```

2. **Desktop Shortcut**:
   ```
   C:/Users/YourName/Desktop/
   └── LocalDrop.lnk     # Shortcut pointing to shared folder
   ```

3. **Portable Drive**:
   ```
   E:/                   # USB Drive
   ├── LocalDrop.exe     # Run from drive
   └── Shared_Files/     # Files on drive
   ```

### Option 2: Run from Source

#### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

```bash
# 1. Clone the repository
git clone https://github.com/AdityaAdaki21/LocalDrop.git
cd LocalDrop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python LocalDrop.py
```

## 📖 Usage Guide

### Starting the Server

1. Run `LocalDrop.exe` or `python LocalDrop.py`
2. The server will start and display:
   - Local URL (http://localhost:8000)
   - Network URL (http://your-ip:8000)
3. Your default browser will open automatically

### File Operations

#### Uploading Files
- **Drag & Drop**: Drag files directly into the browser window
- **Upload Button**: Click the upload button to select files

#### Downloading Files
- **Single File**: Click the download icon on any file
- **Folders**: Use the menu (⋮) to download folder as ZIP

#### Navigation
- Click folders to open them
- Use the breadcrumb navigation to go back
- Click the home icon to return to root

#### File Information
1. Click the menu icon (⋮) on any file/folder
2. Select "Info" to view details:
   - Size
   - Creation date
   - Modification date
   - File count (for folders)

### Theme Switching
- Click the moon/sun icon in the top-right corner
- Theme preference is saved automatically

### Server Commands
- Type `help` to view available commands
- Use `exit` or `quit` to stop the server
- Press `Ctrl+C` to force quit

## 🛠️ Development

### Building from Source

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
python build_exe.py
```

The executable will be created in the `dist` directory.

### Project Structure
```
LocalDrop/
├── app.py          # Core server implementation
├── LocalDrop.py    # Main application entry point
├── index.html      # Web interface
├── build_exe.py    # Build script
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
