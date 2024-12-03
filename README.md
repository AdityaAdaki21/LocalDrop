# LocalDrop

A modern, feature-rich file server with a beautiful web interface. This application allows you to easily share files and folders across your local network with drag-and-drop support, dark mode, and more.

## Features

- 📁 Browse files and folders with an intuitive interface
- ⬆️ Upload files with drag-and-drop support
- ⬇️ Download files and folders as ZIP
- 🌓 Light/Dark theme support
- 📊 View detailed file and directory information
- 🔄 Real-time updates
- 🌐 Access from any device on your local network

## Screenshots

[adding screenshots later]

## Requirements

- Python 3.9
- Required Python packages (see `requirements.txt`)
- Modern web browser with JavaScript enabled

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AdityaAdaki21/file-server.git
   cd file-server
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python app.py
   ```

4. Access the file server:
   - Local access: `http://localhost:8000`
   - Network access: `http://<your-ip-address>:8000`

## Usage

### Basic Navigation
- Click on folders to navigate into them
- Use the breadcrumb navigation to go back
- Click the home icon to return to the root directory

### File Operations
- **Upload**: Drag and drop files onto the page or click the upload button
- **Download**: Click the download icon on any file
- **Download Folder**: Use the context menu (⋮) to download a folder as ZIP
- **View Info**: Click the context menu (⋮) and select "Info" to view file/folder details

### Theme Switching
Click the moon/sun icon in the top-right corner to switch between light and dark themes.

## Development

The application is built with:
- Backend: Python with `http.server`
- Frontend: HTML5, CSS3, JavaScript
- UI Framework: Bootstrap 5
- Icons: Font Awesome

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

