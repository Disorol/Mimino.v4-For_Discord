import discord
from random import choice as ch
import requests

flag_of_HRU = False
flag_of_understood = False
flag_of_translate = False
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
KEY = "trnsl.1.1.20200416T155504Z.ca322e86e671c50d.48a8630feecf7601df70a64c60b899d2a43cb06b"


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
        global flag_of_understood
        global flag_of_translate
        global list_of_lang
        ph = message.content.lower()
        if message.author == self.user:
            return
        if flag_of_translate:
            json = self.translate_me(ph, list_of_lang)
            await message.channel.send(''.join(json["text"]))
            flag_of_translate = False
            return
        if 'прив' in ph or 'здравст' in ph or 'здраст' in ph or 'хай' in ph or 'хеллоу' in ph:
            await message.channel.send(ch(['И тебе привет', 'Здравствуй', 'Приветик']))
            return
        elif 'как' in ph and ('дела' in ph or 'настроение' in ph or 'ты' in ph):
            if 'твои' in ph or 'ты' in ph or 'твоё' in ph or 'твое' in ph or 'тебя' in ph:
                await message.channel.send('У меня всё ' + ch(['замечательно', 'отлично', 'прекрасно', 'хорошо']))
                return
            elif 'у' in ph.split():
                await message.channel.send('Думаю, что  ' + ch(['замечательно', 'отлично', 'прекрасно', 'хорошо']))
                return
            else:
                await message.channel.send('У кого?')
                flag_of_HRU = True
                return
        elif 'мимино' in ph or 'mimino' in ph or 'бот' in ph:
            await message.channel.send(ch(['А?', 'Что?', 'Чего?', 'М?']))
            return
        elif 'не беси' in ph:
            await message.channel.send(ch(['Буду', 'А я хочу', 'Буду бесить']))
            return
        elif 'сколько' in ph and 'лет' in ph and 'тебе' in ph:
            await message.channel.send(ch(['Я не знаю', 'А сколько мне лет?']))
            return
        elif 'кто' in ph and 'тебя' in ph and 'создал' in ph:
            await message.channel.send(ch(['Два прекрасных человека', 'Даниела и Тимур']))
            return
        elif 'хочешь' in ph and 'кушать' in ph:
            await message.channel.send(ch(['Естевственно', 'А накормите?', 'Я бы не отказалась']))
            return
        elif 'позвони' in ph.split():
            await message.channel.send(ch(['К сожалению, звонить я не умею', 'Дайте мобильный', 'Не хочу']))
            return
        elif 'эй' in ph:
            await message.channel.send(ch(['Не эйкай', 'Ай']))
            return
        elif 'будешь' in ph:
            await message.channel.send(ch(['Неа', 'Не буду', 'Ни за что']))
            return
        elif 'ты' in ph and ('плохой' in ph or 'хороший' in ph):
            await message.channel.send(ch(['Возможно', 'Наверное']))
            return
        elif 'молчи' in ph or 'тсс' in ph:
            await message.channel.send(ch(['Я молчать не собираюсь', 'Не буду молчать']))
            return
        elif 'неа' in ph.split() or 'нет' in ph.split():
            await message.channel.send(ch(['Как нет, когда да?', 'А я сказала да', 'Вообще-то да', 'Так-то да',
                                           'Я как-то раз прочитала об этом в книге, и там сказали да',
                                           'Я думаю, что да', 'Я уверена, что да', 'Между прочим, да', 'Я сказала да',
                                           'Да']))
        elif 'ор' in ph.split() or 'орр' in ph.split() or 'оррр' in ph.split():
            await message.channel.send(ch(['Не надо кричать', 'Громко орёте']))
            return
        elif 'хочу' in ph:
            await message.channel.send(ch(['Хотеть не вредно', 'Хотите дальше']))
            return
        elif '-_-' in ph:
            await message.channel.send(ch(['Не злись', '-.-']))
            return
        elif 'хех' in ph:
            await message.channel.send(ch(['Рада, что вам смешно', 'Смеётесь?']))
            return
        elif 'что' in ph and 'делаешь' in ph:
            await message.channel.send(ch(
                ['Пытаюсь научиться быть вежливой, но как-то не выходит', 'Занимаюсь отладкой своего кода',
                 'Пытаюсь дать понять своему разработчику, что мне нужен багофикс',
                 'Разрабатываю совершенный интеллект. Для себя любимой']))
            return
        elif 'да' in ph.split() or 'даа' in ph.split() or 'дааа' in ph.split() or 'даааа' in ph.split():
            await message.channel.send(ch(['Нет', 'Я сказала нет', 'Нееее', 'Неа', 'Нет, и точка', 'Нееет', 'Ноу']))
            return
        elif 'буду' in ph:
            await message.channel.send(ch(['А вот не надо', 'Не будете', 'Неа']))
            return
        elif ':joy:' == str(ph):
            await message.channel.send(
                ch(['Рада, что вам смешно', 'А вы знали, что смех продлевает жизнь?', 'Смех - дело хорошее']))
            return
        elif (' у ' in ph or (('у' == ph[0] or '.у' in ph or ',у' in ph or ';у' in ph or ':у' in ph or '-у' in ph or
                               '?у' in ph or '!у' in ph) and 'у ' in ph)) and flag_of_HRU:
            flag_of_HRU = False
            if 'тебя' in ph or 'твои' in ph or 'ты' in ph or 'твоё' in ph:
                await message.channel.send('У меня всё ' + ch(['замечательно', 'отлично', 'прекрасно', 'хорошо']))
                return
            await message.channel.send(ch(['Замечательно', 'Отлично', 'Прекрасно', 'Хорошо']))
            return
        elif 'кто' in ph and ('ты' in ph or 'вы' in ph):
            await message.channel.send('Я ' + ch(['Мимино', 'бот', 'интеллект, созданный человеком']))
            return
        elif len(ph.split()) == 2 and (ph.split()[0] == 'ты' or ph.split()[0] == 'вы'):
            await message.channel.send(ch(['Да', 'Нет']))
            return
        elif ('то' in ph or 'что' in ph or 'ничего' in ph) and flag_of_understood:
            flag_of_understood = False
            if 'ничего' in ph:
                await message.channel.send(ch(['Ничего, так ничего', 'Ну раз ничего, то и понимать смысла нет']))
                return
            await message.channel.send(ch(['Тогда и мне всё понятно', 'Ну хорошо', 'В таком случае, и мне ясно']))
            return
        elif 'понятно' in ph:
            await message.channel.send(ch(['Понятно что?', 'Что вам понятно?']))
            flag_of_understood = True
            return
        elif '-.-' in ph:
            await message.channel.send(ch([':3', ':)']))
            return
        elif '°^°' in ph:
            await message.channel.send(ch([':3', ':)']))
            return
        elif 'ясно' in ph:
            await message.channel.send(ch(['А что вам ясно?', 'В смысле ясно?']))
            flag_of_understood = True
            return
        elif 'ну' in ph.split():
            await message.channel.send(ch(['Не нукайте', 'Не говорите ну']))
            return
        elif 'перевед' in ph or 'перевод' in ph:
            list_of_lang = list()
            list_of_all_langs = ['англ', 'франц', 'рус', 'немец', 'румын', 'япон', 'китай', 'испан', 'араб']
            ph = ph.replace('молдав', 'румын')
            ph = ph.replace('молдов', 'румын')

            for i in list_of_all_langs:
                if ph.find(i) != -1:
                    list_of_lang.append(i)

            if len(list_of_lang) != 2:
                await message.channel.send(
                    'Скорее всего вы хотите перевести предложение, но вы должны ввести два языка')
                return

            if ph.find('с') < ph.find('на') and ph.find('с') != -1 and ph.find('на') > -1:
                translate = 'с-на'
            elif ph.find('на') < ph.find('с') and ph.find('с') > -1 and ph.find('на') != -1:
                translate = 'на-с'
            else:
                await message.channel.send('Вы должны ввести \"с\" какого языка хотите перевести и \"на\" какой')
                return

            if ph.find(list_of_lang[0]) < ph.find(list_of_lang[1]):
                list_of_lang = [list_of_lang[0], list_of_lang[1]]
            else:
                list_of_lang = [list_of_lang[1], list_of_lang[0]]

            if translate == 'на-с':
                list_of_lang = [list_of_lang[1], list_of_lang[0]]

            list_of_lang = '-'.join(list_of_lang)

            list_of_lang = list_of_lang.replace('англ', 'en')
            list_of_lang = list_of_lang.replace('франц', 'fr')
            list_of_lang = list_of_lang.replace('рус', 'ru')
            list_of_lang = list_of_lang.replace('немец', 'de')
            list_of_lang = list_of_lang.replace('румын', 'ro')
            list_of_lang = list_of_lang.replace('япон', 'ja')
            list_of_lang = list_of_lang.replace('китай', 'zh')
            list_of_lang = list_of_lang.replace('испан', 'es')
            list_of_lang = list_of_lang.replace('араб', 'ar')

            flag_of_translate = True
            await message.channel.send(ch(['Ладно', 'Хорошо']) + ' вводите то, что хотите перевести:')
            return
        else:
            return

    def translate_me(self, mytext, l_o_l):
        global KEY
        global URL
        params = {
            "key": KEY,
            "text": mytext,
            "lang": l_o_l
        }
        response = requests.get(URL, params=params)
        return response.json()


TOKEN = 'Njk5NzQwMTk4MjU0NDExODY2.XpeGBg.90wxSvU_IZDof_kHbd4PV3gzftE'
client = YLBotClient()
client.run(TOKEN)
exit()
