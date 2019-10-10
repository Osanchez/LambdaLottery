import lxml
import requests
from bs4 import BeautifulSoup

"""
Author: Omar Sanchez
Email: OmarSanchezDev@gmail.com
Date: 10/10/19

Note:
This is a lambda function for use with AWS lambda that retrieves the most recent winning lottery numbers and 
jackpot information. Can be incorporated into a variety of AWS services

Disclaimer:
Please make sure to cite this repo and give credit to any authors if you use this resource
"""

games = ["Mass Cash", "Megabucks", "Midday Numbers", "Numbers", "Lucky For Life", "Mega Millions", "Powerball"]


# TODO: Check contents of event and context in order to pass to lambda function properly
def lambda_handler(event, context):
    json_response = {
        'dialogAction': {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                'contentType': "PlainText",
                'content': get_winning_numbers(context)
            }
        }
    }

    return {
        'dialogAction': json_response['dialogAction']
    }


def get_winning_numbers(game_name):
    result_text = ""

    if game_name.title() in games:
        game = game_name.title()
        numbers = scrap_winning_numbers()

        if game == "Mass Cash":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:5]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + "! Jackpot: " + jackpot
        elif game == "Megabucks":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:6]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + "! Jackpot: " + jackpot
        elif game == "Midday Numbers":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:4]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + "! Jackpot: " + jackpot
        elif game == "Numbers":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:4]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + "! Jackpot: " + jackpot
        elif game == "Lucky For Life":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:5]
            lucky_ball = numbers[game]["result"][5:6][0]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + " with lucky ball number " + lucky_ball + "! Jackpot: " + jackpot
        elif game == "Mega Millions":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:5]
            mega_ball = numbers[game]["result"][5:6][0]
            multiplier = numbers[game]["result"][6:7][0]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + " with mega ball number " + mega_ball + " and a multiplier of " + multiplier + "! Jackpot: " + jackpot
        elif game == "Powerball":
            draw_date = numbers[game]["draw_date"]
            winning_numbers = numbers[game]["result"][0:5]
            power_ball = numbers[game]["result"][5:6][0]
            power_play = numbers[game]["result"][6:7][0]
            jackpot = numbers[game]["jackpot_amount"]

            result_text = game + "\nThe Winning Numbers for " + str(draw_date) + " are " + ', '.join(winning_numbers) \
                + " with power ball number " + power_ball + " and a power play of " + power_play + "! Jackpot: " + jackpot
    else:
        result_text = "Please Enter a valid game name from the following list [" + ', '.join(games) + "]"

    return result_text


def scrap_winning_numbers():
    winning_numbers_link = "https://www.lotteryusa.com/massachusetts/"
    sorted_winning_numbers = {}

    resp = requests.get(winning_numbers_link)
    soup = BeautifulSoup(resp.text, "lxml")

    for table_row in soup.findAll('tr'):
        for table_column in table_row.findAll('td'):
            for section in table_column.findAll('div'):
                if section.text in games:
                    # Game Name
                    # print section.text

                    # Winning Numbers
                    unfiltered_winning_numbers = table_row.find("ul", {"class": "draw-result"})
                    winning_numbers = [str(x.text).strip().replace('\n', '').replace(' ', '').replace('LuckyBall', '').replace('MB', '').replace('PB', '').replace('Megaplier:', '').replace('PowerPlay:', '') for x in unfiltered_winning_numbers.findAll('li')]
                    # print winning_numbers

                    # Draw Date
                    result_date = table_row.find("span", {"class": "date"}).text
                    # print result_date

                    # Jackpot
                    jackpot = str(table_row.find("span", {"class": "jackpot-amount"}).text).strip()
                    # print jackpot

                    # add all the values to a dictionary
                    sorted_winning_numbers[section.text] = {"result": winning_numbers, "draw_date": result_date, "jackpot_amount": jackpot}

    return sorted_winning_numbers


if __name__ == "__main__":
    pass
    # print(get_winning_numbers("Mass cash"))
