# Instagram to discord post images

This script executes 2 actions:
1.) Monitors for new image posted in a instagram account (create a cronjob).
2.) If found new image, a bot post new instagram image in a discord channel.

REQUIREMENTS:

- Python v3
- Python module re, json, requests

USAGE:

1.) Replace INSTAGRAM_USERNAME with username account you want to monitor.
2.) Replace WEBHOOK_URL with Discord account webhook url. To know how, just Google: "how to create webhook discord".
3.) Replace DATABASE with any finename you want to use as temporary data for checking new photos.

COLLABORATIONS:

Collaborations to improve this script are always welcome :)