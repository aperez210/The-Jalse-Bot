import os
import sys
import random
import time
import discord
import pip
import ffmpeg
import yt2mp3
pip.main(["install", "discord.py[voice]","-q", "-U", "--upgrade"])

def read_key_file():
    try:
        with open("key.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None

TOKEN = read_key_file()

SECONDS_PER_TICK = 1
TICKRATE = 1/SECONDS_PER_TICK
JOE_BIDEN = "<:jb:1217390315523145810>"
ALEX = "<@231878943412584448>"
ME = "The Jalse Bot"
jalsebot = 0

intent = discord.flags.Intents.all()
client = discord.Client(intents=intent)
@client.event
async def on_ready():
    me = client.user
    jalsebot = me.id
    print(f'{me} has connected to Discord!')
    if 3 == len(sys.argv) and sys.argv[1].isdigit and sys.argv[2].isdigit:
        g = client.guilds[int(sys.argv[1])]
        channel = g.channels[int(sys.argv[2])]
    else:
        g = await select_from_list(client.guilds)
        print(f'{me} is in {g}')
        await save_emoji_list(g)
        channel = await select_from_list(g.channels)
    match type(channel):
        case discord.channel.TextChannel:
            await start_loop(channel)
        case discord.channel.VoiceChannel:
            #channel = discord.channel.VoiceChannel(channel)
            voice = await channel.connect()
            await voice_commands(channel,voice)
                
async def song_list(channel):
    current_directory = os.getcwd()
    song_directory = os.path.join(current_directory, "audio")
    out = []
    for file in os.listdir(song_directory):
        out.append(file.rsplit(".")[0])
    chunks = await break_string_into_chunks("\n".join(out))
    for chunk in chunks:
        await channel.send(chunk)
    return JOE_BIDEN

async def get_song_str(filename:str):
    current_directory = os.getcwd()
    pictures_directory = os.path.join(current_directory, "audio")
    for file in os.listdir(pictures_directory):
        file_name = file.rsplit(".")[0]
        if file_name.lower() == filename.lower():
            return os.path.join("audio",file)
        
    return os.path.join("pictures","error.png")

            
async def voice_commands(channel:discord.channel.VoiceChannel,voice):
    stopped = False
    try: 
        while not stopped:
            try:
                async for message in channel.history(limit=1):
                    out = message.content
                    user = message.author
                    output = ""
                    try:
                        attatchment = message.attachments[0]
                    except:
                        attatchment = None
                    tokens = await interpret(out)
                    if tokens:
                        match tokens[0]:
                            case "play":
                                song = ""
                                if tokens[1].startswith("https"):
                                    song = await yt2mp3.download_youtube_video_as_mp3(tokens[1])
                                elif tokens[1]:
                                    song = await get_song_str(" ".join(tokens[1:len(tokens)]))
                                else:
                                    song = "never gonna give you up" 
                                
                                playable = discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=song)
                                output = f"playing {song.split("\\")[1].split(".")[0]}"
                                voice.play(playable)
                            case "stop":
                                if voice.is_playing():
                                    output = "stopping"
                                    voice.stop()
                            case "list":
                                output = await song_list(channel)
                        await channel.send(content=output)
                                
     
            except Exception as error:
                message = "error"
                print(error)
    except:
        print("stopped")
async def interpret(s:str):
    if s[0] == "|":
        x = s[1:len(s)].split(" ")
        print(x)
        return x 
    else:
        return None
async def get_emoji_list(server:discord.guild.Guild):
    l = ""
    c = 0
    odd = False
    for emoji in server.emojis:
        l = f"{l}\n{emoji.name},{emoji.id}"
        c+=1
    return f"{c}{l}"

async def save_emoji_list(server:discord.guild.Guild):
    id = server.id
    file_name = f"{id}.txt"
    file_name = os.path.join("guildemojis",file_name)
    content = await get_emoji_list(server)
    try:
        with open(file_name, "r") as file:
            existing_content = file.read()
        if existing_content != content:
            with open(file_name, "w") as file:
                file.write(content)
                print("Content updated in", file_name)
        else:
            print("Content unchanged in", file_name)
    except FileNotFoundError:
        with open(file_name, "w") as file:
            file.write(content)
            print("File", file_name, "created with content")

async def select_from_list(list):
    c = 0
    for entry in list:
        try:
            print(f"{c},{entry.name},{entry.id}")
        except:
            print(f"{c},{entry}")
        c+=1
    valid = False
    while not valid:
        n = input("select a number ")
        print("\r",end="")
        if n.isdigit():
            n = int(n)
            if 0<=n<=c-1:
                return list[n]
        print("\r",end="")
 
async def start_loop(channel:discord.channel.TextChannel):
    stopped = False
    out = ""
    attatchment = ""
    user = ""
    await channel.send(f"{ME} is listening")
    try: 
        while not stopped:
            try:
                async for message in channel.history(limit=1):
                    out = message.content
                    user = message.author
                    try:
                        attatchment = message.attachments[0]
                    except:
                        attatchment = None
            except Exception as error:
                message = "error"
                print(error)
            stopped = await int_and_respond(channel,out,attatchment,user)
            time.sleep(SECONDS_PER_TICK)
    except Exception as e:
        print("Stopped!")
        await channel.send(f"{ME} has stopped listening")
        quit()

async def int_and_respond(channel:discord.channel.TextChannel,message,attatch,user):
    guild = channel.last_message.guild
    output = ""
    pic_out = None
    join_meme = False
    if message:
        if message[0] == "|":
            message = message[1:len(message)]
            tokens = message.split(" ")
            match tokens[0].lower():
                case "join":
                    if join_meme:
                        output = "THIS DOESN'T DO ANY THING YET"
                        join_meme = True
                    else:
                        output = "stop it."
                    
                case "source":
                    output = await send_text("source")
                case "help":
                    output = await send_text("help")
                case "scrub":
                    if len(tokens) >= 2:
                        if tokens[1].isdigit():
                            output = await scrub_messages(channel,int(tokens[1]))
                        else:
                            output = await scrub_messages(channel,50)
                case "emoji":
                    if tokens[1].isdigit():
                        output = await random_emoji_list(guild,int(tokens[1]))
                    else:
                        output = await random_emoji(guild)
                case "joe":
                    output = "".join([JOE_BIDEN]*10)      
                case "stop":
                    print("\nStopping...")
                    return True
                case "say":
                    print("\nSending message...")
                    output = " ".join(tokens[1:])
                case "roll":
                       output = await ROLL(tokens)
                case "pic":
                    try:
                        if tokens[1] == "add" and attatch:
                            filename = str(attatch.filename)
                            ext = filename.rsplit(".")[1]
                            try:
                                name = (" ".join(tokens[2:])) +"."+ ext
                            except:
                                name = filename
                            await attatch.save(os.path.join("pictures",name))
                    except:
                        output = "uh oh"
                    pic_name = await picture(tokens)
                    if not attatch:
                        pic_out = pic_name[0]
                        output = pic_name[1]
                    else:
                        output = "picture get"
                    print(f"\nSending the picture {output}")
                case "piclist":
                    output = await picture_list(channel)
            if output != "":
                if pic_out:
                    await channel.send(output, file=pic_out)
                else: 
                    await channel.send(output)
    return False
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

async def scrub_messages(channel:discord.channel.TextChannel,range:int):
    c = 0
    target = client.user.id
    async for message in channel.history(limit=range):
        compare = message.author.id == target
        if compare:
            await message.delete()
            c+=1
    return f"deleted {c} messages"
        
async def random_emoji_list(server:discord.guild.Guild,n:int):
    out = ""
    for i in range(n):
        out += await random_emoji(server)
    return out
    
async def random_emoji(server:discord.guild.Guild):
    current_directory = os.getcwd()
    guildemojis_directory = os.path.join(current_directory, "guildemojis")
    for file in os.listdir(guildemojis_directory):
        save_id = int(file.rsplit(".")[0])
        path = os.path.join(guildemojis_directory,f"{save_id}.txt")
        if save_id == server.id:
            rando = 0
            c = 0
            try:
                with open(path, "r") as file:
                    for line in file:
                        l = line.strip("\n")
                        if l.isdigit():
                            rando = random.randint(1,int(l)+1)
                        else:
                            if c == rando:
                                split = l.rsplit(",")
                                return f"<:{split[0]}:{split[1]}>"
                        c+=1
            except Exception as e:
                print(e)
                return "random emoji get failed"
    
async def send_text(filename:str):
    name = os.path.join("text",f"{filename}.txt")
    try:
        with open(name, "r") as file:
            return file.read()
    except:
        return None

async def picture_list(channel):
    current_directory = os.getcwd()
    pictures_directory = os.path.join(current_directory, "pictures")
    out = []
    for file in os.listdir(pictures_directory):
        out.append(file.rsplit(".")[0])
    chunks = await break_string_into_chunks("\n".join(out))
    for chunk in chunks:
        await channel.send(chunk)
    return JOE_BIDEN

async def break_string_into_chunks(input_string):
    chunk_size=1999
    return [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]

async def picture(tokens):
    picture_path = ""
    if len(tokens) > 1:
            picture_name = " ".join(tokens[1:])
            picture_path = await get_picture_str(picture_name)
            if picture_path:
                pic_out = discord.File(picture_path)
                output = f"{picture_name}"
            else:
                output = "failed to find picture"
    else:
        rand_pic =  await get_picture_rand()
        pic_out = discord.File(rand_pic[0])
        output = rand_pic[1]
    return [pic_out,output]

async def get_picture_rand():
    pictures_directory = os.path.join(os.getcwd(), "pictures")
    directory_list = os.listdir(pictures_directory)
    length = len(directory_list)
    rand = random.randint(0,length)
    file = directory_list[rand-1] 
    return [os.path.join("pictures",file),file.rsplit(".")[0]]
    
async def get_picture_str(filename:str):
    current_directory = os.getcwd()
    pictures_directory = os.path.join(current_directory, "pictures")
    for file in os.listdir(pictures_directory):
        file_name = file.rsplit(".")[0]

        if file_name.lower() == filename.lower():
            return os.path.join("pictures",file)
        
    return os.path.join("pictures","error.png")

async def ROLL(tokens):
    print("\nRolling")
    if len(tokens)>1:
        return f"You rolled: {await roll_n_dice(int(tokens[1]))}"
    else:
        return f"You rolled: {await roll_n_dice(int(6))}" 
    
async def roll_n_dice(sides:int):
    return random.randint(1,sides -1)

try:
    client.run(TOKEN)
except:
    print("A fatal errors occured. RIP.")