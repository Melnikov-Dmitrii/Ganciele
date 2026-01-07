\# Guess the Character — Discord Game Bot



Multiplayer Discord bot that manages a turn-based guessing game.

Players join a voice channel, secretly assign characters to each other,

and then try to guess them by asking yes/no questions.



\## Game Flow



1\. Players join the same voice channel.

2\. The bot collects participants and randomly assigns the playing order.

3\. Each player receives a private message asking them to choose a character

&nbsp;  for the next player in the circle.

4\. After all characters are submitted, the bot sends each player

&nbsp;  assigned characters of other players via direct messages.

5\. The guessing phase starts and players ask yes/no questions verbally.



\## Features



\- Multiplayer game support

\- Random player order (circle)

\- Private character assignment via DMs

\- Game state management

\- Slash commands interface



\## Tech Stack



\- Python

\- discord.py (async)



\## Bot Commands



\- /start — create a new game session

\- /join — join the current game

\- /leave — leave the current game

\- /list — show list of players in  current game

\- /begin — start character assignment

\- /end — finish the game



\## Installation \& Run



1\. Clone the repository:

&nbsp;  git clone https://github.com/Melnikov-Dmitrii/Ganciele



2\. Install discord.py

&nbsp;  pip install discord.py



3\. Create token.txt file and add your bot token inside



4\. Run the bot:

&nbsp;  python main.py

