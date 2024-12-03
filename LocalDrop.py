import os
import sys
import logging
from app import run_server
import webbrowser
import threading
import time
import signal

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def shutdown_server(server, reason=""):
    """Gracefully shutdown the server"""
    print(f"\n{'=' * 40}")
    print(f"Shutting down server... {reason}")
    print(f"{'=' * 40}")
    
    try:
        server.shutdown()
        server.server_close()
        print("Server stopped successfully")
    except Exception as e:
        print(f"Error during shutdown: {e}")
    
    print("\nThank you for using LocalDrop!")
    print("Press Enter to exit...")
    sys.exit(0)

def handle_user_input(server):
    """Thread to handle user input for server shutdown"""
    while True:
        try:
            cmd = input().lower().strip()
            if cmd == 'exit' or cmd == 'quit':
                shutdown_server(server, "User requested exit")
                break
            elif cmd == 'help':
                print("\nAvailable commands:")
                print("  exit, quit - Stop the server and exit")
                print("  help      - Show this help message")
                print("  clear     - Clear the console")
            elif cmd == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nLocalDrop File Sharing Server")
                print("============================")
                print("\nType 'help' for available commands")
        except EOFError:
            break

def signal_handler(signum, frame):
    """Handle system signals"""
    print("\nReceived signal to terminate")
    shutdown_server(signal_handler.server, "Signal received")

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Set the index.html path
        index_path = get_resource_path('index.html')
        if not os.path.exists(index_path):
            logger.error(f"Could not find index.html at {index_path}")
            input("\nPress Enter to exit...")
            sys.exit(1)

        # Change working directory to where the executable is
        if getattr(sys, 'frozen', False):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\nLocalDrop File Sharing Server")
        print("============================")
        print("\nStarting server...")
        
        # Run the server with index.html path
        server = run_server(port=8000, index_path=index_path)
        
        # Store server instance in signal handler
        signal_handler.server = server
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print("\nServer is running!")
        print(f"{'=' * 40}")
        print("Available commands:")
        print("  exit, quit - Stop the server and exit")
        print("  help      - Show available commands")
        print("  clear     - Clear the console")
        print(f"{'=' * 40}\n")
        
        # Open browser automatically
        webbrowser.open('http://localhost:8000')
        
        # Start input thread for handling exit command
        input_handler = threading.Thread(target=handle_user_input, args=(server,))
        input_handler.daemon = True
        input_handler.start()
        
        # Keep the main thread running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            shutdown_server(server, "Ctrl+C pressed")

    except Exception as e:
        logger.error(f"Error starting server: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()