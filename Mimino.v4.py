import discord
from random import choice as ch

flag_of_HRU = False


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        global flag_of_HRU
        ph = message.content.lower()
        if message.author == self.user:
            return
        if 'привет' in ph:
            await message.channel.send('И тебе привет')
            return
        elif 'как' in ph and ('дела' in ph or 'настроение' in ph):
            if 'твои' in ph or 'ты' in ph or 'твоё' in ph or 'твое' in ph or 'тебя' in ph:
                await message.channel.send('У меня всё ' + ch(['замечательно', 'отлично', 'прекрасно', 'хорошо']))
                return
            else:
                await message.channel.send('У кого?')
                flag_of_HRU = True
                return
        elif (' у ' in ph or (('у' == ph[0] or '.у' in ph or ',у' in ph or ';у' in ph or ':у' in ph or '-у' in ph or
                               '?у' in ph or '!у' in ph) and 'у ' in ph)) and flag_of_HRU:
            if 'тебя' in ph or 'твои' in ph or 'ты' in ph or 'твоё' in ph:
                await message.channel.send('У меня всё ' + ch(['замечательно', 'отлично', 'прекрасно', 'хорошо']))
                flag_of_HRU = False
                return
            await message.channel.send(ch(['Замечательно', 'Отлично', 'Прекрасно', 'Хорошо']))
            flag_of_HRU = False
            return
        elif len(ph.split()) == 2 and ph.split()[0] == 'ты' or ph.split()[0] == 'вы':
            await message.channel.send(ch(['Да', 'Нет']))
            return
        else:
            return


TOKEN = 'Njk5NzQwMTk4MjU0NDExODY2.XpYx3Q.fK8CWo2evQ1kbPWVvmLerv79pwc'
client = YLBotClient()
client.run(TOKEN)
exit()
