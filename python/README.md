## Memory usage script in Python

<!-- This script is designed to monitor the memory consumption of a system and generate an alarm by sending an HTTP request to an API when the memory usage exceeds a specified threshold. -->


## Install 

1. Clone the repository:
```
git clone git@github.com:AntonioKampf/Memory-control-script-task.git
```

2. Install the required dependencies:
```
pip3 install -r requirements.txt
```

3. Grant execution permission to the script:
```
chmod +x ./memory_control.py
```


## Usage

To run the script with default parameters (80% of memory and http://127.0.0.1:8080/alarm), use the following command:
```
python3 ./memory_control.py
```

To specify the memory usage and request URL, use the following command:
```
python3 ./memory_control.py -m [memory usage percentage, e.g. 30, 40] -r [url]
```


## Help

To get help, run the script with the following command:
```
python3 ./memory_control.py --help
```
