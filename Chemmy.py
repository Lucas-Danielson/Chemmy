# bot.py
import os
import subprocess

import discord
from discord import Member
from discord.ext.commands import Bot, has_permissions, MissingPermissions

from dotenv import load_dotenv

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

def actionLog(action):
    time = str(datetime.datetime.now())
    print(time + ": " + action)

def errorLog(error):
    time = str(datetime.datetime.now())
    print(time + ": " + error)

#google sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("calApi").sheet1


load_dotenv()
TOKEN = '----------'
SERVER = 'AP Chemistry'

bot = Bot("!")
client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )



#Commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'chemmy' or 'Chemmy' in message.content:
        emoji = '❤️'
        await message.add_reaction(emoji)
        

    commandList = "Commands: \n!homework - Displays today's homework\n!homework [mm/dd] - Displays homework on a specific day "

    #!commands
    if message.content == '!commands':
        response = commandList
        actionLog("command list command")
        await message.channel.send(response)

    #!homework
    if message.content.startswith('!homework'):
        try:
            msg = message.content.split(" ")
            date = msg[1]
            col = sheet.col_values(1)
            try:
                ind = col.index(date) + 1
                hw = sheet.cell(ind, 2).value
                pass
            except ValueError:
                response = "That date does not exist in the calender! Make sure the date is formatted as mm/dd."
            try:
                if hw == 'None':
                    response = "There is no homework on " + date + "!"   
                elif hw == 'Test':
                    response = "On " + date + " there was a test"    
                else:
                    response = "The homework on " + date + " is " + hw
            except UnboundLocalError:  
                pass
            except Exception as e:
                errorLog(e)
                pass
            actionLog("homework command")
            await message.channel.send(response)
        except IndexError:      
            data = sheet.get_all_records()
            now = datetime.datetime.now()
            day = now.strftime("%a")
            formattedDate = now.strftime("%m") + "/" + now.strftime("%d")
            col = sheet.col_values(1)
            try:
                ind = col.index(formattedDate) + 1
                hw = sheet.cell(ind, 2).value
                pass
            except ValueError:
                response = "There is no data for today's date! This can happen if there is no school today or if the data has not been updated with the new calender. \n Try !homework [mm/dd] to see the homework on a specific date!"
            try:
                if hw == 'None':
                    response = "Woohoo! No Homework"    
                elif hw == 'Test':
                    response = "There was a test today, no homework!"   
                else:
                    response = "Today's homework is " + hw
            except UnboundLocalError:  
                pass
            except Exception as e:
                errorLog(e)
                pass
            actionLog("homework command")
            await message.channel.send(response)

client.run(TOKEN)
