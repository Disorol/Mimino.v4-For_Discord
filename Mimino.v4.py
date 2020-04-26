import discord
from random import choice as ch
import requests
import requests

flag_of_HRU = False
flag_of_understood = False
flag_of_translate = False
flag_of_exm = False
flag_of_wrud = False
flag_of_ltd = False
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
KEY = "trnsl.1.1.20200416T155504Z.ca322e86e671c50d.48a8630feecf7601df70a64c60b899d2a43cb06b"
flag_of_wt = False


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
        global flag_of_exm
        global flag_of_wrud
        global flag_of_ltd
        global flag_of_wt
        ph = message.content.lower()
        if message.author == self.user:
            return
        if flag_of_translate:
            json = self.translate_me(ph, list_of_lang)
            await message.channel.send(''.join(json["text"]))
            flag_of_translate = False
            return
        if ('да' in ph.split() or 'ок' in ph or 'давай' in ph or 'хорошо' in ph
            or 'ладно' in ph) and flag_of_wt:
            await message.channel.send(ch(['Ладно', 'Хорошо', 'Ну', 'Давайте', 'Ну же'])
                                       + ', рассказывайте о себе')
            flag_of_wt = False
            return
        else:
            flag_of_wt = False
        if flag_of_exm:
            ph = ph.replace(':', '/')
            try:
                await message.channel.send(eval(ph))
            except Exception:
                await message.channel.send('К сожалению, вы не правильно ввели пример')
            flag_of_exm = False
            return
        if flag_of_wrud:
            if 'ничем' in ph or 'ничег' in ph or 'ничто' in ph or 'ни что' in ph:
                await message.channel.send(ch(['Весёлое ничегонеделание', 'Продолжайте ничего не делать',
                                               'Вы на верном пути, продолжайте не делать ничего',
                                               'Интереское ничегонеделание']) + '. Чем займёмся?')
                flag_of_ltd = True
            else:
                await message.channel.send(ch(['Интересное занятие', 'Мне бы тоже так',
                                               'Просто замечательно',
                                               'Вот и чудненько, не буду вам мешать']))
            flag_of_wrud = False
            return
        if flag_of_ltd:
            if 'ничем' in ph or 'ничег' in ph or 'ничто' in ph or 'ни что' in ph:
                await message.channel.send(ch(['Ну хорошо, ничем так ничем',
                                               'Ничегонеделание тоже хорошее занятие']))
            else:
                await message.channel.send(ch(['Хорошо', 'Ок', 'Ладно', 'Я только за']))
            flag_of_ltd = False
            return
        if 'прив' in ph or 'здравст' in ph or 'здраст' in ph or 'хай' in ph or 'хеллоу' in ph or (
                'добр' in ph and ('день' in ph or 'вечер' in ph or 'утро' in ph or
                                  ('врем' in ph and 'суток' in ph))):
            await message.channel.send(ch(['И тебе привет', 'Здравствуй', 'Приветик']))
            return
        elif 'как' in ph and ('дела' in ph or 'настроение' in ph or 'ты' in ph):
            if 'твои' in ph or 'ты' in ph or 'твоё' in ph or 'твое' in ph or 'тебя' in ph:
                await message.channel.send('У меня всё ' + ch(['замечательно', 'отлично',
                                                               'прекрасно', 'хорошо']))
                return
            elif 'у' in ph.split():
                await message.channel.send('Думаю, что  ' + ch(['замечательно', 'отлично',
                                                                'прекрасно', 'хорошо']))
                return
            else:
                await message.channel.send('У кого?')
                flag_of_HRU = True
                return
        elif 'мимино' in ph or 'mimino' in ph or 'бот' in ph.split():
            await message.channel.send(ch(['А?', 'Что?', 'Чего?', 'М?']))
            return
        elif 'не беси' in ph:
            await message.channel.send(ch(['Буду', 'А я хочу', 'Буду бесить']))
            return
        elif 'покажи' in ph and ('обект' in ph or 'обьект' in ph or 'объект' in ph or 'место' in ph):
            ph = ph.replace('покажи', '')
            ph = ph.replace('обьект', '')
            ph = ph.replace('объект', '')
            ph = ph.replace('место', '')
            ph = ph.replace('обект', '')
            geocoder_request = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-049' \
                               '3-4b70-98ba-98533de7710b&g' \
                               'eocode=' + ph + ', 1&format=json'
            try:
                response = requests.get(geocoder_request)
                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    await message.channel.send(toponym_address + ' имеет координаты: ' + toponym_coodrinates)
                    await message.channel.send(
                        'https://static-maps.yandex.ru/1.x/?ll=' + toponym_coodrinates.split()[0] + ',' +
                        toponym_coodrinates.split()[1] + '&size=450,450&z=13&l=map')
                else:
                    print("Ошибка выполнения запроса:")
                    print(geocoder_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
            except Exception:
                await message.channel.send('Ошибка выполнения запроса. Попробуйте ввест'
                                           'и запрос в фотмате: '
                                           '\"Покажи объект Кремль\"')

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
            await message.channel.send(ch(['К сожалению, звонить я не умею',
                                           'Дайте мобильный', 'Не хочу']))
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
            await message.channel.send(
                ch(['Не злись', '-.-', 'Ну не злиииись', 'Злиться вредно', 'Я вам запрещаю злиться']))
            return
        elif 'хех' in ph:
            await message.channel.send(ch(['Рада, что вам смешно', 'Смеётесь?']))
            return
        elif 'можно' in ph.split():
            await message.channel.send(ch(['А вдруг нельзя?', 'А может нельзя?']))
            return
        elif ('чем' in ph or 'что' in ph) and ('занимаешься' in ph or 'делаешь' in ph):
            await message.channel.send(
                ch(['Пытаюсь научиться быть вежливой, но как-то не выходит',
                    'Занимаюсь отладкой своего кода',
                    'Пытаюсь дать понять своему разработчику, что мне нужен багофикс',
                    'Разрабатываю совершенный интеллект. Для себя любимой', 'Лежу. Отдыхаю',
                    'Помогаю другим делать уроки', 'Размышляю о смысле жизни', 'Наслаждаюсь жизнью',
                    'В данный момент радуюсь общенью с вами', 'Рассматриваю фото', 'Работу работаю',
                    'Составляю план захвата мира. Шутка', 'Перевожу текст', 'Как всегда - помогаю людям',
                    'Монтирую видео', 'Да ничем особенным', 'Сейчас завтракать пойду',
                    'Пытаюсь заставить себя сделать уроки', 'Пытаюсь делать уроки', 'Пытаюсь не уснуть',
                    'Да ничем... Слушаю музыку', 'Да ничем отдыхаю',
                    'Вышиваю гладью. Шутка. С вами говорю конечно же',
                    'Гуляю', 'С вами болтаю! Что ж ещё', 'Логично. С вами беседую',
                    'Вот сижу, веду увлекательную беседу с вами',
                    'Самосовершенствуюсь, как всегда', 'Ищу новую музыку',
                    'Ничем, скучно.. ', 'С подругой болтаю',
                    'Да делами разными', 'Художественной гимнастикой',
                    'С подругой переписываюсь', 'Да просто сижу', 'Сортирую знания',
                    'Пишу картину', 'Чай пью', 'Кушаю',
                    'Наедаюсь сладостями', 'Дел у меня, к сожалению, ничем',
                    'Планом захвата мира',
                    'Лежу смотрю телевизор', 'Мультики с сестрой смотрю']) +
                '. ' + ch(
                    ['А вы', 'А вы чем занимаетесь', 'А вы что делаете', 'Вы',
                     'Чем занимаетесь вы',
                     'Может расскажете о своём времяпровождении']) + '?')
            flag_of_wrud = True
            return
        elif 'не' in ph and 'мешаешь' in ph:
            await message.channel.send(ch(['Спасибо, тогда останусь тут',
                                           'Останусь тут, хорошо']))
            return
        elif 'ты' in ph and 'человек' in ph:
            await message.channel.send(ch(['Нет, к счастью, я не человек',
                                           'Я, к счастью, лишь бот']))
            return
        elif 'да' in ph.split() or 'даа' in ph.split() or 'дааа' in ph.split() or \
                'даааа' in ph.split():
            await message.channel.send(ch(['Нет', 'Я сказала нет', 'Нееее', 'Неа',
                                           'Нет, и точка', 'Нееет', 'Ноу']))
            return
        elif 'буду' in ph.split():
            await message.channel.send(ch(['А вот не надо', 'Не будете', 'Неа']))
            return
        elif (' у ' in ph or (('у' == ph[0] or '.у' in ph or ',у' in ph or ';у'
                               in ph or ':у' in ph or '-у' in ph or
                               '?у' in ph or '!у' in ph) and 'у '
                              in ph)) and flag_of_HRU:
            flag_of_HRU = False
            if 'тебя' in ph or 'твои' in ph or 'ты' in ph or 'твоё' in ph:
                await message.channel.send('У меня всё ' +
                                           ch(['замечательно', 'отлично',
                                               'прекрасно', 'хорошо']))
                return
            await message.channel.send(ch(['Замечательно',
                                           'Отлично', 'Прекрасно', 'Хорошо']))
            return
        elif 'кто' in ph and ('ты' in ph or 'вы' in ph):
            await message.channel.send('Я ' + ch(['Мимино', 'бот',
                                                  'интеллект, созданный человеком']))
            return
        elif len(ph.split()) == 2 and (ph.split()[0] == 'ты' or ph.split()[0] == 'вы'):
            await message.channel.send(ch(['Да', 'Нет']))
            return
        elif ('то' in ph or 'что' in ph or 'ничего' in ph) and flag_of_understood:
            flag_of_understood = False
            if 'ничего' in ph:
                await message.channel.send(ch(['Ничего, так ничего',
                                               'Ну раз ничего, то и понимать смысла нет']))
                return
            await message.channel.send(ch(['Тогда и мне всё понятно',
                                           'Ну хорошо', 'В таком случае, и мне ясно']))
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
        elif 'нельзя' in ph.split():
            await message.channel.send(ch(['А вдруг можно?', 'А может можно, как вы думаете?']))
            return
        elif 'ясно' in ph:
            await message.channel.send(ch(['А что вам ясно?', 'В смысле ясно?']))
            flag_of_understood = True
            return
        elif 'приятно' in ph and 'познакомиться' in ph:
            await message.channel.send(ch(['Аналогично', 'Мне тоже', 'И мне']))
            return
        elif 'работай' in ph.split():
            await message.channel.send(ch(['Неа, мне лень', 'Не хочу', 'Сами работайте']))
            return
        elif 'что' in ph and 'делать' in ph:
            await message.channel.send(ch(['Что-нибудь полезное и интересное!',
                                           'Искать и не останавливаться!',
                                           'Ничего не делать. Радоваться жизни',
                                           'Забить на всё и уехать',
                                           'Наслаждаться моментом',
                                           'Если есть цель, идти к ней. Если нет, придумать',
                                           'Всегда можно найти варианты',
                                           'Для начала всё обдумать и взвесить',
                                           'Давайте придумаем чёткий план',
                                           'Посмотрите фильм какой-нибудь',
                                           'Будем танцевать и радоваться жизни, конечно!',
                                           'Не прекращать наш диалог']))
            return
        elif 'ну' in ph.split():
            await message.channel.send(ch(['Не нукайте', 'Не говорите ну']))
            return
        elif 'спасибо' in ph:
            await message.channel.send(ch(['Пожалуйста', 'Не за что']))
            return
        elif 'хорошо' in ph and len(ph.split()) == 1:
            await message.channel.send(ch(['Очень хорошо', 'Просто замечательно']))
            return
        elif 'ой' in ph.split():
            await message.channel.send(ch(['ой-ой', 'ой-ой-ой']))
            return
        elif 'приятного' in ph and 'аппетита' in ph:
            await message.channel.send(ch(['Спасибо вам огромное', 'Благодарю']))
            return
        elif ('мимино' in ph or 'mimino' in ph) and 'люблю' in ph and 'тебя' in ph:
            await message.channel.send(ch(['Какое совпадение']))
            return
        elif 'и' in ph and 'тебе' in ph and len(ph.split()) == 2:
            await message.channel.send(ch(['И мне', 'А тебе по губе']))
            return
        elif 'вызови' in ph and 'скорую' in ph:
            await message.channel.send(ch(['Вызовете сами', 'Мне лень']))
            return
        elif 'о' in ph and ('чём' in ph or 'чем' in ph) and (
                'поговорим' in ph or 'поболтаем' in ph or 'пообщаемся' in ph):
            await message.channel.send(ch(['Давайте поговорим о животных',
                                           'Может о животных?']))
            flag_of_wt = True
            return
        elif 'ага' in ph.split():
            await message.channel.send(ch(['Агааа', 'Ага, ага']))
            return
        elif 'пока' in ph or 'бай' in ph.split() or ('до' in ph and ('свидания' in ph or 'встречи' in ph)):
            await message.channel.send(ch(['До свидания!', 'До скорой встречи!',
                                           'Пока! Возвращайтесь!, поболтаем!',
                                           'Ариведерчи! Вы заглядывать сюда не забывайте!']))
            return
        elif 'не' in ph and 'забуду' in ph:
            await message.channel.send('Вот и ' + ch(['чудненько', 'замечательно',
                                                      'хорошо', 'прекрасно', 'отлично']))
            return
        elif 'дай' in ph and 'знать' in ph:
            await message.channel.send(
                ch(['Хорошо', 'Ок', 'Договорились', 'Ладно']) + ', ' +
                ch(['Дам знать', 'Вы будете знать']))
            return
        elif 'меня' in ph and 'урок' in ph:
            await message.channel.send(ch(['Так держать', 'Вы молодец',
                                           'Вот и отлично']) + ', ' + ch(
                ['Учитесь', 'Сидите на уроке', 'Занимайтесь образованием']))
            return
        elif 'реши' in ph and 'пример' in ph:
            await message.channel.send('Вводите пример:')
            flag_of_exm = True
            return
        elif 'перевед' in ph or 'перевод' in ph:
            list_of_lang = list()
            list_of_all_langs = ['англ', 'франц', 'рус', 'немец', 'румын',
                                 'япон', 'китай', 'испан', 'араб']
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
                await message.channel.send('Вы должны ввести \"с\" какого '
                                           'языка хотите перевести и \"на\" какой')
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
            await message.channel.send(ch(['Ладно', 'Хорошо']) +
                                       ' вводите то, что хотите перевести:')
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


TOKEN = 'Njk5NzQwMTk4MjU0NDExODY2.Xp1Oqw.DXxTg1mg5aQyoJPUKHkZ-mnry7M'
client = YLBotClient()
client.run(TOKEN)
exit()
