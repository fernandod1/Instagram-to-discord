# Instagram to discord post images

This script executes 2 actions:

1. Monitors for new image posted in a instagram account.
2. If found new image, a bot posts new instagram image in a discord channel.
3. Repeat after set interval.

## Requirements:

- Python v3
- Python module re, json, requests

## Usage:

Environment Variables:

- Set IG_USERNAME to username account you want to monitor. Example - ladygaga
- Set WEBHOOK_URL to Discord account webhook url. To know how, just Google: "how to create webhook discord".
- Set TIME_INTERVAL to the time in seconds in between each check for a new post. Example - 1.5, 600 (default=600)

## Collaborations:

Collaborations to improve script are always welcome.
