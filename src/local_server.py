import os
import re
import threading
import keyboard
import datetime
import webbrowser
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import traceback 
import tkinter as tk
from tkinter import filedialog

def choose_file():#handles the file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    initial_dir = os.path.expanduser("~")  # Get user's home directory
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Choose the Entry Point File")
    return file_path

# Configuration Variables
PORT = 8000 #
IPV4 = '0.0.0.0' #
FILE_PATH_SERVED = choose_file() #set using a while dialog when the script is first run
FILE_EXTENSIONS = ('.html', '.css', '.js', '.json') #ad any additional languages here thay may change your project's content when altered

# Global Variables
NETWORK_ADDRESS = f"{IPV4}:{PORT}" #used for automatically loading your project into the browser
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))#parent dir of the main script's src dir
SERVER_LOG_PATH = os.path.join(PARENT_DIR, "logs", "serverLog.txt") #where the custom logging fucntion can fins the log file
WATCH_PATH = os.path.dirname(FILE_PATH_SERVED) #The folder that your entrry file is contained in. Child directories are also watched by default

# MIME type mapping (expand as needed)
MIME_TYPES = { #used to ensure proper MIME type is sent to the roiwer in the response header. Scrucial when using ESM modules, etc. 
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json'
    # ... will be expanded
}

# Logging function
def custom_log_message(log_type, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{log_type.upper()}] {message}\n"
    with open(SERVER_LOG_PATH, 'a') as file:
        file.write(log_entry)
    print(log_entry, end='')

# Function to stop the server
def stop_server():
    try:
        custom_log_message("info", "Stopping server...")
        os.system("pkill -f 'python web-server.py'")
    except Exception as e:
        custom_log_message("error", f"An error occurred while stopping the server: {e}\n{traceback.format_exc()}")

# Function to open URL in the browser automatically
def open_url():
    try:
        url = f'http://{NETWORK_ADDRESS}'
        webbrowser.open(url)
    except Exception as e:
        custom_log_message("error", f"An error occurred while opening the URL: {e}\n{traceback.format_exc()}")


# Custom request handler
class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        try:
            self.send_no_cache_headers()
            super().end_headers()
        except Exception as e:
            custom_log_message("error", f"An error occurred while sending headers: {e}\n{traceback.format_exc()}")

    def send_no_cache_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')

    def do_GET(self):
        try:
            # Extract requested path from GET request
            requested_path = self.path.strip('/')

            # If no file is requested, serve the default file
            if not requested_path:
                file_to_serve = FILE_PATH_SERVED
            else:
                # Handle potential path traversal attacks
                if '..' in requested_path or requested_path.startswith('/'):
                    self.send_error(403, 'Forbidden')
                    return

                # Combine directory and requested path
                file_to_serve = os.path.join(os.path.dirname(FILE_PATH_SERVED), requested_path)

            # Check if the file exists and is accessible
            if not os.path.isfile(file_to_serve):
                self.send_error(404, 'File Not Found')
                return

            # Set default content type based on file extension
            custom_log_message("info", MIME_TYPES.get(os.path.splitext(file_to_serve)[1].lower(), 'application/octet-stream'))
            content_type = MIME_TYPES.get(os.path.splitext(file_to_serve)[1].lower(), 'application/octet-stream')


            # Check for overrides in Content-Type header (optional)
            if self.headers.get('Content-Type'):
                content_type = self.headers.get('Content-Type')
                # Validate and sanitize content type if necessary

            # Check for the "Trigger-Refresh" header (optional)
            if self.headers.get('Trigger-Refresh') == 'True':
                self.send_response(302)  # Send a redirect response
                self.send_header('Location', '/')  # Redirect to the same URL
                self.end_headers()
                return

            # Open the file and send its contents
            with open(file_to_serve, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(file.read())

        except Exception as e:
            self.send_error(500, 'Internal Server Error')
            custom_log_message("error", f"Error serving file: {e}")

# Function to run the HTTP server
def run(server_class=HTTPServer, handler_class=NoCacheHandler, port=PORT, file_to_serve=FILE_PATH_SERVED):
    try:
        server_address = (IPV4, port)
        handler_class.directory = os.path.dirname(file_to_serve)  # Set the directory for file serving
        handler_class.default_file = os.path.basename(file_to_serve)  # Set the default file to serve
        httpd = server_class(server_address, handler_class)
        open_url()
        custom_log_message("info", f"Server started on port {port} serving file {file_to_serve}")
        httpd.serve_forever()
    except OSError as e:
        custom_log_message("error", f"Error: {e}. Port {port} might be in use.\n{traceback.format_exc()}")
    except Exception as e:
        custom_log_message("error", f"An unexpected error occurred while starting the server: {e}\n{traceback.format_exc()}")

# File modification/ hot reloading handler
class RefreshHandler(FileSystemEventHandler):
    def trigger_refresh():
        try:
            # Use the NETWORK_ADDRESS variable for the server URL
            url = f"http://{NETWORK_ADDRESS}/trigger-refresh"  # Example endpoint
            headers = {"Trigger-Refresh": "True"}
            # Add data to request body if needed (e.g., file info)
            # data = {"changed_file": "path/to/file"}
            response = requests.post(url, headers=headers, data=data)  # Optional data
            if response.status_code != 200:
                custom_log_message("error", f"Failed to trigger refresh: {response.status_code}")
            else:
                # Optionally log or process the server's response
                custom_log_message("info", f"Server response: {response.text}")
        except Exception as e:
            custom_log_message("error", f"Failed to trigger refresh: {e}")

    def on_modified(self, event):
        if event.src_path.endswith(FILE_EXTENSIONS):
            custom_log_message("info", f"File {event.src_path} has been modified. Triggering refresh...")
            try:
                self.trigger_refresh()
            except Exception as e:
                custom_log_message("error", f"Failed to trigger refresh: {e}")

#where evrthing gets set in motion
if __name__ == '__main__':
    observer = Observer()
    observer_started = False
    try:
        # Observer to watch for file modifications
        custom_log_message("info",WATCH_PATH)
        observer.schedule(RefreshHandler(), path=WATCH_PATH, recursive=True)
        observer.start()
        observer_started = True

        # Start the HTTP server in a separate thread. Calls the run function
        run_thread = threading.Thread(target=run)
        run_thread.start()

        # Wait for the run_thread to finish
        run_thread.join()

    except KeyboardInterrupt:
        custom_log_message("info", "Keyboard interrupt detected. Exiting...")
    except Exception as e:
        custom_log_message("error", f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
    finally:
        # Stop the observer when the script exits
        if observer_started:
            observer.stop()
            observer.join()
