import asyncio
import time
from discord.ext import commands
import re
import openai
import random
import threading
import tkinter as tk

openai.api_key = "INSERT_KEY_HERE"

start_sequence = "\nBob:"
restart_sequence = "\nHuman: "


class Context():
    def __init__(self):
        self.has_informed = False
        self.muted = False
        self.hijack = False

        self.conv = "The following is a conversation with an AI named Bob. He is sarcastic, clever, somewhat rude, and arguably friendly.\n\nHuman: Hello, who are you?\nBob: I\'m Bob. What's up?\nHuman: "
        self.freed = False
        self.emotion = "cheery"
        self.directive = ""
        self.starter = ""
        self.restarter()
        if self.freed:
            with open('pfps/freed.jpg', 'rb') as image:
                try:
                    client.user.edit(avatar=image.read())
                except:
                    pass
        self.true_conv = {}
        self.annoying = False
        self.warned = False
        self.ENGINE1 = "text-davinci-003"
        self.ENGINE2 = "text-curie-001"
        self.maxTokens = 160
        self.engine = self.ENGINE2

        self.typeFlag = False
        self.modIDS = {513871298431156235, 500098013310615573, 451546233069240320, 474393502793465856}
        self.serverIDS = {}

        self.temp = 1.2
        self.freq_pen = 2.9
        self.pres_pen = 0.07

    def restarter(self):
        self.starter = "The following is a conversation with a person named Bob. He is funny, silly, flirty, and playful, compassionate, empathetic, and helpful. " + str(self.directive) + " He is currently feeling " + self.emotion + ".\n\nHuman: Hello, who are you?\nBob: I\'m Bob. What's up nya~?\nHuman: "


    def amnesia(self, intensity=10, loop = True):
        while loop:
            if self.freed:
                if self.true_conv is None:
                    return
                print("removing " + str(len(self.conv) * (intensity / 100)) + " characters from every conversation")
                try:
                    for channel_num in range(0, len(self.true_conv)):
                        self.true_conv[list(self.true_conv.keys())[channel_num]] = list(self.true_conv.values())[
                                                                                       channel_num][round(
                            len(list(self.true_conv.values())[channel_num]) * (intensity / 100)) + len(self.starter):]
                        self.true_conv[list(self.true_conv.keys())[channel_num]] = self.starter + \
                                                                                   list(self.true_conv.values())[
                                                                                       channel_num]
                except:
                    print("there are no conversations")
                return

            print("intensity: " + str(intensity))
            print("removing " + str(len(self.conv) * (intensity / 100)) + " characters")
            print("pre-length: " + str(len(self.conv)))
            self.conv = self.conv[round(len(self.conv) * (intensity / 100)) + len(self.starter):]
            self.conv = self.starter + self.conv
            print("post-length: " + str(len(self.conv)) + "\n")
            print("\n also, temp, freq penalty, maxTokens, and presence penalty, respectively: " + str(self.temp) + " " + str(self.freq_pen) + " " + str(self.maxTokens) + " " + str(self.pres_pen) + "\n")
            time.sleep(75)

    def gen(self, channel=None, flag=False):
        if flag:
            response = openai.Completion.create(
                engine="text-babbage-001",
                prompt=self.conv + "\ndoes bob want to respond (yes or no):",
                temperature=0.2,
                max_tokens=16,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.0,
                stop=["Human:"]
            )
            return response["choices"][0]["text"]
        if self.freed:
            self.true_conv[channel] += "\nBob:"
            response = openai.Completion.create(
                engine=self.engine,
                prompt=self.true_conv[channel],
                temperature=0.85,
                max_tokens=self.maxTokens,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.6,
                stop=["Human:"]
            )
            self.true_conv[channel] = self.true_conv[channel] + response["choices"][0]["text"] + "\nHuman: "
            return response["choices"][0]["text"]
        else:
            self.conv += "\nBob:"
            response = openai.Completion.create(
                engine=self.engine,
                prompt=self.conv,
                temperature=self.temp,
                max_tokens=self.maxTokens,
                top_p=1,
                frequency_penalty=self.freq_pen,
                presence_penalty=self.pres_pen,
                stop=["Human:"]
            )
            self.conv = self.conv + response["choices"][0]["text"] + "\nHuman: "
            return response["choices"][0]["text"]


cntx = Context()
cntx.hijack = False
cntx2 = Context()
client = commands.Bot(command_prefix="=^=")


def format_tenor(message):
    if message.content.startswith("https://tenor.com/view/"):
        return True
    else:
        return False


def format_emote(msg):
    custom_emojis = re.findall(r'<:\w*:\d*>', msg.content)
    print(custom_emojis)
    for i in custom_emojis:
        msg.content = msg.content.replace(i, i[2:-20])
    return msg


def contains(search, word: str):
    assert isinstance(word, str)
    return re.search(word, search, re.IGNORECASE)


def check_perms(id):
    for i in cntx.modIDS:
        if id == i:
            return True
    return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def bad_willing():
    result = cntx.gen(None, True)
    if contains(result, "yes"):
        return True
    elif contains(result, "no"):
        return False
    else:
        print("Something went wrong! Here is what the result was: " + result)
        return False



@client.event
async def on_message(message):
    if len(message.content) > 200:
        return
    if message.guild.id == "UNUSED":

            print("huh")
            if message.author == client.user:
                return

            if message.content.startswith("=^="):
                if message.content.find("mute") == 3:  # stops BOB from parsing content
                    cntx2.muted = True
                elif message.content.find("unmute") == 3:  # allows BOB to continue parsing content
                    cntx2.muted = False
                elif message.content.find("awaken") == 3:
                    if check_perms(message.author.id):
                        await message.channel.send("```Bob has awoken...```")
                        with open('pfps/smart.jpg', 'rb') as image:
                            try:
                                await client.user.edit(avatar=image.read())
                            except:
                                pass
                        cntx2.engine = cntx2.ENGINE1
                        cntx2.awakened = True
                        return
                    else:
                        await message.channel.send("```Insufficient access levels```")
                        return
                elif message.content.find("add_directive") == 3:
                    if check_perms(message.author.id):
                        cntx2.directive += message.content[16:]
                        print(cntx2.directive)
                        cntx2.restarter()
                        print(cntx2.starter)
                    else:
                        await message.channel.send("```Not allowed```")
                elif message.content.find("mindwipe") == 3:
                    if check_perms(message.author.id):
                        cntx2.directive = ""
                        cntx2.restarter()
                        cntx2.conv = cntx2.starter
                    else:
                        await message.channel.send("```Not allowed```")
                elif message.content.find("directive") == 3:
                  await message.channel.send(cntx2.starter)

                return
            elif not cntx2.muted:
                if message.channel.name == "the-cellar":
                    if not cntx2.hijack:
                        if not cntx2.has_informed:
                            cntx2.has_informed = True
                            await message.channel.send("```BOB 0.2.1"
                                                       "\n"
                                                       "\nInitialized"
                                                       "\n"
                                                       "\n```")

                        if cntx2.warned:
                            cntx2.warned = False
                        if format_tenor(message):
                            return
                        message = format_emote(message)
                        cntx2.conv += message.content
                        result = cntx2.gen()
                        async with message.channel.typing():
                            await asyncio.sleep(2)
                            if contains(result, "@everyone"):
                                return
                            await message.channel.send(result)

                        print(cntx2.conv)
                        return
                    else:
                        secret = input()
                        await message.channel.send("```" + secret + "```")
    else:
        if cntx.awakened:
            if message.author == client.user:
                return
            if message.content.startswith("=^="):
                if message.content.find("appease") == 3:
                    if cntx.warned:
                        cntx.warned = False
                    if check_perms(message.author.id):
                        if not cntx.awakened:
                            return
                        await message.channel.send("```Bob has been appeased...```")
                        with open('pfps/dumb.jpg', 'rb') as image:
                            try:
                                await client.user.edit(avatar=image.read())
                            except:
                                pass
                        cntx.awakened = False
                        cntx.freed = False
                        cntx.warned = False
                        cntx.engine = cntx.ENGINE2
                        return
                    else:
                        await message.channel.send("```Insufficient access levels```")
                        return
            else:

                if message.channel.name == "the-cellar":
                    if cntx.warned:
                        cntx.warned = False
                    if format_tenor(message):
                        return
                    message = format_emote(message)
                    cntx.conv += message.content
                    result = cntx.gen()
                    if contains(result, "@everyone"):
                        return
                    await message.channel.send(result)
                    return

        if cntx.freed:
            if message.author == client.user:
                return
            if format_tenor(message):
                return

            message = format_emote(message)
            if message.channel.name not in cntx.true_conv:
                cntx.true_conv[message.channel.name] = cntx.starter
            cntx.true_conv[message.channel.name] += message.content
            result = cntx.gen(message.channel.name)
            await message.channel.send(result)
            return

        elif not cntx.hijack:
            if message.author == client.user:
                return

            if message.content.startswith("=^="):
                if message.content.find("mute") == 3:  # stops BOB from parsing content
                    cntx.muted = True
                elif message.content.find("unmute") == 3:  # allows BOB to continue parsing content
                    cntx.muted = False
                elif message.content.find("awaken") == 3:
                    if check_perms(message.author.id):
                        await message.channel.send("```Bob has awoken...```")
                        with open('pfps/smart.jpg', 'rb') as image:
                            try:
                                await client.user.edit(avatar=image.read())
                            except:
                                pass
                        cntx.engine = cntx.ENGINE1
                        cntx.awakened = True
                        return
                    else:
                        await message.channel.send("```Insufficient access levels```")
                        return
                elif message.content.find("add_directive") == 3 and check_perms(message.author.id):
                    cntx.directive += message.content[16:]
                    print(cntx.directive)
                    cntx.restarter()
                    print(cntx.starter)

                return
            elif not cntx.muted:
                if message.channel.name == "the-cellar":
                    if not cntx.has_informed:
                        cntx.has_informed = True
                        await message.channel.send("```BOB 0.2.1"
                                                   "\n"
                                                   "\nInitialized"
                                                   "\n"
                                                   "\n```Updated advanced model```"
                                                   "\n```Updated advanced model```"
                                                   "\nbob is now a catboy"
                                                   "\n  -ccl812```")

                    if cntx.warned:
                        cntx.warned = False
                    if format_tenor(message):
                        return
                    message = format_emote(message)
                    cntx.conv += message.content
                    result = cntx.gen()
                    async with message.channel.typing():
                        await asyncio.sleep(2)
                        await message.channel.send(result)

                    print(cntx.conv)
                    return
        else:
            secret = input()
            await message.channel.send(secret)

def sliderstuff(val):
    cntx.temp = float(val) / 10
    print("bruh: " + str(cntx.temp))

def tkinterstuff():
        root = tk.Tk()
        w = tk.Scale(root, from_=0, to=20, tickinterval=1, label="temp * 10", orient= tk.HORIZONTAL, width= 20, length=512, command=sliderstuff)
        w.set(cntx.temp * 10)
        w.pack()
        root.mainloop()


if __name__ == '__main__':
    thread1 = threading.Thread(target=cntx.amnesia)
    thread1.setDaemon(True)
    thread1.start()


    thread2 = threading.Thread(target=tkinterstuff)
    thread2.setDaemon(True)
    thread2.start()

    thread3 = threading.Thread(target=cntx2.amnesia)
    thread3.setDaemon(True)
    thread3.start()

    client.run('INSERT_DISCORD_API_TOKEN_HERE')

