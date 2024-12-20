import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore
load_dotenv()

# Initialize Firebase Admin
cred = credentials.Certificate("skyislimit.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

intents = discord.Intents.all()
TOKEN = os.getenv("bot_token")

bot = commands.Bot(command_prefix='!', intents=intents)

# List for "Foxzy bade log"
bade_log = [
    "bade log", "ultra bade log", "super bade log", "god of bade log",
    "real bade log", "bade log ultra pro max"
]

if TOKEN is None:
    print("Bot token is not set")
else:

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content.startswith('!kingcobra'):
            await message.channel.send('KingCobra is GORBL!')

        await bot.process_commands(message)

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')

    @bot.command()
    async def say(ctx, *, message):
        await ctx.send(message)

    @bot.command()
    async def server(ctx):
        await ctx.send(ctx.guild.name)

    @bot.command()
    async def foxzy(ctx):
        await ctx.send(f"Foxzy is {random.choice(bade_log)}")

    @bot.command()
    async def ping(ctx):
        latency = bot.latency
        ping_ms = round(latency * 1000)
        await ctx.send(f'Pong! Latency: {ping_ms}ms')

    @bot.command()
    async def sum(ctx, num1: int, num2: int):
        result = num1 + num2
        await ctx.send(f'The sum of {num1} and {num2} is {result}')

    @bot.command()
    async def feature(ctx, enabled: bool):
        if enabled:
            await ctx.send("Feature is Enabled")
        else:
            await ctx.send("Feature is Disabled")

    @bot.command()
    async def joined(ctx, *, member: discord.Member):
        join_date = member.joined_at.strftime('%B %d, %Y at %I:%M %p')
        await ctx.send(f'{member} joined on {join_date}')

    def check(ctx):
        def inner(m):
            return m.author == ctx.author

        return inner

async def withdrawMoney(ctx,userName):
    await ctx.send("Amount to Withdraw?")
    respo=await bot.wait_for('message',check=check(ctx),timeout=37.0)
    newAmmount =  int(respo)

    if newAmmount < 0:
        await ctx.send("Level nikal dunga bakchodi kri toh")
    
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    if doc['Balance'] > newAmmount:
        await ctx.send(f"Are you sure? You want to withdraw{newAmmount}? (yes/no)")
        confirm = await bot.wait_for('message',check=check(ctx),timeout=40.0)

        if confirm.content.lower() == 'yes':
            updatedamt = doc['Balance'] - newAmmount
            doc = doc_path.update({
                'Balance' : updatedamt
            })

            await ctx.send(f'{str(newAmmount)} Ammount withdraw')
            await ctx.send(f'updated balance: {str(updatedamt)}')
        elif confirm.content.lower() == 'no':
            await ctx.send('withdraw canncled.')
        else:
            await ctx.send('worng input')
    else:
        await ctx.send('insufficent balance.')

async def showService(ctx,userName):
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    await ctx.send(f"\n--------------------- Wellcome {doc['FullName']} -------------------------\n")

    await ctx.send('Sevrice Avalable: ')
    await ctx.send('1. withdraw money')
    await ctx.send('2. deposite money')
    await ctx.send('3. balance check')
    await ctx.send('4. Account Closing')
    await ctx.send('5. Logout')

    respo = await bot.wait_for('message',check=check(ctx),timeout=45.0)
    choise= int(respo.content)

    if choise == 1:
        await withdrawMoney(ctx,userName)
        await showService(ctx,userName)
    elif choise == 2:
        # dipostieMoney(UserName)
        await showService(ctx,userName)
    elif choise == 3:
        await ctx.send(f"your Account Balance is {str(doc['Balance'])}")
        await showService(ctx,userName)
    elif choise == 4:
        # accountClosing(userName)
        await showService(ctx,userName)
    elif choise == 5:
        await ctx.send('Logout Done!.')

    @bot.command()
    async def login(ctx, user_name, password):
        try:
            password = int(password)
        except ValueError:
            await ctx.send("Password must be numeric. Try again.")
            return

        doc_path = db.collection('users').document(user_name)
        doc = doc_path.get()
        if doc.exists:
            doc = doc.to_dict()
            if password == doc.get('password'):
                await ctx.send(f"You have successfully logged in as {user_name}.\n")
                await showService(ctx,user_name)
                return
            else:
                await ctx.send("Incorrect password. Please try again.")
        else:
            await ctx.send("User not found. Use `.signup` to create a new account.")

    bot.run(TOKEN)