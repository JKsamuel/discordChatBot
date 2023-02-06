"""
Jongeun Kim, 000826393, Mohawk College, 19/Oct/2022

"""
import random
from tokenize import String
import discord
from faq_bot_plus_ML import *
from faq_support_method import *

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        intents.messages = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as', self.user)
        
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
                
        # if user type 'ping' then it return the result the speed of network connectivity        
        if message.content.startswith('ping'):
            await message.channel.send(f'pong! {round(round(self.latency, 4)*1000)} ms')
        # if user type 'roll' then it return random number between 1 to 6
        elif message.content.startswith('roll'):
            await message.channel.send(f'{random.randint(1, 6)} came out')

        # get the utterance and generate the response
        utterance = message.content 
        print(utterance)
        intent = understand(utterance)  
        
        """
        step1 using regular expression to matching
        step2 if it fails to matching then using spacy
        """
        if intent == None or intent == -1:
            intent = matcherMedia(utterance)    # using spacy module
            # index number 23 indicates farewell pattern in matcherMedia() function
            if intent == 23:
                await self.change_presence(status=discord.Status.offline)
                await message.channel.send("bye bye")
                response = generate(intent)
                await message.channel.send(response)
            # index number 21 indicates welcome pattern(greeting) pattern in matcherMedia() function
            elif intent == 21:
                await self.change_presence(status=discord.Status.online)
                response = generate(intent)
                await message.channel.send(response)
            # Return None or -1 value will return flexiable answer expression.
            elif intent == None or intent == -1:
                answer = chat(utterance)
                if answer == -1:
                    await message.channel.send(generate(answer))
                else:
                    await message.channel.send(answer)
        else:    
            response = generate(intent)
            # send the response
            await message.channel.send(response)
        print(utterance)

client = MyClient()

with open("bot_token.txt") as file:
    token = file.read()

client.run(token)