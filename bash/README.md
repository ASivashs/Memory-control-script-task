## Memory usage script in Bash

<!-- This script is designed to monitor the memory consumption of a system and generate an alarm by sending an HTTP request to an API when the memory usage exceeds a specified threshold. -->


## Install 

1. Clone the repository:
```
git clone git@github.com:AntonioKampf/Memory-control-script-task.git
```
2. Grant execution permission to the script:
```
chmod +x ./memory_control.sh
```


## Dependencies

If curl not installed in your system install it with command:

Debian/Ubuntu
```
apt install curl
```
CentOS/Red Hat
```
yum install curl
```


## Usage

To run the script with default parameters (80% of memory and http://127.0.0.1:8080/alarm), use the following command:
```
./memory_control.sh
```

To specify the memory usage and request URL, use the following command:
```
./memory_control.sh [memory usage percentage, e.g. 30, 40] [url]
```
