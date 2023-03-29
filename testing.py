from nba_api.live.nba.endpoints import scoreboard
import requests
from datetime import datetime
import pytz






# Today's Score Board
games = scoreboard.ScoreBoard()

# json
games.get_json()

UTC = pytz.utc

indTime = pytz.timezone('Asia/Kolkata')
date = datetime.now(indTime)


data = games.get_dict()
# all_games = data['scoreboard']['games']
mainMessage = f"<b>🏀 {date.strftime('%d-%m-%Y')}</b>\n\n"
for i in range(len(data['scoreboard']['games'])):

    
    
    all_games = data['scoreboard']['games'][i]
    home_team = all_games['homeTeam']
    away_team=all_games['awayTeam']

    if home_team['score'] > away_team['score']:

        mainMessage += f"<b>{home_team['teamName']}</b> - {home_team['score']} : ({home_team['wins']} - {home_team['losses']}) 🏆"
        mainMessage += "\n"
        
    

        away_team = all_games['awayTeam']
        mainMessage += f"<b>{away_team['teamName']}</b> - {away_team['score']} : ({away_team['wins']} - {away_team['losses']})\n\n"
        mainMessage+=f"⛹️‍♂️ {all_games['gameLeaders']['homeLeaders']['name']} - {all_games['gameLeaders']['homeLeaders']['points']}/{all_games['gameLeaders']['homeLeaders']['rebounds']}/{all_games['gameLeaders']['homeLeaders']['assists']}\n\n"
        mainMessage += "\n\n\n"
    else:
        mainMessage += f"<b>{home_team['teamName']}</b> - {home_team['score']} : ({home_team['wins']} - {home_team['losses']}) "
        mainMessage += "\n"

        away_team = all_games['awayTeam']
        mainMessage += f"<b>{away_team['teamName']}</b> - {away_team['score']} : ({away_team['wins']} - {away_team['losses']}) 🏆"
        mainMessage += "\n\n"
        mainMessage+=f"⛹️‍♂️ {all_games['gameLeaders']['awayLeaders']['name']} - {all_games['gameLeaders']['awayLeaders']['points']}/{all_games['gameLeaders']['awayLeaders']['rebounds']}/{all_games['gameLeaders']['awayLeaders']['assists']}\n"
        mainMessage += "\n\n\n"

url = "https://api.telegram.org/bot6176942284%3AAAFr5ouK0fy9sqJLjPgrqCRJrNUEa0M_uyQ/sendMessage"

payload = {
    "text": mainMessage,
    "parse_mode": "html",
    "disable_web_page_preview": False,
    "disable_notification": False,
    "reply_to_message_id": None,
    "chat_id": "-977129241"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)


# print(data['scoreboard']['games'][0])
