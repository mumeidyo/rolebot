from bot import run_bot
from app import app

if __name__ == "__main__":
    #run_bot() #This line is commented out because the original intention is to separate the bot and web app. Running both simultaneously would require more sophisticated coordination.
    app.run(host="0.0.0.0", port=5000, debug=True)