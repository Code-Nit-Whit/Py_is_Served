# Py_is_Served  
Python's http.server module wrapped in a graphical interface with hot reloading, configurability, and a strong focus on ease of use. Upcoming v0.1.0 release to include prebuilt executable binaries for the major desktop platforms and possibly an installer for quick, hands-free setup.

This project is still in early development. As of now, the server is functional. Testing and fine-tuning are ongoing for hot reloading functionality and may be usable by the time anyone gets around to reading this.

---

### Dependencies and Compatibility

**Py_is_Served** is currently set up for Linux and Python 3.8 and above. While care is being taken to include non-system-specific libraries, syntax and functionality may differ slightly across operating systems. If you find that something is not working on your platform, please let me know with an issue report or feature request. Minor adjustments may be necessary for versions of Python older than 3.8.

To test or use this module pre-release, the following dependencies will need to be installed:

| Library  | Installation (pip)    | Installation (apt)            | Size Estimate |
|----------|------------------------|-------------------------------|---------------|
| keyboard | `pip install keyboard` | `sudo apt install python3-keyboard` | ~1MB  |
| watchdog | `pip install watchdog` | `sudo apt install python3-watchdog` | ~1.5MB |

- Size estimates are approximations and may vary depending on the specific version and distribution.
- Consider using virtual environments to manage dependencies for your project and avoid conflicts with system-wide installations.
- `os`, `re`, `threading`, `datetime`, `webbrowser`, `http.server`, `traceback`, `tkinter`: These are all part of the Python standard library and come pre-installed with Python 3 on most Linux distributions. No additional installation is required in most cases. Note that this might vary depending on your system configuration, especially if Python was pre-installed.

To check for the availability of each library:

**Using pip**  
`pip show <library name>`

**Using Aptitude (apt)**  
`apt list` or `apt --installed <library name>`

---

### Using Py_is_Served

With all dependencies in place, the main script, `local_server`, can be run with pip in the terminal using `python3 local_server.py` with the terminal currently navigated to the directory or virtual environment containing the script.

Currently, configurations can be set using the **"Configuration Variables"** at the top of the main script.

You will be prompted to select your **entry point file** through a file system dialogue.

Once the correct file is chosen, it will be <ins>automatically served to your default browser using your chosen network address.</ins>

Logging is currently set up both for in the terminal and in a logging file that can be found in the script's root directory. The logging is currently very verbose. This can be changed by altering the `custom_log_message` function near the top of the main script.

Proper logging and future configuration implementation rely on the script remaining in its home directory. Unlike standalone http servers, this script does not require being run from inside of your project's directory.

Please let me know about any issues, bugs, or incompatibilities you run into! I'm hoping to have the first version of this completed soon and simpler interfacing implemented.

--- 