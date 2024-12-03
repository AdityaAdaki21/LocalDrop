import http.server
import socketserver
import os
import json
from urllib.parse import unquote
import logging
import socket
from socketserver import ThreadingTCPServer
import re
import zipfile
import io
import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_local_ip():
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# Add security check for path traversal attempts
def is_safe_path(base_path, requested_path):
    # Convert to absolute paths
    base_path = os.path.abspath(base_path)
    requested_path = os.path.abspath(requested_path)
    # Check if the requested path starts with the base path
    return requested_path.startswith(base_path)

class FileServerHandler(http.server.SimpleHTTPRequestHandler):
    def get_folder_name(self):
        return os.path.basename(os.getcwd()) or "Root"

    def do_GET(self):
        # Decode URL-encoded path
        path = unquote(self.path)
        
        logger.debug(f"Received GET request for path: {path}")
        
        client_ip = self.client_address[0]
        logger.info(f"Request from client IP: {client_ip}")
        
        # Handle folder download requests
        if self.path.startswith('/api/download-folder/'):
            try:
                folder_path = unquote(self.path[19:])  # Remove '/api/download-folder/'
                folder_path = os.path.normpath(folder_path)
                
                # Security check
                if not is_safe_path(os.getcwd(), folder_path):
                    self.send_error(403, "Access denied")
                    return
                
                if not os.path.exists(folder_path):
                    self.send_error(404, "Folder not found")
                    return
                
                if not os.path.isdir(folder_path):
                    self.send_error(400, "Path is not a directory")
                    return

                memory_file = io.BytesIO()
                
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arc_name = os.path.relpath(file_path, folder_path)
                            try:
                                zf.write(file_path, arc_name)
                            except PermissionError:
                                logger.warning(f"Permission denied for file: {file_path}")
                                continue
                
                memory_file.seek(0)
                folder_name = os.path.basename(folder_path)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', f'attachment; filename="{folder_name}.zip"')
                self.end_headers()
                self.wfile.write(memory_file.getvalue())
                return
            except Exception as e:
                logger.error(f"Error creating zip file: {str(e)}")
                self.send_error(500, str(e))
                return

        # Handle info requests
        if self.path.startswith('/api/info'):
            try:
                # Remove '/api/info/' and handle path properly
                item_path = unquote(self.path[9:]).strip('/')
                # Convert to proper system path
                item_path = os.path.normpath(item_path)
                
                # Security check
                if not is_safe_path(os.getcwd(), item_path):
                    self.send_error(403, "Access denied")
                    return
                
                # If path is empty, use current directory
                if not item_path:
                    item_path = '.'
                
                logger.debug(f"Getting info for path: {item_path}")
                
                if not os.path.exists(item_path):
                    self.send_error(404, f"Path not found: {item_path}")
                    return
                
                try:
                    stats = os.stat(item_path)
                except PermissionError:
                    self.send_error(403, "Permission denied")
                    return
                
                info = {
                    'name': os.path.basename(item_path) or item_path,
                    'size': stats.st_size,
                    'created': datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    'modified': datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'is_dir': os.path.isdir(item_path),
                }
                
                if info['is_dir']:
                    # Count files and calculate total size for directories
                    total_size = 0
                    file_count = 0
                    for root, dirs, files in os.walk(item_path):
                        file_count += len(files)
                        for file in files:
                            try:
                                total_size += os.path.getsize(os.path.join(root, file))
                            except (PermissionError, OSError):
                                continue
                    info['file_count'] = file_count
                    info['total_size'] = total_size
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(info).encode())
                return
            except Exception as e:
                logger.error(f"Error getting item info: {str(e)}")
                self.send_error(500, str(e))
                return

        # Handle API requests for directory listing
        if path.startswith('/api/list'):
            try:
                requested_path = path[9:] or '.'  # Remove '/api/list' prefix
                logger.debug(f"Listing directory contents for: {requested_path}")
                
                # Get directory contents
                items = []
                for item in os.listdir(requested_path):
                    full_path = os.path.join(requested_path, item)
                    items.append({
                        'name': item,
                        'is_dir': os.path.isdir(full_path),
                        'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                    })
                
                # Send JSON response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(items).encode())
                logger.debug(f"Successfully sent directory listing with {len(items)} items")
                
            except Exception as e:
                logger.error(f"Error processing directory listing: {str(e)}")
                self.send_error(500, str(e))
            return

        # Serve the main HTML page for root requests
        if path == '/':
            try:
                logger.debug("Serving main HTML page")
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                
                # Read the index.html file
                with open('index.html', 'rb') as f:
                    html_content = f.read().decode('utf-8')
                    # Replace the placeholder with actual folder name
                    folder_name = self.get_folder_name()
                    html_content = html_content.replace('LocalDrop', folder_name)
                    self.wfile.write(html_content.encode())
                    
                logger.debug("Successfully served main HTML page")
                return
            except Exception as e:
                logger.error(f"Error serving main HTML page: {str(e)}")
                self.send_error(500, str(e))
                return

        # For all other requests, use the default handler
        return super().do_GET()

    def do_POST(self):
        # Handle file upload
        if self.path == '/api/upload':
            try:
                # Get the content length
                content_length = int(self.headers['Content-Length'])
                
                # Get the upload path from headers
                upload_path = unquote(self.headers.get('X-Upload-Path', '.'))
                
                # Parse multipart form data
                content_type = self.headers['Content-Type']
                if not content_type.startswith('multipart/form-data'):
                    raise ValueError("Expected multipart form data")
                
                # Read the file data
                form_data = self.rfile.read(content_length)
                
                # Find the boundary
                boundary = content_type.split('=')[1].encode()
                
                # Parse the form data to get file content
                parts = form_data.split(boundary)
                for part in parts:
                    if b'filename=' in part:
                        # Extract filename
                        filename_match = re.search(b'filename="(.+?)"', part)
                        if filename_match:
                            filename = filename_match.group(1).decode()
                            # Find the actual file content
                            file_content = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]
                            
                            # Create full path
                            full_path = os.path.join(upload_path, filename)
                            
                            # Save the file
                            with open(full_path, 'wb') as f:
                                f.write(file_content)
                            
                            logger.info(f"File uploaded successfully: {filename}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
                
            except Exception as e:
                logger.error(f"Upload error: {str(e)}")
                self.send_error(500, str(e))
            return

def run_server(port=8000):
    try:
        # Use ThreadingTCPServer instead of TCPServer
        ThreadingTCPServer.allow_reuse_address = True
        handler = FileServerHandler
        server_ip = get_local_ip()
        with ThreadingTCPServer(("", port), handler) as httpd:
            logger.info(f"Server started at port {port}")
            logger.info(f"Server IP address: {server_ip}")
            logger.info(f"Access locally at: http://localhost:{port}")
            logger.info(f"Access from other devices at: http://{server_ip}:{port}")
            logger.info("Server is ready to handle multiple connections")
            httpd.serve_forever()
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise

if __name__ == "__main__":
    run_server()
