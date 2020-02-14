import vk_api
import os, re
import json
from getpass4 import getpass
from tqdm import tqdm
import time, csv, random
from colorama import init, Fore, Back
init(convert=True)


def get_access_token(login='', password='', access_token=0):                            # функция получения access_token
    try:
        User = VK.users.get()
    except:
        print(Fore.RED+"Error")                                                         # вывод ошибки
    else:
        print(f"\nHello {User[0]['first_name']}")                                       # приветствие пользователю, авторизация прошла успешно
        with open('vk_config.v2.json', 'r') as data_file:                               # открыть файл на чтение
            data = json.load(data_file)
        for x in data[login]['token'].keys():
            for y in data[login]['token'][x].keys():
                access_token = data[login]['token'][x][y]['access_token']
    return access_token


def get_base():                                                                         # функция получения ID из базы по раннее отработанным пользователям
    with open('data_base_users.csv', 'r', encoding='utf-8') as resultFile:              # прочесть файл базы данных с ID
        reader = csv.reader(resultFile, delimiter=';')
        headers = next(reader)
        for row in reader:
            try:
                if re.search(r'\D', str(row[0])) or row[0]=='': continue                # если повредилась база и в ней встретилось НЕ число продолжить
                past_id.add(int(row[0]))                                                # внести ID в множество
            except IndexError:                                                          # в случае если база данных пуста
                pass                                                                    # вернуть пустое множество
    return past_id


def search_users(gr=[], list_users=[]):                                                 # функция получения ID пользователей в группах
    offset_list, sort_list=[0, 10, 50, 70, 120, 150, 170],['id_asc','id_desc']
    print(Fore.GREEN + 'Поиск пользователей в тематической группе')
    for i in tqdm(gr):
        try:
            id_gr=i['id']
            us=vk.method('groups.getMembers',{'group_id':id_gr, 'sort':random.SystemRandom().choice(sort_list), 'offset': random.SystemRandom().choice(offset_list)})['items']  # получить ID пользователя
            list_users.extend(us)                                                                                                                                               # внести ID в список
        except Exception as e:                                                                                                                                                  # при возникновении ошибки уснуть на 2 сек.
            time.sleep(1.5)                                                                                                                                                       # исключить слишком частое обращение к API ВК
    return list_users


def get_text_wall(i, info_wall=[]):
    if 'copy_history' in info_wall[i].keys():
        frasa = info_wall[i]['text'] + info_wall[i]['copy_history'][0]['text']
    else:
        frasa = info_wall[i]['text']
    return frasa

def cath_exept(j, result, info_of_user):
    info_of_user[j] = 'отсутствуют данные'
    return info_of_user[j]


def add_result(info_user, info_of_user, ball, result=[]):
    key_list = ['bdate', 'activities', 'interests', 'can_post']
    result.append(info_user)
    result.append(str(info_of_user['first_name']) + ' ' + str(info_of_user['last_name']))
    for j in key_list:
        try:
            if str(info_of_user[j])=='': result.append(cath_exept(j, result, info_of_user))
            else: result.append(str(info_of_user[j]))
        except KeyError as e:
            result.append(cath_exept(str(e), result, info_of_user))
            continue
    result.append(ball)
    result.append(str(time.strftime("%Y-%m-%d")))
    return result


def get_info_wall(list_users=[]):
    print(Fore.GREEN + 'Идет процесс анализа пользовательских страниц')
    for info_user in tqdm(list_users):
        result, ball =[], 0
        try:
            info_wall = vk.method('wall.get', {'owner_id': info_user, 'count': 10})['items']
            time.sleep(random.SystemRandom().choice(pause_time))
            if len(info_wall)<10: continue
            else:
                for i in range(len(info_wall)):
                    frasa=get_text_wall(i, info_wall)
                    if get_look_text(doing, frasa=frasa):
                        ball = ball+1
                        continue
                    else:
                        continue
                    time.sleep(random.SystemRandom().choice(pause_time))
            if ball>0:
                info_of_user = vk.method('users.get', {'user_ids': info_user, 'fields': 'activities, interests, bdate, can_post'})[0]
                base.append(add_result(info_user, info_of_user, ball, result=[]))
            else: continue
        except vk_api.exceptions.ApiError as error:
            if '[9]' in str(error) or '[29]' in str(error):
                print(Fore.RED + str(error))
                print(Fore.RED + ' ВК заблокировал доступ к API. Попробуйте через 24 часа.')
                break
            else:                                                                   # временный запрет на использование API ВК
                time.sleep(random.SystemRandom().choice(pause_time))
                continue                                                            # в случае возникнвения другой ошибки продолжить сессию
        except IndexError:
            continue
    return base


def get_look_text(doing, frasa=''):
    for i in doing:
        pattern1 = r'\b' + i + r'\b'
        if re.search(pattern1, frasa, flags=re.IGNORECASE) is not None: return True  # поиск ключевого слова
        else: continue
    return False

def print_info_error():
    print(Fore.YELLOW + 'Программа перезапустится через 75 секунд.')
    time.sleep(75)


def get_search_text():
    try:
        with open('text_search.txt', 'r', encoding='utf-8') as f:
            word_list=[word.strip().lower() for line in f for word in line.split(',')]
            word_list=list(filter(lambda n: n != '', word_list))
            if word_list==[]:
                print(Fore.RED + 'ВНИМАНИЕ: Вы не наполнили файл "text_search.txt"! ключевыми словами')
                print(Fore.GREEN + 'Для продолжения работы необходимо: ')
                print(Fore.GREEN + '1. Открыть файл "text_search.txt"  и наполнить его ключевыми словами!')
                print(Fore.GREEN + '2. Сохранить и закрыть "text_search.txt".')
                print_info_error()
                run()
        return word_list
    except FileNotFoundError:
        print(Fore.RED + 'ВНИМАНИЕ: Вы не создали файл "text_search.txt"!')
        print(Fore.GREEN + 'Для продолжения работы необходимо: ')
        print(Fore.GREEN + '1. Создать файл "text_search.txt" наполнив его ключевыми словами!')
        print(Fore.GREEN + '2. Поместить его в ту же папку где находится программа.')
        print_info_error()
        run()


def create_base(headers=[['ID','name','birth_date','activities','interests','can_post','post_ball','datetime session']]):       # функция создания базы данных
    try:
        with open('data_base_users.csv', 'r') as resultFile:                                                                    # в случае если сессии проводились ранее прочесть содержимое
            readcsv = csv.reader(resultFile)
    except FileNotFoundError:                                                                                                   # в случае первой сессии и отсутствия файла
        with open('data_base_users.csv', 'w') as resultFile:                                                                    # создать пустой файл с соответствующими заголовками
            wr = csv.writer(resultFile, delimiter=';')
            wr.writerows(headers)


def quest_use_base(quest_use=''): # функция ответа использования базы
    if quest_use == "да": return True
    elif quest_use == "нет": return False
    # в случае ошибки вернуть None и повторить попытку


def enter_name_group():
    while True:
        print(Fore.YELLOW + 'введите запрос на группу: ', end='')
        name_group = input().strip()                                                                    # запрос для поиска групп ВК
        if name_group == '':                                                                            # в случае если запрос пуст повторить
            print(Fore.RED + 'Ошибка: Вы не ввели запрос на группу')
            print(Fore.YELLOW + 'Попрбоуйте снова')
            continue
        else:
            break
    return name_group

def print_info():                                                                                       # функция вывода инструкции и порядка использования
    info_list=info_list=['Программа: VK_Analysis_Users', 'I. Служит для сбора данных об интересах и деятельности пользователей сети ВК.',
                         'II. Утилита может быть полезна специалистам по машинному обучению, блогерам, владельцем коммерческих интернет-площадок.',
                         '--------------------------------------------------',
                         'ИНСТРУКЦИЯ:',
                         '--Перед запуском создайте файл "text_search.txt" в котором через запятую перечислите ключевые слова.',
                         '--НАПРИМЕР: Фотограф, фото, canon, nikon, фотография, фотографировал, фотографировала, съемка, фотопортрет, фотопортреты, фотостудия, фотостудии, модель, Photoshop, снимал, снимала, объектив',
                         '--Сохраните и закройте файл "text_search.txt". Запустите "VK_Analysis_Users"','--Введите ваш логин в формате +79170001020.', '--Введите пароль от своей страницы ВК.','--Запустите программу и введите название тематической группы.',
                         '--Программа заберет ID пользователей состоящих в группе.','--Утилита проведет анализ контента, интересов и дятельности полученных пользователей.','1. Файл "text_search.txt" и "data_base_users.csv"(кодировка utf-8) должны находится в той же папке что и программа.',
                         '2. При завершении в терминал будет выведен ID пользователей которых добавили в базу.',
                         '3. В случае если вы ранее использовали программу есть возможность избежать записи в базу одних и тех пользователей.',
                         '4. Для этого используйте базу данных пользователей которых утилита добавила ранее.',
                         '5. В случае самого первого использования программа создаст пустую базу в формате с именем "data_base_users.csv".',
                         '6. Программа проведет анализ записей на стене каждого найденного пользователя и выставит оценку по 10-ти бальной шкале.','7. Если одно или несколько ключевых слов встретилось в одной записи на стене пользователяю добавляется 1 бал.','8. Программа анализирует последние 10-ть записей на стене пользователя.',
                         '9. Если произвольное из ключевых слов встретилось 8 раз в 8-ми записях оценка пользователя будет равна 8, соответственно если 5 раз то оценка равна 5 и т.д.','10. Программа добавит интересы пользователя и его профессиональную деятельность.',
                         'ПРЕДУПРЕЖДЕНИЕ:',
                         '--Существуют ограничения на использование методов API ВК.',
                         '--Программа не сохраняет ваши пароль и логин.','--Авторизацию необходимо проходить каждый раз при запуске.','--Программа не работает при двухфакторной аутентификации.',
                         '--------------------------------------------------','Разработчик: Сурнов Алексей.', 'e-mail: alslight@list.ru']
    [print(Fore.RED+info_list[k]) if k==23 or k==24 or k==25 or k==26 or k==27 else print(Fore.YELLOW+info_list[k]) for k in range(len(info_list))]


def run():

    print(Fore.BLUE + '--------------------------------------------------')

    while True:
        print(Fore.GREEN + 'Введите логин: ', end='')                                           # цветная печать
        login = input()                                                                         # ввод логина
        password = getpass(prompt=Fore.GREEN + 'Введите ваш пароль: ')                          # ввод пароля
        try:
            global VK
            VK = vk_api.VkApi(login, password)
            VK.auth(reauth=True, token_only=False)
            VK = VK.get_api()
            access_token = get_access_token(login, password)
            break
        except vk_api.exceptions.BadPassword:
            print(Fore.RED + 'Неверное имя пользователя или пароль')
            print(Fore.YELLOW + 'Попрбоуйте снова')
        except vk_api.AuthError:
            print(Fore.RED + 'Неверное имя пользователя или пароль либо отсутствует подключение к интернету.')
            print(Fore.RED + 'Возможно вы используете двухфакторную аутентификацию. Пожалуйста отключите ее')
            print(Fore.YELLOW + 'Попрбоуйте снова')

    create_base()
    global vk
    vk = vk_api.VkApi(token=access_token)

    print(Fore.BLUE + '--------------------------------------------------')

    name_group=enter_name_group()
    gr = vk.method('groups.search', {'q':name_group , 'sort': 0})['items']

    list_users = set(search_users(gr))

    while True:
        print(Fore.BLUE + '------------------------------------------------------------------------')
        print(Fore.YELLOW + 'Чтобы не записывать в базу данных одних и тех же пользователей используйте данные')
        print(Fore.YELLOW + 'по пользователям которых вы ранее вносили')
        print(Fore.BLUE + '------------------------------------------------------------------------')
        print(Fore.YELLOW + 'Использовать базу данных по ранее отработанным пользователям [да/нет]?: ', end='')
        quest_use = input().lower()
        past_id = get_base()
        if quest_use_base(quest_use) == True:
            list_users = list_users - past_id                                                           # удаление пользователей из найденного множества если ранее их вносили в базу данных
            break
        elif quest_use_base(quest_use) == False:
            break                                                                                       # не использовать базу данных
        else:
            print(Fore.RED + 'Ошибка ввода: вы ввели ' + quest_use + '. Пожалуйста попробуйте снова')   # в случае если пользователь ошибся при вводе повторить запрос

    list_users = list(list_users)
    global doing
    doing = get_search_text()

    get_info_wall(list_users)

    with open('data_base_users.csv', 'a', encoding='utf-8') as resultFile:                              # записать в базу данных пользователей
        wr = csv.writer(resultFile, delimiter=';')
        for row in base:
            wr.writerow(row)

    print(Fore.BLUE + '------------------------------------------------------------------------')

    print(Fore.GREEN + 'В базу добавленны следующие пользователи:')
    [[print(Fore.GREEN + str(int(j + 1)) + '. ID: ' + str(base[j][0])) if i == 0 else print(end='') for i in range(len(base[j]))] for j in range(len(base))]
    # вывести в терминал пользователей добавленных в базу



if __name__ == "__main__":                                                                              # запуск программы

    result, base, past_id, ball, shet = [], [], set(), 0,0
    pause_time = [0.8, 0.5, 0.25, 0.15, 1.1]
    print_info()                                                                                        # вывод инструкции
    run()                                                                                               # запуск основной функции программы
    os.remove('vk_config.v2.json')
    print(Fore.GREEN+'сессия завершилась')
    time.sleep(70)