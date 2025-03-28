# DYNAMIC THREAT RESPONSE
It is a real-time process monitoring tool designed to track system performance, detect high-CPU usage applications, and automatically terminate suspicious processes. It also features an interactive web-based dashboard for visualizing system health and managing processes efficiently. This project showcases core operating system concepts, including process management, resource monitoring, and automation, making it a practical tool for both system administrators and developers.

**KEY FEATURES**
- Monitor real-time CPU and memory usage  
- Detect resource-intensive or suspicious processes  
- Terminate high-CPU usage processes automatically  
- Provide an intuitive dashboard for manual and automated control

 # Process Monitoring  
- Continuously tracks all running processes  
- Displays CPU and memory usage per process  
- Supports whitelisting of system-critical applications  
- Configurable threat detection threshold  

# Automated Process Management  
- Runs a background scanner every 5 seconds  
- Automatically terminates processes exceeding CPU limits  
- Maintains a threat history log for future reference

# Web-Based Dashboard  
- Displays a live process list with sorting and filtering options  
- Shows system health metrics (CPU load, RAM usage, uptime)  
- Allows manual process termination from the UI  
- Provides historical threat visualizations

## Technology Stack  

This project is built using:  

### Backend:  
- Python 3.x – Core language for logic and processing  
- Flask – Web framework for handling API requests  
- psutil – Library for system monitoring and process management  
- Threading – Background execution for continuous monitoring  

### Frontend:  
- Vanilla JavaScript – Interactive UI functionality  
- HTML5/CSS3 – Web dashboard design and layout  
- Fetch API – For backend communication

## Installation & Setup  

### Prerequisites  
Ensure you have the following installed:  
- Python 3.7+  
- Windows OS (Compatible with Linux/macOS with minor changes)  
- Git (optional for cloning the repository)
