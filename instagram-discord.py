#!/usr/bin/python

# Copyright (c) 2020 Fernando
# Url: https://github.com/fernandod1/
# License: MIT

# DESCRIPTION:
# This script executes 2 actions:
# 1.) Monitors for new image posted in a instagram account (create a cronjob).
# 2.) If found new image, a bot posts new instagram image in a discord channel.

# REQUIREMENTS:
# - Python v3
# - Python module re, json, requests
import re
import json
import sys
import requests
import urllib.request
import os

# USAGE:
# Replace INSTAGRAM_USERNAME with username account you want to monitor.
# Replace WEBHOOK_URL with Discord account webhook url. To know how, just Google: "how to create webhook discord".
# Replace DATABASE with any finename you want to use as temporary data for script store last imageID posted.

INSTAGRAM_USERNAME = "magdapalimariu" # Example: ladygaga
WEBHOOK_URL = "https://discord.com/api/webhooks/795736319187484693/grIMrthpHsANsP5bRATqncxTs81qqspV7HdWVr545B1PW9VmUONodUujDlGaed_0xcrJ"                # Url to your discord webhook
DATABASE = "database.txt"

# ----------------------- Do not modify under this line ----------------------- #

def write_to_file(content,filename):
    try:
        f = open(filename,"w")
        f.write(content)  
        f.close()
    except IOError:
        print("Error occured trying to read the file "+filename+".")

def read_from_file(filename):
    try:
        f = open(filename,"r")
        content = f.read()
        f.close()
        return content
    except IOError:
        print("Error occured trying to read the file "+filename+".")

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

def webhook(webhook_url,html):
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}    
    embed["color"] = 15467852
    embed["title"] = "New pic of @"+INSTAGRAM_USERNAME+""
    embed["url"] = "https://www.instagram.com/p/"+get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    #embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url":get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discod, code {}.".format(result.status_code))

def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(read_from_file(DATABASE)==get_last_publication_url(html)):
            print("Not new image to post in discord.")
        else:
            write_to_file(get_last_publication_url(html),DATABASE)
            print("New image to post in discord.")
            webhook(WEBHOOK_URL, get_instagram_html(INSTAGRAM_USERNAME))
    except:
        print("An error occured.")


if __name__ == "__main__":

    main()


