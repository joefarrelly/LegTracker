# LegTracker for WoW

## Overview

LegTracker uses the WoW API to show the characters in a given guild who are able to craft legendary items in the Shadowlands expansion, along with the rank of each equipment slot they are able to craft. Backend is coded entirely in Python. Frontend is done using a google sheet.

Requires Python 3, created using version 3.8.6.

## Blizzard API Setup
First step is to get a **Client ID** and **Client Secret** in order to access to Blizzard API. Instructions on how to do that can be found [here](https://develop.battle.net/documentation/guides/getting-started). Make a note of the **Client ID** and **Client Secret**, they will be needed in the Backend Setup.

## Google API Setup

In order to use Google Sheets to display the data you need to go to the [Google console](https://console.developers.google.com) and create a new project as follows:
* Create a new project:
    * Click the dropdown in the top left next to the Google APIs logo.
    * Click **"New Project"** in the top right of the Select a project box.
    * Enter the project name and organization (optional), and click the **"Create"** button.
    * Make sure the dropdown in the top left next to the Google APIs logo now shows the name of the project you just created.
* Click **"Enable APIs and Services"** at the top of the screen.
* Find the **"Google Sheets API"**, click it, then click the **"Enable"** button.
* Click the **"Create Credentials"** button in the top right of the overview page.
* Fill in the **"Find out what kind of credentials you need"** form as follows:
    * Which API are you using? - **Google Sheets API**.
    * Where will you be calling the API from? - **Other UI (e.g. Windows, CLI tool)** 
    * What data will you be accessing? - **Application data**.
* Click the **"What credentials do I need?"** button.
* Fill in the **"Create a service account"** form as follows:
    * Service account name - **{ANY NAME}**.
    * Role - **Project > Editor**.
    * Service account ID - **{GENERATED AUTOMATICALLY}**
    * Key type - **JSON**
* Make a note of the **"Service account ID"**, it will be needed in the Google Sheet Setup.
* Click the **"Continue"** button.
* Downlaod the generated JSON file, it will be needed in the Backend Setup.

Additonally we need to enable the Google Drive API as well:
* Click **"Enable APIs and Services"** at the top of the screen.
* Find the **"Google Drive API"**, click it, then click the **"Enable"** button.

## Google Sheet Setup

* Go to [Google Sheets](https://docs.google.com/spreadsheets) and under **"Start a new spreadsheet"** click the **"Blank"** template.
* Name the sheet whatever you like.
* Click the **"Share"** button in the top right of the page.
* Enter the **"Service account ID"** generated in the Google API Setup and hit Enter on the keyboard.
* Uncheck the **"Notify people"** checkbox and click the **"Send"** button in the bottom right of the window.
* Make a note of the **"Spreadsheet ID"**, it will be needed in the Backend Setup.
* The **"Spreadsheet ID"** can be extracted from the URL of the sheet, it is the value located between `/d/` and `/edit`.

## Backend Setup
* Clone the repo:
```bash
git clone https://github.com/joefarrelly/LegTracker.git 
```
* Update repo:
    * Move and rename the JSON downloaded in the Google API Setup to `~/LegTracker/client_secret.json`.
    * Using `.env.sample` as a template, create `.env` in `~/LegTracker/.env`, where the values are:
        * BLIZZ_CLIENT: Your Client ID from the Blizzard API Setup.
        * BLIZZ_SECRET: Your Client Secret from the Blizzard API Setup.
        * SPREADSHEET_KEY: The Spreadsheet ID from the Google Sheet Setup.
        * REALM: The realm slug that the guild is located on.
        * GUILD: The name slug of the guild.
        * RANKS: Not needed at this point, functionality not yet implemented.
* Install the packages needed:
```bash
pip install -r legtracker\requirements.txt
```

## Running the Tool

```bash
legtracker\core.py
```