<div align="center">
  <img src="logo.png" alt="logo" width="200" height="auto" />
  <h1>Wallapop Scrapper</h1>
  
  <p>
    A selenium based web scrapper that let's you scrape all the data from a given motorcycle model ads to later process the data
  </p>
  
<h4>
    <a href="https://github.com/Ki-re/Wallapop-Scrapper/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Ki-re/Wallapop-Scrapper/issues/">Request Feature</a>
  <span> · </span>
    <a href="https://github.com/Ki-re/Wallapop-Scrapper/pulls">Contribute</a>
  </h4>
</div>

<br />

## Disclaimer

This script was designed in 2022 and is no longer being maintained. Feel free to adapt the code to your needs.

<!-- About the Project -->

## About the Project

The script searches all the ads for a given motorcycle model on wallapop and saves the obtained data to a sql database. That data can later be processed to get metrics on the market prices to determine whether a published bike's price is worth or not.

This script was designed on 2022 and is no longer being mantained, feel free to adapt the code to your needs

<!-- Requirements -->

## Requirements

In order to run this script you will need: 

```bash
 pip install selenium
```

Download the chromedriver version that matches your chrome version: 

```bash
https://chromedriver.chromium.org/downloads
```

<!-- Get Started -->

## Get Started

Clone the project

```bash
  git clone https://github.com/Ki-re/dgt_exam_alert.git
```

Create your telegram bot with BotFather

```bash
  /newbot
```

Get your bot's telegram token and the chat id where you want the result message to be sent

```bash
  telegram_bot_token = ""
  chat_id = ""
```

Set-up the config.py file with your data

```bash
  nif = "00000000A"
  fecha_examen = "00/00/0000"
  fecha_nacimiento = "00/00/0000"
  carnet = ""
  update_time = 300 
  telegram_bot_token = ""
  chat_id = ""
```

Run the script
```
  python3 main.py
```

<!-- License -->

## License

Distributed under the no License. See LICENSE.txt for more information.
