import openai
import speech_recognition as sr
from gtts import gTTS
import io
import webrtcvad

from discord.ext import commands
from config import Config
import discord

openai.api_key = "YOUR_OPENAI_API_KEY"
PREFIX = Config.prefix
TOKEN = Config.bot_token

class TTSBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_context = []  # Initialize audio context for conversation history

    def transcribe_speech(self, audio_data):
        # Function to convert speech to text
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service; {e}"

    def generate_gpt_response(self, prompt, context=[]):
        # Function to generate GPT-3.5 chat responses
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            context=context
        )
        return response.choices[0].text.strip()

    def text_to_speech(self, text):
        # Function to convert text to speech using gTTS
        tts = gTTS(text=text, lang='en')
        tts_bytes = io.BytesIO()
        tts.write_to_fp(tts_bytes)
        tts_bytes.seek(0)
        return tts_bytes

    async def listen_and_respond(self, voice_channel, text_channel):
        # Function to continuously listen for user input and generate responses
        vad = webrtcvad.Vad(3)  # Create a VAD with aggressiveness level (1 to 3, higher means more sensitive to speech)
        await text_channel.send("Bot is now listening. Speak in the voice channel.")

        while voice_channel.is_connected():
            try:
                audio_data = await voice_channel.listen()  # Start listening to the voice channel
                if vad.is_speech(audio_data.frame_data, audio_data.sample_rate):
                    user_input = self.transcribe_speech(audio_data)  # Call instance method using self
                    print("User Input (Speech): ", user_input)

                    self.audio_context.append(user_input)  # Append user input to the audio context

                    prompt = "\n".join(self.audio_context)  # Generate GPT-3.5 response based on the audio context
                    gpt_response = self.generate_gpt_response(prompt, context=self.audio_context)  # Call instance method using self
                    print("GPT-3.5 (Chat): ", gpt_response)

                    tts_bytes = self.text_to_speech(gpt_response)  # Convert GPT-3.5 chat response to speech

                    # Play the GPT-3.5 chat response in the voice channel
                    voice_channel.play(discord.FFmpegPCMAudio(tts_bytes))

                    while voice_channel.is_playing():  # Wait until the audio is done playing
                        await asyncio.sleep(1)
            except Exception as e:
                print("Error: ", e)
                break

        await text_channel.send("Bot is now disconnected from the voice channel.")
        self.audio_context.clear()  # Clear the audio context when disconnected
        await voice_channel.disconnect()  # Disconnect the bot from the voice channel

    @commands.command()
    async def listen(self, ctx):
        # Command to listen to the voice channel and start the conversation
        if ctx.author.voice:
            try:
                voice_channel = await ctx.author.voice.channel.connect()
                print("Bot is connected to voice channel:", voice_channel.channel.name)
                self.bot.loop.create_task(self.listen_and_respond(voice_channel, ctx.channel))  # Use self.bot to access the bot instance
                await ctx.channel.send("Bot is now connected and listening.")
            except Exception as e:
                print("Error: ", e)
                await ctx.channel.send("Error occurred while connecting to the voice channel.")
        else:
            await ctx.channel.send("You aren't connected to a voice channel.")

    @commands.command()
    async def disconnect(self, ctx):
        # Command to disconnect from the voice channel
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.channel.send("Bot is now disconnected from the voice channel.")
        else:
            await ctx.channel.send("Bot is not connected to a voice channel.")