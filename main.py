import discord
from discord.utils import get
from discord.ext import commands,tasks
from datetime import datetime
from datetime import date
import json
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
number_of_triesusers={}
first_try_wrong=[]
number_of_tries = []
points_got = {}
total_points_got = {}
print(number_of_tries)
potd_questions=[]
potd_solvers_with_formention={}
fivepointers=[]
fourpointers=[]
threepointers=[]
twopointers=[]
onepointers=[]
@client.event
async def on_ready():
    print("Bot is ready.")



@client.event
async def on_message(message):


    if message.content.startswith(".potdwriterquestions") and message.channel.id==801144910127300708:#potd_update
        await message.channel.send("Enter POTD Question: ")

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        global potd_question
        potd_question = msg.content.lower()
        await message.channel.send("**POTD Question**")
        await message.channel.send(f'POTD Question is : {potd_question}')
        potd_questions.append(potd_question)

    if message.content.startswith("$potd"):
        await message.channel.send(potd_question)
    if message.channel.id==801148301948223548:#potd_forward
        channel_potd = client.get_channel(787632827822374973)#potd_main
        await channel_potd.send(message.content)




    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="mod-mail")
    if message.content.startswith(".potdans") and message.channel.id ==801144910127300708 :#potd_update
        channel = client.get_channel(801144910127300708)#potd_update

        await channel.send("Enter new answer(must be a number) :")
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        msg = await client.wait_for("message", check=check)
        global potd_answer
        potd_answer = msg.content.lower()
        await channel.send("**POTD Answer**")
        await channel.send(f'POTD Answer is : {potd_answer}')
        lister.clear()
        potd_solvers.clear()
        wrongs.clear()
        done.clear()
        number_of_triesusers.clear()
        first_try_wrong.clear()
        points_got.clear()
        number_of_tries.clear()
        fivepointers.clear()
        fourpointers.clear()
        threepointers.clear()
        twopointers.clear()
        onepointers.clear()
        total_points_got.clear()


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
            #correct answer
            t = str(message.author.display_name)
            r = int(message.content)
            if message.content==potd_answer and type(r)==int:
                if t in lister:
                    await message.author.send("You have already solved potd!")
                if t not in lister and t not in wrongs:
                    channel = client.get_channel(801147305596026880)#potd_congrats
                    potd_solvers.append(message.author.display_name)
                    potd_solvers_with_formention[message.author.display_name]=message.author.id
                    if t not in first_try_wrong:

                        await message.author.send("Congratulations ! You got **5** Points for this question.")
                        await message.author.send("Leaderboard will be released at end of POTD")
                        points_got[t]=1
                        total_points_got[t]=5
                        channelnn = client.get_channel(801144941664665600)#potd_log
                        await channelnn.send("PSC Admin " +  message.author.display_name+" got the answer correct , please give him role of POTD Solver in the server.")
                    if t in first_try_wrong:
                        points_get_bywrong=5-number_of_triesusers[t]
                        await message.author.send(f"Congratulations ! You got {points_get_bywrong} Points for this question.")
                        await message.author.send("Leaderboard will be released at end of POTD")
                        channelnn = client.get_channel(801144941664665600)#potd_log
                        await channelnn.send("PSC Admin " +  message.author.display_name+" got the answer correct , please give him role of POTD Solver in the server.")
                        points_got[t]=(6-points_get_bywrong)
                        total_points_got[t]=points_get_bywrong

                    lister.append(t)
                    channel3 = client.get_channel(801144941664665600)#potd_log
                    await channel3.send(len(potd_solvers))



                if t in wrongs:
                    await message.author.send("Sorry ! You can't try this POTD now , as you gave wrong answer.")






            if type(r)!=int:
                print(type(message.content))
                await message.author.send("Please enter an integer answer")
            #wrong_answer
            if message.content!= potd_answer and type(r)==int:
                if t not in lister:
                    if t not in wrongs:

                        if t in first_try_wrong:
                            number_of_triesusers[str(message.author.display_name)]+=1   
                        if t not in first_try_wrong:
                            first_try_wrong.append(t)
                            number_of_triesusers[str(message.author.display_name)]=1    
                        print(first_try_wrong)
                        #number_of_tries.append("wrong")
                        #print(number_of_tries)
                        #print(len(number_of_tries))
                        chances_left = 5-number_of_triesusers[str(message.author.display_name)]
                        print(number_of_triesusers)
                        if number_of_triesusers[str(message.author.display_name)]==6:
                            wrongs.append(message.author.display_name)
                        else:    
                            await message.author.send("Sorry ! Wrong Answer")
                            if chances_left==1:

                                await message.author.send(f"You have {chances_left} chance left")
                            else:
                                await message.author.send(f"You have {chances_left} chances left")    
                            channel = client.get_channel(801144941664665600)#potd_log
                            await channel.send(wrongs)

                        print(wrongs)    
                    if t in wrongs:
                        await message.author.send("Sorry ! You can't try this POTD now , as you gave wrong answer.")



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
    if message.content.startswith("noone"):
        await message.channel.send("NO ONE SOLVED POTD-{lengthofpotd} :(")       
    if message.content.startswith("$lb"):
        lengthofpotd = len(potd_questions)
        await message.channel.send(f"**POTD-{lengthofpotd} SOLVERS**")
        Weightedfactor=100/(len(lister))
        print(Weightedfactor)
        for pog in potd_solvers_with_formention:
            print(total_points_got[pog])
            if total_points_got[pog]==5 and pog not in fivepointers:


                fivepointers.append(pog)

            if total_points_got[pog]==4 and pog not in fourpointers:
                fourpointers.append(pog)
            if total_points_got[pog]==3 and pog not in threepointers:
                threepointers.append(pog)    
            if total_points_got[pog]==2 and pog not in twopointers:
                twopointers.append(pog)
            if total_points_got[pog]==1 and pog not in onepointers:
                onepointers.append(pog)            
        for five in fivepointers :
            await message.channel.send("**"+five+"**"+"   5pt")
        for four in fourpointers :
            await message.channel.send("**"+four+"**"+"   4pt")    
        for three in threepointers :
            await message.channel.send("**"+three+"**"+"   3pt") 
        for two in twopointers:
            await message.channel.send("**"+two+"**"+"   2pt")
        for one in onepointers:
            await message.channel.send("**"+one+"**"+"   1pt")            
    if message.content.startswith("$weightedpointslb"):
        lengthofpotd = len(potd_questions)
        await message.channel.send(f"**POTD-{lengthofpotd} SOLVERS**")
        Weightedfactor=100/(len(lister))
        print(Weightedfactor)
        await message.channel.send("Weighted Factor ="+Weightedfactor)
        for pog in potd_solvers_with_formention:
            print(total_points_got[pog])
            if total_points_got[pog]==5 and pog not in fivepointers:


                fivepointers.append(pog)

            if total_points_got[pog]==4 and pog not in fourpointers:
                fourpointers.append(pog)
            if total_points_got[pog]==3 and pog not in threepointers:
                threepointers.append(pog)    
            if total_points_got[pog]==2 and pog not in twopointers:
                twopointers.append(pog)
            if total_points_got[pog]==1 and pog not in onepointers:
                onepointers.append(pog)            
        for five in fivepointers:
            mult = 5*Weightedfactor
            await message.channel.send("**"+five+"**"+f"   5pt*{Weightedfactor}=**{mult}**")
        for four in fourpointers:
            multi = 4*Weightedfactor
            await message.channel.send("**"+four+"**"+f"   4pt*{Weightedfactor}=**{multi}**")   
        for three in threepointers:
            multip = 3*Weightedfactor
            await message.channel.send("**"+three+"**"+f"   3pt*{Weightedfactor}=**{multip}**")
        for two in twopointers:
            multipl = 2*Weightedfactor
            await message.channel.send("**"+two+"**"+f"   2pt*{Weightedfactor}=**{multipl}**")
        for one in onepointers:
            multiple= Weightedfactor
            await message.channel.send("**"+one+"**"+f"   1pt*{Weightedfactor}=**{multiple}**") 
    if message.content.startswith("$kanerithi"):
            await message.channel.send(potd_answer)         
@client.command()
async def potdmistake(ctx, *,message):
    if str(message) in wrongs:
        wrongs.remove(str(message))
        await ctx.send("Name removed")
        print(wrongs)
    else:
        print(str(message),wrongs)



client.run('ODAxMTQyMjgwOTY2MTExMjcy.YAcX5A.mW9R01-FQRAN0vOMibHeKi9IBkA')
