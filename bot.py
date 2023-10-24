import discord
import responses


async def send_msg(msg, user_msg, is_private):
    try:
        response = responses.get_response(user_msg)
        await msg.author.send(response) if is_private else await msg.channel.send(response)

    except Exceptions as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTE2NjM4Mjk0MTE1NzQ2NjI5Mw.GDqgXz.ZQ9X-o_KjitTo46Kl5TmgI-rzeRdtKXBHnKXB0'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(msg):
        if msg.author == client.user:
            return

        username = str(msg.author)
        user_msg = str(msg.content)
        channel = str(msg.channel)

        print(f'{username} said: "{user_msg}" ({channel})')

        if user_msg[0] == '?':
            user_msg = user_msg[1:]  # "?Help me please" gets rid of ?
            await send_msg(msg, user_msg, is_private=True)
        else:
            await send_msg(msg, user_msg, is_private=False)

    client.run(TOKEN)
