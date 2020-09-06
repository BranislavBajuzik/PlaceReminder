# PlaceReminder
Simple bucketlist-like CLI utility for places of interest

## Run
```shell
places.py [-h] file {add,remove,list,pick} [places [places ...]]
```

### positional arguments:
  - `file`
    - File to read/store the places in
  - `action`
    - Action to take
    - One of `add`, `remove`, `list`, `pick`

### optional arguments:
  - `places`
    - Optional, space-separated places
    - Places to add/remove
  - `-h`, `--help`
    - show this help message and exit

## Contribute

#### Setup environment
```Shell
python -m pip install -r requirements-dev.txt
pre-commit install
```
