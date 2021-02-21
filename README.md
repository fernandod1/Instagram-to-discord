# Instagram to discord post images

This script executes 2 actions:

1. Monitors for new image posted in a instagram account.
2. If found new image, a bot posts new instagram image in a discord channel.
3. Repeat after set interval.

## Requirements:

- Python v3
- Python module re, json, requests

## Usage:

Install the dependencies
```shell
python3 -m pip install -r requirements.txt
```

Copy over the config.example.yml
```shell
cp config.example.yml config.yml
```
Fill out config.yml

Run the script
```shell
python3 main.py
```


## Collaborations:

Collaborations to improve script are always welcome.
