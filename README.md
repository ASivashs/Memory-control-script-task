## Memory usage task

This script is designed to monitor the memory consumption of a system and generate an alarm by sending an HTTP request to an API when the memory usage exceeds a specified threshold.


## Install 

1. Clone the repository:
```
git clone <repo url>
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Grant execution permission to the script:
```
chmod +x ./memory_control.py
```


## Usage

To run the script with default parameters (80% of memory and http://localhost:8000), use the following command:
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
