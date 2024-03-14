import asyncio

import discord

import discord

from discord.ext import commands

import pyttsx3

# ~~~~~ Cog ~~~~~
# create a discord bot that reads new messages from a voice channel's text channel
# IFF the bot is in that voice channel, then, repeat the message using TTS over the voice channel
class Parrot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = pyttsx3.init()
        self.voice_client = None
        print('Parrot cog loaded successfully')

    @commands.command(name="speak")
    async def speak(self, ctx):
        await ctx.send('I am a parrot')

    @commands.command(name="parrot")
    async def parrot(self, ctx: commands.Context):
        print(f'parrot command called by {ctx.author.name}')
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")

    # command to boot the parrot from the voice channel
    @commands.command(name="boot")
    async def boot(self, ctx):
        print(f'booting parrot {ctx.author.name}')
        # Check if the bot is in a voice channel
        if self.bot.voice_clients is None:
            return

        # Boot the bot from the voice channel
        await self.bot.voice_clients[0].disconnect()

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        
        # ignore if bot is not in a voice channel
        if message.content[0] == '!' or len(self.bot.voice_clients) == 0:
            return

        # Check if the message is from the text channel linked to the voice channel
        voice_channel = self.bot.voice_clients[0].channel
        if message.channel.name == voice_channel.name:
           
            # Repeat the message using TTS over the voice channel
            if message.author != self.bot.user:
                # voice_client = self.bot.voice_clients[0]
                # Use pyttsx3 to convert text to speech
                tts_message = message.content
                self.engine.save_to_file(tts_message, 'tts_message.wav')
                self.engine.runAndWait()

                # Check if the bot is connected to a voice channel
                # Play the TTS message over the voice channel
                if self.voice_client is not None and self.voice_client.play is not None:
                    await self.voice_client.play(discord.FFmpegPCMAudio('tts_message.wav'))

# ~~~~~ Setup ~~~~~
def setup(bot):
    bot.add_cog(Parrot(bot))