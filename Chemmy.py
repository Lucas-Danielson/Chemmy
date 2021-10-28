#bot.py
import os

import discord
from dotenv import load_dotenv

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


#google sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("calApi").sheet1


load_dotenv()
TOKEN = 'Secret :)'
SERVER = 'AP Chemistry'

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

    commandList = "Commands: \n!homework - Displays today's homework\nMore coming soon! "

    #!commands
    if message.content == '!commands':
        response = commandList
        await message.channel.send(response)

    #!homework
    if message.content == '!homework':
        

        data = sheet.get_all_records()

        now = datetime.datetime.now()

        formattedDate = now.strftime("%m") + "/" + now.strftime("%d")

        col = sheet.col_values(1)

        ind = col.index(formattedDate) + 1
        hw = sheet.cell(ind, 2).value
        if hw == 'None':
            response = "Woohoo! No Homework"
        else:
            response = "Today's homework is " + hw
        
        await message.channel.send(response)
    
    


client.run(TOKEN)