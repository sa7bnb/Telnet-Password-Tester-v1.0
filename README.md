# Telnet Password Tester v1.0

A GUI-based tool for testing default and common passwords against network devices via Telnet. Built to recover the root password on a network camera I own, after the default credentials were unknown.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## Background

I purchased a network camera (IP camera) that runs a Linux-based firmware with Telnet access enabled. The default root password was not documented, so I built this tool to systematically test known default passwords commonly used by IP camera manufacturers and IoT devices.

**This tool is intended for use on devices you own.** Only use it on hardware and networks you have authorization to access.

## Features

- **Graphical user interface** — no command line needed
- **Configurable target** — set host, port, username, and timeout
- **Custom password lists** — load any `.txt` file with one password per line
- **Browse button** — file picker dialog for selecting password files
- **Adjustable delay** — set the delay between login attempts to avoid lockouts
- **Progress bar** — real-time progress with percentage display
- **Color-coded log** — green for success, grey for failed attempts, blue for info, red for errors
- **Start/Stop control** — stop the test at any time
- **Result banner** — clear indication when a password is found (or not)
- **Comment support** — lines starting with `#` in the password file are ignored
- **Duplicate removal** — automatically skips duplicate passwords

## Screenshot

![Telnet Password Tester v1.0](https://raw.githubusercontent.com/sa7bnb/Telnet-Password-Tester-v1.0/main/image.png)

## Installation

### Windows (pre-built executable)

A pre-built `.exe` file is available under [Releases](../../releases). Download the latest release and extract it. The archive contains:

- `Telnet Password Tester.exe` — the application
- `passwords.txt` — the password wordlist

Place both files in the same folder and run the `.exe`. No Python installation required.

### Windows / Linux (from source)

Requires **Python 3.8+** with `tkinter` (included by default on Windows).

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/telnet-password-tester.git
cd telnet-password-tester

# Run the application
python3 Telnet_Password_Tester.py
```

On Linux, if `tkinter` is not installed:

```bash
sudo apt install python3-tk
```

## Usage

1. **Host** — enter the IP address of the target device
2. **Port** — Telnet port (default: 23)
3. **Username** — the username to authenticate with (default: root)
4. **Timeout** — connection timeout in seconds
5. **File** — select a password list file (use `Browse...` or type the path)
6. **Delay** — time between attempts in seconds (increase if the device locks out)
7. Click **Start** to begin testing
8. Click **Stop** at any time to abort

When a password is found, it is displayed in the log and in a green result banner. If no password matches, a red banner is shown instead.

## Password List

The included `passwords.txt` contains **757 unique passwords** compiled from multiple sources:

- **Mirai botnet** default credentials
- **IP camera defaults** for 50+ manufacturers (Hikvision, Dahua, Axis, Foscam, Reolink, Samsung, etc.)
- **Tuya / Chinese camera** passwords (cracked hashes from security research)
- **Router and network device** defaults
- **Common numeric passwords** and keyboard patterns
- **IoT and embedded system** defaults
- **SecLists / NCSC** most common passwords

You can use your own password file — just create a text file with one password per line. Lines starting with `#` are treated as comments and ignored.

## How It Works

The tool connects to the target via Telnet, sends the username and password, and checks the response for shell prompt characters (`#`, `$`, `>`) that indicate a successful login. Failed attempts are detected by the absence of these prompts or the presence of error messages like "incorrect" or "failed".

Each attempt opens a new Telnet connection to avoid session state issues.

## Disclaimer

This tool is provided for **educational and authorized testing purposes only**. I built it to recover access to my own network camera. You are solely responsible for ensuring you have proper authorization before testing any device. Unauthorized access to computer systems is illegal.

## Author

Developed by **SA7BNB - Isak** — [github.com/sa7bnb](https://github.com/sa7bnb)

## License

MIT License — see [LICENSE](LICENSE) for details.
