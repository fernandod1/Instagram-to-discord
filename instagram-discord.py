#!/usr/bin/python

# Copyright (c) 2020 Fernando
# Url: https://github.com/fernandod1/
# License: MIT

# DESCRIPTION:
# This script executes 2 actions:
# 1.) Monitors for new image posted in a instagram account.
# 2.) If found new image, a bot posts new instagram image in a discord channel.
# 3.) Repeat after set interval.

# REQUIREMENTS:
# - Python v3
# - Python module re, json, requests
import re
import json
import sys
import requests
import urllib.request
import os
import time

# USAGE:
# Environment Variables
# Set IG_USERNAME to username account you want to monitor. Example - ladygaga
# Set WEBHOOK_URL to Discord account webhook url. To know how, just Google: "how to create webhook discord".
# Set TIME_INTERVAL to the time in seconds in between each check for a new post. Example - 1.5, 600 (default=600)

INSTAGRAM_USERNAME = os.environ.get('IG_USERNAME')


# ----------------------- Do not modify under this line ----------------------- #


def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(webhook_url, html):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {"embeds": []}
    embed = {
        "color": 15467852,
        "title": "New pic of @" + INSTAGRAM_USERNAME + "",
        "url": "https://www.instagram.com/p/" + \
               get_last_publication_url(html) + "/", "description": get_description_photo(html),
        "image": {
            "url": get_last_thumb_url(html)}
    }
    # embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 "
                      "Safari/537.11 "
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html):
            print("Not new image to post in discord.")
        else:
            os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html)
            print("New image to post in discord.")
            webhook(os.environ.get("WEBHOOK_URL"),
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if os.environ.get('IG_USERNAME') is not None and os.environ.get('WEBHOOK_URL') is not None:
        while True:
            main()
            time.sleep(float(os.environ.get('TIME_INTERVAL') or 600))
    else:
        print('Please configure environment variables properly!')