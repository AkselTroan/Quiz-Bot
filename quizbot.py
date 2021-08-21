import discord
import asyncio
from discord.ext import commands
from discord.utils import get
import time
import random
import os
import qt as qt
import importlib

importlib.import_module('qt')


# |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= |
# | This is discord will allow discord members in the server to play a round of quiz.            |
# | The quiz master (Host of the bot) Will make their own questions in the questions.txt file    |
# | The format in this file will be "Question:Answer".                                           |
# | The host master will chose the game settings through the Python app                          |
# |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= |

client = commands.Bot(command_prefix='!')  # Creates the bot with command prefix of '!'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Global Variables =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
gamemode = ['Free for All', 'Team Play']  # currently two gamemodes
current_gamemode = ''
all_members = []  # a List of all current members of the quiz
playing_quiz = False
logs = "This is the log"
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Global Variables =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class Member:

    def __init__(self, name, points):

        self.name = name
        self.points = points
        self.team = ''

    def add_points(self, amount):
        self.points += amount

    def remove_points(self, amount):
        self.points -= amount

    def join_team(self, team):
        self.team = team


@client.command()
async def join(ctx):
    global all_members, gamemode, current_gamemode
    author = str(ctx.author).split("#", 1)

    if gamemode == 'Free for All' and playing_quiz is False:
        current_gamemode = 'Free for All'
        ctx.channel.send("Now playing Free for All")

        if author[0] in all_members:
            ctx.channel.send("You're already registered")

        else:
            member = Member(author[0], 0)
            all_members.append(member)
            ctx.channel.send(f'{author[0]} just joined the quiz')

    elif gamemode == 'Team Play' and playing_quiz is False:
        current_gamemode = 'Team Play'
        ctx.channel.send("Now playing Teamplay")


def main():
    global gamemode, current_gamemode, all_members, playing_quiz, logs
    gamemode = ['Free for All', 'Team Play']  # currently two gamemodes
    current_gamemode = ''
    all_members = []  # a List of all current members of the quiz
    playing_quiz = False
    logs = ["This is the log"]
    while True:
        qt.run()
        new_log = input("Insert new log: ")
        logs.append(new_log)
    # client.run('INSERT YOUR TOKEN HERE') # Secret token!


if __name__ == '__main__':
    main()
