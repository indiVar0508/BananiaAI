# Banania

[Banania](https://playminigames.net/game/banania) is puzzle game to solve maze environment popular in 1990s.This project is an attempt to recreate the a approximation of game and use different path finding algorithms and AI algorithms to play level one of the game.


<p align='center'>
    <img src="./Resources/banania_a_star.gif">
</p>

# Setup

If you want to give it a try you can clone the project 

```
      git clone ghttps://github.com/indiVar0508/Banania.git
```

Install the requirements into your Python virtual environment, make sure you are in `BananiaAI` directory

```
    python3 -m venv venv # create virtual environment
    source venv/bin/activate # activate virtual environment in terminal
    pip install -r requirements.txt
```

# How to Play

If you want to run the game once your virtual environment is setup, you can simply run main.py file to intialize the prompt to start the game.

```
    python main.py
```

The prompt will give options to either play yourself or let A* algorithm find path to goal it self