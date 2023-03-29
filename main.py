from nba_api.live.nba.endpoints import scoreboard
import requests
from datetime import datetime
import pytz
from fastapi import FastAPI
from firebase_admin import *
import json

#Firebase initialization
cred = credentials.Certificate({
  #Credentials here
})
#firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
    'databaseURL': "Enter URL"
})

def createreference(gamecode,time):
    main_ref = db.reference('/')
    req_data = main_ref.get('nba')[0]['nba']
    print(req_data)
    if gamecode in req_data.keys():
        return False
    else:
        ref = db.reference('nba').child(gamecode)
        ref.set(time)
        return True

# print(createreference('20230328_BOSGSW','29-03-2023 11:40:42'))

app = FastAPI()


@app.get("/nba")
async def nba():
    games = scoreboard.ScoreBoard()
    games.get_json()

    UTC = pytz.utc

    indTime = pytz.timezone('Asia/Kolkata')
    date = datetime.now(indTime)


    data = games.get_dict()
    mainMessage = f"<b>🏀 {date.strftime('%d-%m-%Y')}</b>\n\n"
    try:
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
    except:
        mainMessage ="No games today 😞"


    url = "Telegram API"

    payload = {
        "text": mainMessage,
        "parse_mode": "html",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": ""
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return {"message": response.text}

@app.get("/nbalive")
async def nbalive():
    games = scoreboard.ScoreBoard()
    games.get_json()

    UTC = pytz.utc

    indTime = pytz.timezone('Asia/Kolkata')
    date = datetime.now(indTime)
    data = games.get_dict()
    mainMessage = f"<b>🏀 {date.strftime('%d-%m-%Y')} Live Update!</b>\n\n"

    for i in range(len(data['scoreboard']['games'])):
        all_games = data['scoreboard']['games'][i]
        
        if all_games['gameStatusText']=="Final":
            gamecode=all_games['gameCode'].replace('/','_')
            time=date.strftime('%d-%m-%Y %T')

            if createreference(gamecode,time):
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
                
                url = "API here"
                payload = {
                    "text": mainMessage,
                    "parse_mode": "html",
                    "disable_web_page_preview": False,
                    "disable_notification": False,
                    "reply_to_message_id": None,
                    "chat_id": "-"
                }
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers)
                return {"message": response.text}
            
            else:
                continue

    return {"message": "No Live Matches Now"}