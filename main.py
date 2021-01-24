import discord
from discord.ext import commands,tasks
from datetime import datetime
from datetime import date

lister= []
wrongs = []

time = datetime.today()
global k
k = str(time).split()
print(k)
print(time)
client = commands.Bot(command_prefix=">")
potd_solvers=[]
done=[]
m = k[0].split("-")
dates = m[2]
month = m[1]
year = m[0]



@tasks.loop(seconds=166800)
async def potd_olver():
    channelx = client.get_channel(801147305596026880)#potd-congrats
    await channelx.send("᲼᲼᲼᲼᲼᲼᲼᲼"*2+"**POTD SOLVERS---------( {}-{}-{} )**".format(dates,month,year))
    await channelx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼")

@client.event
async def on_ready():
    potd_olver.start()
    print("Bot is ready.")



@client.event
async def on_message(message):

    if message.content.startswith(".potdwriterquestions"): #potd_update
        if message.channel.id==801144910127300708 or message.channel.id==802913210311245824:
            await message.channel.send("Enter POTD Question: ")

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            msg = await client.wait_for("message", check=check)
            global potd_question
            potd_question = msg.content.lower()
            await message.channel.send("**POTD Question**")
            await message.channel.send(f'POTD Question is : {potd_question}')

    if message.content.startswith("$potd"):
        await message.channel.send(potd_question)
    if message.channel.id==801148301948223548:#potd_forward
        channel_potd = client.get_channel(787632827822374973)#potd_main
        await channel_potd.send(message.content)


    x = 1

    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="mod-mail")
    if message.content.startswith(".potdans"):
        if message.channel.id==801144910127300708 or message.channel.id==802913210311245824:#potd_update
            channel = client.get_channel(801144910127300708)#potd_update

            await message.channel.send("Enter new answer(must be a number) :")
            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            msg = await client.wait_for("message", check=check)
            global potd_answer
            potd_answer = msg.content.lower()
            await message.channel.send("**POTD Answer**")
            await message.channel.send(f'POTD Answer is : {potd_answer}')
            lister.clear()
            potd_solvers.clear()
            wrongs.clear()
            done.clear()


    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array and not message.author.bot:
            pass

        else:
            k = message.author.id
            embed = discord.Embed(title="potd-log",
                                  colour=message.author.colour,
                                  timestamp=datetime.utcnow())

            embed.set_thumbnail(url=message.author.avatar_url)
            fields = [("Member", message.author.display_name, False), ("Message", message.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await modmail_channel.send(embed=embed)


            t = str(message.author.display_name)
            r = int(message.content)
            if message.content==potd_answer and type(r)==int:
                if t in lister:
                    await message.author.send("You have already solved potd!")
                if t not in lister and t not in wrongs:
                    channel = client.get_channel(801147305596026880)#potd_congrats
                    potd_solvers.append(message.author.display_name)
                    await channel.send("Congratulations {} for solving Today's POTD".format(message.author.mention))
                    lister.append(t)
                    channel3 = client.get_channel(801144941664665600)#potd_log
                    await channel3.send(len(potd_solvers))

                if t in wrongs:
                    await message.author.send("Sorry ! You can't try this POTD now , as you gave wrong answer.")






            if type(r)!=int:
                print(type(message.content))
                await message.author.send("Please enter an integer answer")

            if message.content!= potd_answer and type(r)==int:
                if t not in lister:


                    if t in wrongs:
                        await message.author.send("Sorry ! You can't try this POTD now , as you gave wrong answer.")
                    else:
                        x += 1
                        print(x)
                        if x == 2:
                            wrongs.append(message.author.display_name)
                        await message.author.send("Sorry ! Wrong Answer")
                        channel = client.get_channel(801144941664665600)#potd_log
                        await channel.send(wrongs)



                if t in lister:
                    await message.author.send("You have already solved potd!")








    elif str(message.channel) == "mod-mail" and message.content.startswith("<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments


        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]


@client.command()
async def potdmistake(ctx, *,message):
    if str(message) in wrongs:
        wrongs.remove(str(message))
        await ctx.send("Name removed")
        print(wrongs)
    else:
        print(str(message),wrongs)



client.run('ODAxMTQyMjgwOTY2MTExMjcy.YAcX5A.mW9R01-FQRAN0vOMibHeKi9IBkA')
