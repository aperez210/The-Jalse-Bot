import os
import random
import time
import discord

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

intent = discord.flags.Intents.all()
client = discord.Client(intents=intent)
@client.event
async def on_ready():
    me = client.user
    print(f'{me} has connected to Discord!')
    g = await select_from_list(client.guilds)
    print(f'{me} is in {g}') 
    channel = await select_from_list(g.channels)
    await start_loop(channel)

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
    await channel.send(f"{ME} is listening")
    try: 
        while not stopped:
            try:
                async for message in channel.history(limit=1):
                    out = message.content
                    try:
                        attatchment = message.attachments[0]
                    except:
                        attatchment = None
            except Exception as error:
                message = "error"
                print(error)
            stopped = await int_and_respond(channel,out,attatchment)
            if out != "":
                print(out,end="\r")
            time.sleep(1)
            print("\r",end="")
    except Exception as e:
        print("Stopped!")
        await channel.send(f"{ME} has stopped listening")
        quit()

async def int_and_respond(channel,message,attatch):
    output = "default"
    pic_out = None
    if message:
        if message[0] == "|":
            message = message[1:len(message)]
            tokens = message.split(" ")
            match tokens[0].lower():
                case "joe":
                    match tokens[1].lower():
                        case "biden":
                            output = "".join([JOE_BIDEN]*10)
                case "stop":
                    print("\nStopping...")
                    return True
                case "say":
                    print("\nSending message...")
                    output = " ".join(tokens[1:])
                case "roll":
                    print("\nRolling")
                    if len(tokens)>1:
                        output = f"You rolled: {await roll_n_dice(int(tokens[1]))}"
                    else:
                        output = f"You rolled: {await roll_n_dice(int(6))}"    
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
                        output = "FUCK!"
                    pic_name = await picture(tokens)
                    if not attatch:
                        pic_out = pic_name[0]
                        output = pic_name[1]
                    else:
                        output = "picture get"
                    print(f"\nSending the picture {output}")
                case "piclist":
                    output = await picture_list(channel)
    
            if pic_out:
                await channel.send(output, file=pic_out)
            else: 
                await channel.send(output)
    return False

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

async def roll_n_dice(sides:int):
    return random.randint(1,sides -1)

try:
    client.run(TOKEN)
except:
    print("this shit is FUCKED")