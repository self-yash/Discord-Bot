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
        newAmmount =  int(respo.content)
    
        if newAmmount < 0:
            await ctx.send("Level nikal dunga bakchodi kri toh")
            return
    
        doc_path = db.collection('users').document(userName)
        doc = doc_path.get()
        doc = doc.to_dict()

        if doc['Balance'] > newAmmount:
            await ctx.send(f"Are you sure? You want to withdraw {newAmmount}? (yes/no)")
            confirm = await bot.wait_for('message',check=check(ctx),timeout=40.0)

            if confirm.content.lower() == 'yes':
                updatedamt = doc['Balance'] - newAmmount
                doc = doc_path.update({
                    'Balance' : updatedamt
                })

                await ctx.send(f'{str(newAmmount)} Ammount withdraw')
                await ctx.send(f'Updated Balance: {str(updatedamt)}')
            elif confirm.content.lower() == 'no':
                await ctx.send('withdraw Cancelled.')
            else:
                await ctx.send('Wrong input')
        else:
            await ctx.send('insufficent balance.')

    async def dipostieMoney(ctx,userName):
        await ctx.send("Amount to be Deposited?")
        try:
            respo= await bot.wait_for('message',check=check(ctx),timeout=37.0)
        except:
            await ctx.send("Timed Out. Login Again")
            return 
            
        newAmmount=int(respo.content)

        if newAmmount < 0:
            await ctx.send("Ek raipta lgaunga")
            return
    
        doc_path = db.collection('users').document(userName)
        doc = doc_path.get()
        doc = doc.to_dict()

        updatedamt = doc['Balance'] + newAmmount
        doc = doc_path.update({
           'Balance' : updatedamt
        })

        await ctx.send(f'{str(newAmmount)} Ammount added')
        await ctx.send(f'updated balance: {str(updatedamt)}')

    async def accountClosing(ctx,userName):
        doc_path = db.collection('users').document(userName)
        doc = doc_path.get()
        doc = doc.to_dict()

        if doc['Balance'] > 0:
            await ctx.send('You Need To withdraw your money first.')
        else:
            doc = doc_path.get()
            doc.delete()
            await ctx.send('Your Account Has Closed.')

    async def TakeUserData(ctx,fullname,DoB,Branch):
        if fullname == '':
            await ctx.send('Username cannot be empty. Gharwalo ne naam nhi diya kya bs*k')
            return

        if len(DoB) != 10:
            await ctx.send('Invalid Date of Birth')
            return

        if Branch == '':
            await ctx.send("Branch Cannot be Empty")
            return

        doc = {
            'FullName': fullname,
            'DoB': DoB,
            'Branch': Branch,
            'Balance': 0 
        }
        return doc

    async def MakeUserName(ctx):
        UserName = str(input("Enter Your UserName: "))
        doc_path = db.collection('users').document(UserName)
        finddoc = doc_path.get()

        if finddoc.exists:
            await ctx.send("Username already taken try another.")
            return
        else:
            return UserName


    async def showService(ctx,userName):
        doc_path = db.collection('users').document(userName)
        doc = doc_path.get()
        doc = doc.to_dict()

        await ctx.send(f"\n--------------------- Welcome {doc['FullName']} -------------------------\n")
        await ctx.send('Service Available: \n1. Withdraw money\n2. Deposit money\n3. Check Balance\n4. Account Closing\n5. Logout')

        respo = await bot.wait_for('message',check=check(ctx),timeout=45.0)
        try:
            choise= int(respo.content)
        except:
            await ctx.send("Timed Out")
            return
        if choise == 1:
            await withdrawMoney(ctx,userName)
            await showService(ctx,userName)
        elif choise == 2:
            await dipostieMoney(ctx,userName)
            await showService(ctx,userName)
        elif choise == 3:
            await ctx.send(f"Your Account Balance is {str(doc['Balance'])}")
            await showService(ctx,userName)
        elif choise == 4:
            await accountClosing(ctx,userName)
            await showService(ctx,userName)
        elif choise == 5:
            await ctx.send('Logged Out!')

    @bot.command()
    async def register(ctx,user_name,password,date_of_birth,bra):
        UserDoc = await TakeUserData(ctx,user_name,date_of_birth,bra)
        passwd=1
        DocName = user_name
        if len(password)==4 and password.isdigit():
            passwd = int(password)
        else:
            await ctx.send("Password must be 4 digit and numeric")
            return

        UserDoc['password'] = passwd

        doc_path = db.collection('users').document(DocName)
        doc_path.set(UserDoc)

        await ctx.send(f'You are now registered as {user_name}.')

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
