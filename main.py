from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import *
# import re
import asyncio
from aiogram.utils.exceptions import CantInitiateConversation, ChatNotFound, BotBlocked

print(444)
#bot = Bot(token="6390845058:AAGc80cZgBv6UbQI_AeD4utEg2GkjQon73I")
bot = Bot(token="7037507472:AAFB_JU964RA79QUCiL_-1McLw8G6cIXbZg")  # test

dp = Dispatcher(bot, storage=MemoryStorage())

keyboard_main_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard=True)

'''
keyboard_main_admin.row(types.KeyboardButton('Новые заявки'), types.KeyboardButton('Новые заявки(Все)'))
keyboard_main_admin.add(types.KeyboardButton('Все заявки'), types.KeyboardButton('Отложенные заявки'))
keyboard_main_admin.row(types.KeyboardButton('Принятые заявки'), types.KeyboardButton('Отклоненные заявки'))
keyboard_main_admin.add(types.KeyboardButton('Удалить просмотренные заявки'))
keyboard_main_admin.add(types.KeyboardButton('Поддержка'))
'''

keyboard_main_admin.row(types.KeyboardButton('Отложенные'), types.KeyboardButton('Отработанные'),
                        types.KeyboardButton('В очереди'))
keyboard_main_admin.row(types.KeyboardButton('Удалить отработанные заявки'))
keyboard_main_admin.add(types.KeyboardButton('Отправить уведомление'))
keyboard_main_admin.row(types.KeyboardButton('Справка'), types.KeyboardButton('Поддержка'))

keyboard_user.add(types.KeyboardButton('Отправить уведомление'))
keyboard_user.row(types.KeyboardButton('Справка'))
keyboard_user.add(types.KeyboardButton('Поддержка'))
keyboard_user.add(types.KeyboardButton('Регистрация'))

keyboard_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_exit.row(types.KeyboardButton('Вернуться в начало'))

keyboard_approve = types.InlineKeyboardMarkup(row_width=2)
approve_button = types.InlineKeyboardButton("Одобрено", callback_data='approve')
reject_button = types.InlineKeyboardButton("Отклонено", callback_data='reject')
talk_button = types.InlineKeyboardButton("Подойти", callback_data='talk')
skip_button = types.InlineKeyboardButton("Отложить", callback_data='skip')
prev_button = types.InlineKeyboardButton("⬅️", callback_data='prev')
next_button = types.InlineKeyboardButton("➡️", callback_data='next')
keyboard_approve.add(approve_button, reject_button, talk_button, skip_button, prev_button, next_button)

keyboard_yes = types.InlineKeyboardMarkup(row_width=2)
yes_button = types.InlineKeyboardButton("Да", callback_data='yes')
no_button = types.InlineKeyboardButton("Нет", callback_data='no')
keyboard_yes.add(yes_button, no_button)

keyboard_department = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_department.row(types.KeyboardButton('ЦР'), types.KeyboardButton('ЦК2'), types.KeyboardButton('ЦК3'))
keyboard_department.row(types.KeyboardButton('ЦК4'), types.KeyboardButton('ЦК5'), types.KeyboardButton('ЦК6'))
keyboard_department.row(types.KeyboardButton('ЦК7'), types.KeyboardButton('ЦК8'), types.KeyboardButton('ЦК9'))
keyboard_department.add(types.KeyboardButton('Вернуться в начало'))


class MessageText(StatesGroup):
    waiting_for_name = State()


class SupportText(StatesGroup):
    waiting_for_text = State()


class RegText(StatesGroup):
    waiting_for_department_for_reg = State()
    waiting_for_name_for_reg = State()


class SendNot(StatesGroup):
    waiting_for_dep_to_send = State()
    waiting_for_name_to_send = State()
    waiting_for_not_to_send = State()


class Reg(StatesGroup):
    waiting_for_id = State()
    waiting_for_username = State()
    waiting_for_fio = State()
    waiting_for_department = State()


def status_define(check):
    a = ''
    if check == 0:
        a = 'Новое'
    elif check == 1:
        a = 'Одобрено'
    elif check == 2:
        a = 'Отклонено'
    elif check == 3:
        a = 'Отложено'
    elif check == 4:
        a = 'Подойти'
    elif check == 5:
        a = 'Просмотрено'
    return a


'''
@dp.message_handler(commands=["info"], chat_type=[types.ChatType.PRIVATE])
async def info(message: types.Message):
    await message.answer(
        "Здравствуйте, я Алита, роботизированный секретарь Центра развития. Я помогаю направлять уведомления "
        "руководству Центра по рассмотрению и согласованию документов.\n - Чтобы увидеть это сообщение введите "
        "/info\n - "
        "Чтобы увидеть список пользователей, которым можно отправить уведомление, напишите /list\n\n Чтобы я могла вам "
        "помочь, напишите мне в личные сообщения /start, затем, в беседе, в которой я состою, напишите уведомление, "
        "которое вы хотите отправить руководителю в формате 'send "
        "Фамилия Имя Руководителя|Текст обращения'", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=["list"], chat_type=[types.ChatType.PRIVATE])
async def get_fio(message: types.Message):
    fio_list_message = 'Вот список доступных получателей:\n'
    for fio in fio_list:
        fio_list_message += str(fio[2]) + '\n'
    await message.answer(fio_list_message, reply_markup=types.ReplyKeyboardRemove())
'''


@dp.message_handler(state=SendNot.waiting_for_dep_to_send, chat_type=[types.ChatType.PRIVATE])
async def send_command(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        global keyboard_admin_list
        async with state.proxy() as data:
            data['department'] = message.text
        keyboard_admin_list = types.ReplyKeyboardMarkup(resize_keyboard=True)
        fio_list = get_fio_from_department(message.text)
        print(fio_list)
        for fio in fio_list:
            keyboard_admin_list.add(types.KeyboardButton(str(fio[0])))
        keyboard_admin_list.add(types.KeyboardButton('Вернуться в начало'))
        await message.answer('Выберите получателя', reply_markup=keyboard_admin_list)
        await SendNot.waiting_for_name_to_send.set()


@dp.message_handler(state=SendNot.waiting_for_name_to_send, chat_type=[types.ChatType.PRIVATE])
async def send_command(message: types.Message, state: FSMContext):
    '''
    pattern = re.compile(r'\b(send)\b', re.IGNORECASE)
    mes = re.sub(pattern, '', message.text)
    mes = re.sub(r"\s+", " ", mes)
    mes = mes.replace(" |", "|")
    mes = mes.split('|')
    mes[0] = mes[0][1:]
    '''
    async with state.proxy() as data:
        data['name'] = message.text

    admins_fio = get_fio()

    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    elif (message.text,) in admins_fio:
        if message.from_user.username is not None:
            await message.reply('Напишите ваше уведомление', reply_markup=keyboard_exit)
            await SendNot.waiting_for_not_to_send.set()
        else:
            if is_in_admins(message):
                await message.reply(f"Сообщение не было отправлено, потому что у вас не установлен "
                                    f"никнейм.\nУстановить его можно в настройках телеграмма",
                                    reply_markup=keyboard_main_admin)
                await MessageText.waiting_for_name.set()
            else:
                await message.reply(f"Сообщение не было отправлено, потому что у вас не установлен "
                                    f"никнейм.\nУстановить его можно в настройках телеграмма",
                                    reply_markup=keyboard_user)
                await MessageText.waiting_for_name.set()
    else:
        print(5)
        await message.answer('Пожалуйста, выберите кого-то из списка ниже.', reply_markup=keyboard_admin_list)


@dp.message_handler(state=SendNot.waiting_for_not_to_send, chat_type=[types.ChatType.PRIVATE])
async def send_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sender_id'] = message.from_user.id
        data['sender_username'] = message.from_user.username
        data['message'] = message.text
        sender_id = data['sender_id']
        sender_username = data['sender_username']
        name = data['name']
        department = data['department']
        message_text = data['message']
    result = get_id_from_fio(name)
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    elif message.from_user.username is not None:
        try:
            insert_messages(result[0], sender_id, sender_username, message_text,
                            message.date, 0)
            await bot.send_message(result[0],
                                   f"Вам прислал уведомление  @{sender_username}:\n{message_text}")
            await message.reply(f"Сообщение отправлено")
        except (CantInitiateConversation, ChatNotFound, BotBlocked) as e:
            await message.reply(
                f"Что-то пошло не так! Сообщение не было отправлено. Возможно, получатель заблокировал бота.")
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()


'''
@dp.message_handler(commands=["FIO", "info"], chat_type=[types.ChatType.PRIVATE])
async def unable_to_use(message: types.Message):
    await message.answer('Данный функционал не доступен в личных сообщениях.')
'''


@dp.message_handler(filters.Text(startswith='Вернуться в начало', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def go_to_main_menu(message: types.Message, state: FSMContext):
    result = get_id()
    await state.finish()
    if (message.from_user.id,) in result:
        await message.answer("Пожалуйста, выберите что-то из меню ниже",
                             reply_markup=keyboard_main_admin)
        await MessageText.waiting_for_name.set()
    else:
        await message.answer("Пожалуйста, выберите что-то из меню ниже",
                             reply_markup=keyboard_user)


# Обработчик команды /start
@dp.message_handler(commands="start", chat_type=types.ChatType.PRIVATE)
async def start(message: types.Message):
    result = get_id()
    if (message.from_user.id,) in result:
        await message.reply("Здравствуйте, выберите, что вы хотите сделать",
                            reply_markup=keyboard_main_admin)
        await MessageText.waiting_for_name.set()
    else:
        await message.reply("Здравствуйте, выберите, что вы хотите сделать", reply_markup=keyboard_user)
        await MessageText.waiting_for_name.set()


@dp.message_handler(commands="reg_admin", chat_type=types.ChatType.PRIVATE)
async def reg_admin_id(message: types.Message):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    elif message.from_user.id == 547523349:
        await message.answer('Введите Id пользователя', reply_markup=keyboard_exit)
        await Reg.waiting_for_id.set()


@dp.message_handler(state=Reg.waiting_for_id, chat_type=types.ChatType.PRIVATE)
async def reg_admin_username(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            data['ID'] = message.text
        await message.answer('Введите username пользователя', reply_markup=keyboard_exit)
        await Reg.waiting_for_username.set()


@dp.message_handler(state=Reg.waiting_for_username, chat_type=types.ChatType.PRIVATE)
async def reg_admin_fio(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            data['username'] = message.text
        await message.answer('Введите фамилию и имя пользователя', reply_markup=keyboard_exit)
        await Reg.waiting_for_fio.set()


@dp.message_handler(state=Reg.waiting_for_fio, chat_type=types.ChatType.PRIVATE)
async def reg_admin_db(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer('Выберите свой отдел', reply_markup=keyboard_department)
        await Reg.waiting_for_department.set()


@dp.message_handler(state=Reg.waiting_for_department, chat_type=types.ChatType.PRIVATE)
async def reg_admin_db(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            data['department'] = message.text
            id = data['ID']
            username = data['username']
            name = data['name']
            department = data['department']
        text = insert_new_admin(id, username, name, department)
        if is_in_admins(message):
            await message.answer(text,
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer(text,
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()


@dp.message_handler(state=RegText.waiting_for_name_for_reg, chat_type=types.ChatType.PRIVATE)
async def support_group(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer('Выберите ваш отдел', reply_markup=keyboard_department)
        await RegText.waiting_for_department_for_reg.set()


@dp.message_handler(state=RegText.waiting_for_department_for_reg, chat_type=types.ChatType.PRIVATE)
async def support_group(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        async with state.proxy() as data:
            reg_name = data['name']
        await bot.send_message(-4029925124,
                               f'Новая заявка на регистрацию!\nID:{message.from_user.id}\nNickname:@'
                               f'{message.from_user.username}\nИмя:{reg_name}\nОтдел:{message.text}')
        result = get_id()
        if (message.from_user.id,) not in result:
            await message.answer('Ваше заявка на регистрацию будет рассмотрена в ближайшее время!',
                                 reply_markup=keyboard_user)
        await state.finish()
        await MessageText.waiting_for_name.set()


def is_in_admins(message):
    result = get_id()
    if (message.from_user.id,) in result:
        return True
    else:
        return False


@dp.message_handler(state=MessageText.waiting_for_name, chat_type=types.ChatType.PRIVATE)
async def name_chosen(message: types.Message, state: FSMContext):
    global notification_list
    notification_list = []
    global index
    index = 0
    admins = get_id()
    if (message.from_user.id,) in admins:
        if message.text == 'В очереди':
            notification_list = get_rows_by_id_and_status(message.from_user.id, [0, 5])
            await message.reply("Тут ваши заявки!",
                                reply_markup=keyboard_exit)
            if len(notification_list) > 0:
                a = status_define(notification_list[index][-1])
                await bot.send_message(message.from_user.id,
                                       f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                       f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                       reply_markup=keyboard_approve)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'У вас пока нет уведомлений')
                result = get_id()
                if (message.from_user.id,) in result:
                    await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                         reply_markup=keyboard_main_admin)
                else:
                    await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                         reply_markup=keyboard_user)
                await MessageText.waiting_for_name.set()
        elif message.text == 'Отложенные':
            notification_list = get_rows_by_id_and_status(message.from_user.id, [3])
            await message.reply("Тут ваши заявки!",
                                reply_markup=keyboard_exit)
            if len(notification_list) > 0:
                a = status_define(notification_list[index][-1])
                await bot.send_message(message.from_user.id,
                                       f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                       f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                       reply_markup=keyboard_approve)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'У вас пока нет уведомлений')
                await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                     reply_markup=keyboard_main_admin)
                await MessageText.waiting_for_name.set()
        elif message.text == 'Отработанные':
            notification_list = get_rows_by_id_and_status(message.from_user.id, [1, 2, 4])
            await message.reply("Тут ваши заявки!",
                                reply_markup=keyboard_exit)
            if len(notification_list) > 0:
                a = status_define(notification_list[index][-1])
                await bot.send_message(message.from_user.id,
                                       f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                       f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                       reply_markup=keyboard_approve)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'У вас пока нет уведомлений')
                await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                     reply_markup=keyboard_main_admin)
                await MessageText.waiting_for_name.set()
        elif message.text == 'Удалить отработанные заявки':
            delete_notifications(message.from_user.id)
            await message.reply('Уведомления со статусами *Отклонено* и *Одобрено* успешно удалены!',
                                parse_mode="Markdown",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        elif message.text == 'Поддержка':
            await state.finish()
            await SupportText.waiting_for_text.set()
            await message.reply('Напишите ваше обращение в поддержку', reply_markup=keyboard_exit)
        elif message.text == 'Отправить уведомление':
            await state.finish()
            await SendNot.waiting_for_dep_to_send.set()
            await message.reply('Выберите отдел получателя', reply_markup=keyboard_department)
        elif message.text == 'Справка':
            await message.answer(
                "Здравствуйте, я Алита, роботизированный секретарь Центра развития. Я помогаю направлять уведомления "
                "руководству Центра по рассмотрению и согласованию документов. Как только статус направленного вами "
                "уведомления изменится - я дам вам знать!\nТакже я могу добавить вас в список получателей, "
                "чтобы вы тоже могли получать уведомления.\n Обязательно сообщите об ошибке в поддержку, если такие "
                "найдутся! Мои создатели оперативно всё решат и пользоваться мной станет ещё удобнее.\nНадеюсь на "
                "продуктивное сотрудничество!😁")
        elif message.text == 'Закрыть':
            await bot.send_message(message.from_user.id, 'Чтобы продолжить работу в главном меню напишите /start')
            await state.finish()

        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже", reply_markup=keyboard_main_admin)
        if message.text == "Вернуться в начало":
            await state.finish()
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()

    else:
        if message.text == 'Поддержка':
            await state.finish()
            await SupportText.waiting_for_text.set()
            await message.reply('Напишите ваше обращение в поддержку', reply_markup=keyboard_exit)
        elif message.text == 'Отправить уведомление':
            await state.finish()
            await SendNot.waiting_for_dep_to_send.set()
            await message.reply('Выберите отдел получателя', reply_markup=keyboard_department)
        elif message.text == 'Регистрация':
            await state.finish()
            await RegText.waiting_for_name_for_reg.set()
            await message.reply('Напишите ваши Фамилию и Имя', reply_markup=keyboard_exit)
        elif message.text == 'Справка':
            await message.answer(
                "Здравствуйте, я Алита, роботизированный секретарь Центра развития.\n Я помогаю направлять "
                "уведомления руководству Центра развития и ЦК ЦР по рассмотрению и согласованию документов в САДД. "
                "Как только статус направленного вами уведомления изменится - я дам вам знать!Если вы "
                "руководитель/заместитель руководителя ЦР или ЦК я могу добавить вас в список получателей, "
                "чтобы вы тоже могли получать уведомления.\nОбязательно сообщите об ошибке в поддержку, если такие "
                "найдутся! Мои создатели оперативно всё решат и пользоваться мной станет ещё удобнее.\n\nНадеюсь на "
                "продуктивное сотрудничество!😁")
        if message.text == "Вернуться в начало":
            await state.finish()
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    '''
    elif message.text == 'Отклоненные заявки':
        notification_list = get_rows_by_value(message.from_user.id, 2)
        await message.reply("Тут ваши заявки!",
                            reply_markup=keyboard_exit)
        await status_change(message, state)
    elif message.text == 'Отложенные заявки':
        notification_list = get_rows_by_value(message.from_user.id, 3)
        await message.reply("Тут ваши заявки!",
                            reply_markup=keyboard_exit)
        await status_change(message, state)
    '''
    '''
    elif message.text == 'Новые заявки(Все)':
        notification_list = get_rows_by_value(message.from_user.id, 0)
        await message.reply("Тут ваши заявки!",
                            reply_markup=keyboard_exit)
        await MessageText.waiting_for_name.set()
        if len(notification_list) == 0:
            await bot.send_message(message.from_user.id,
                                   'Пока новых заявок нет!', reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            for i in notification_list:
                await bot.send_message(message.from_user.id,
                                       f'От: @{i[3]}\nДата уведомления: {i[-2]}'
                                       f'\nУведомление: {i[4]}\nСтатус: Новое', reply_markup=keyboard_main_admin)
                await MessageText.waiting_for_name.set()
    '''


@dp.callback_query_handler(lambda c: c.data in ['approve', 'reject', 'next', 'prev', 'talk', 'skip'],
                           chat_type=types.ChatType.PRIVATE)
async def handle_inline_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    global index
    if callback_query.data == 'approve':
        if notification_list[index][-1] != 1:
            update_value_in_database(notification_list[index][0], 1)
            try:
                await bot.send_message(notification_list[index][2],
                                       f'@{callback_query.from_user.username} изменил статус вашего уведомления *{notification_list[index][4]}* на одобрено',
                                       parse_mode="Markdown")
            except (CantInitiateConversation, ChatNotFound, BotBlocked) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя '
                                       f'@{notification_list[index][3]}:{notification_list[index][4]}, изменился на '
                                       f'одобрено.'
                                       f'У этого пользователя нет чата с ботом! Напомните ему!')

            if len(notification_list) > 0:
                notification_list.pop(index)
                index -= 1
        await callback_query.message.delete()
        new_msg = await callback_query.message.answer("Уведомление одобрено")
        await asyncio.sleep(0.5)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await new_msg.delete()
        except Exception as e:
            pass

        if index < len(notification_list) - 1:
            index += 1

        if len(notification_list) != 0:
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                   f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            print(3)
            print(index, len(notification_list))
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id,
                                   "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    elif callback_query.data == 'reject':
        if notification_list[index][-1] != 2:
            update_value_in_database(notification_list[index][0], 2)
            try:
                print(notification_list)
                await bot.send_message(notification_list[index][2],
                                       f'@{callback_query.from_user.username} изменил статус вашего уведомления *{notification_list[index][4]}* на отклонено',
                                       parse_mode="Markdown")
            except (CantInitiateConversation, ChatNotFound, BotBlocked) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя @{notification_list[index][3]}:'
                                       f'{notification_list[index][4]}, изменился на отклонено. У этого пользователя нет '
                                       f'чата с ботом! Напомните ему!')
            if len(notification_list) > 0:
                notification_list.pop(index)
                index -= 1
        await callback_query.message.delete()
        new_msg = await callback_query.message.answer("Уведомление отклонено")
        await asyncio.sleep(0.5)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await new_msg.delete()
        except Exception as e:
            pass
        print(index, len(notification_list))

        if index < len(notification_list) - 1:
            index += 1
            print(1)
            print(index, len(notification_list))
        elif index == len(notification_list) - 1 and len(notification_list) > 1:
            # index -= 1
            print(2)
            print(index, len(notification_list))

        if len(notification_list) != 0:
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                   f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            print(3)
            print(index, len(notification_list))
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id,
                                   "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    elif callback_query.data == 'talk':
        if notification_list[index][-1] != 4:
            update_value_in_database(notification_list[index][0], 4)
            try:
                await bot.send_message(notification_list[index][2],
                                       f'@{callback_query.from_user.username} хочет поговорить по поводу уведомления: {notification_list[index][4]}\nПожалуйста, свяжитесь с получателем в скорейшем времени')
            except (CantInitiateConversation, ChatNotFound, BotBlocked) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя @{notification_list[index][3]}:'
                                       f'{notification_list[index][4]}, изменился на поговорить. У этого пользователя нет '
                                       f'чата с ботом! Напомните ему!')
            if len(notification_list) > 0:
                notification_list.pop(index)
                index -= 1
        await callback_query.message.delete()
        new_msg = await callback_query.message.answer(
            "Отправили уведомление отправителю, с вами в скором времени свяжутся")
        await asyncio.sleep(0.5)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await new_msg.delete()
        except Exception as e:
            pass
        print(index, len(notification_list))

        if index < len(notification_list) - 1:
            index += 1
            print(1)
            print(index, len(notification_list))
        elif index == len(notification_list) - 1 and len(notification_list) > 1:
            # index -= 1
            print(2)
            print(index, len(notification_list))

        if len(notification_list) != 0:
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                   f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            print(3)
            print(index, len(notification_list))
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id,
                                   "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    elif callback_query.data == 'skip':
        if notification_list[index][-1] != 3:
            update_value_in_database(notification_list[index][0], 3)
            '''
            try:
                await bot.send_message(notification_list[index][2],
                                       f'Статус вашего уведомления:{notification_list[index][4]}, изменился на отклонено')
            except (CantInitiateConversation, ChatNotFound) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя @{notification_list[index][3]}:'
                                       f'{notification_list[index][4]}, изменился на отклонено. У этого пользователя нет '
                                       f'чата с ботом! Напомните ему!')
            '''
            if len(notification_list) > 0:
                notification_list.pop(index)
                index -= 1
        await callback_query.message.delete()
        new_msg = await callback_query.message.answer("Уведомление отложено")
        await asyncio.sleep(0.5)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await new_msg.delete()
        except Exception as e:
            pass
        print(index, len(notification_list))
        if index < len(notification_list) - 1:
            index += 1
            print(1)
            print(index, len(notification_list))
        elif index == len(notification_list) - 1 and len(notification_list) > 1:
            # index -= 1
            print(2)
            print(index, len(notification_list))

        if len(notification_list) != 0:
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}'
                                   f'\nУведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            print(3)
            print(index, len(notification_list))
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id,
                                   "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    elif callback_query.data == 'next':
        if notification_list[index][-1] == 0:
            update_value_in_database(notification_list[index][0], 5)
            '''
            try:
                await bot.send_message(notification_list[index][2],
                                       f'Статус вашего уведомления:{notification_list[index][4]}, изменился на отложено')
            except (CantInitiateConversation, ChatNotFound) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя @{notification_list[index][3]}:'
                                       f'{notification_list[index][4]}, изменился на отложено. У этого пользователя нет '
                                       f'чата с ботом! Напомните ему!')
            '''
        if index < len(notification_list) - 1:
            index += 1
            print(notification_list, index)
            await callback_query.message.delete()
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}\n'
                                   f'Уведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id, "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    elif callback_query.data == 'prev':
        if notification_list[index][-1] == 0:
            update_value_in_database(notification_list[index][0], 5)
            '''
            try:
                await bot.send_message(notification_list[index][2],
                                       f'Статус вашего уведомления:{notification_list[index][4]}, изменился на отложено')
            except (CantInitiateConversation, ChatNotFound) as e:
                await bot.send_message(547523349,
                                       f'Статус уведомления пользователя @{notification_list[index][3]}:'
                                       f'{notification_list[index][4]}, изменился на отложено. У этого пользователя нет '
                                       f'чата с ботом! Напомните ему!')
            '''

        if index > 0:
            index -= 1
            print(notification_list, index)
            await callback_query.message.delete()
            a = status_define(notification_list[index][-1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Заявка {index + 1} из {len(notification_list)}\nОт: @{notification_list[index][3]}\nДата уведомления: {notification_list[index][-2]}\n'
                                   f'Уведомление: {notification_list[index][4]}\nСтатус: {a}',
                                   reply_markup=keyboard_approve)
        elif len(notification_list) == 0:
            await state.finish()
            await bot.send_message(callback_query.from_user.id, "Уведомления закончились!",
                                   reply_markup=keyboard_main_admin)
            await bot.send_message(callback_query.from_user.id, "Пожалуйста, выберите что-то из меню ниже",
                                   reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()


'''
@dp.message_handler(state=MessageText.view_messages, chat_type=types.ChatType.PRIVATE)
async def get_mes(message: types.Message, state: FSMContext):
    print(1)
    await state.finish()
    if len(notification_list) > 0:
        a = ''
        if notification_list[0][-1] == 1:
            a = 'Одобрено'
        elif notification_list[0][-1] == 2:
            a = 'Отклонено'
        elif notification_list[0][-1] == 0:
            a = 'Новое'
        elif notification_list[0][-1] == 3:
            a = 'Отложено'
        await bot.send_message(message.from_user.id,
                               f'От: @{notification_list[0][3]}\nДата уведомления: {notification_list[0][-2]}'
                               f'\nУведомление: {notification_list[0][4]}\nСтатус: {a}',
                               reply_markup=keyboard_approve)
    else:
        await bot.send_message(message.from_user.id, 'У вас пока нет уведомлений')
        await message.answer("Пожалуйста, выберите что-то из меню ниже",
                            reply_markup=keyboard_main_admin)
        await MessageText.waiting_for_name.set()

    if message.text == "Вернуться в начало":
        cur.execute("""SELECT id FROM Users""")
        result = cur.fetchall()
        await state.finish()
        if (message.from_user.id,) in result:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
'''

"""
@dp.message_handler(state=MessageText.waiting_for_text, chat_type=types.ChatType.PRIVATE)
async def text_entered(message: types.Message, state: FSMContext):
    if message.text == "Вернуться в начало":
        cur.execute(""SELECT id FROM Users"")
        result = cur.fetchall()
        if (message.from_user.id,) in result:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
    else:
        await state.update_data(text=message.text)
        user_data = await state.get_data()
        await message.reply(
            f"Вы написали пользователю {user_data['chosen_person']} следующее: {message.text}\nОтправить?",
            reply_markup=keyboard_approve_send)
        await MessageText.waiting_for_approval.set()



@dp.message_handler(state=MessageText.waiting_for_approval, chat_type=types.ChatType.PRIVATE)
async def text_entered(message: types.Message, state: FSMContext):
    if message.text == "Вернуться в начало":
        cur.execute("SELECT id FROM Users")
        result = cur.fetchall()
        if (message.from_user.id,) in result:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()

    elif message.text == "Да":
        user_data = await state.get_data()
        needed_id = 0
        for fio in fio_list:
            if fio[2] == user_data['chosen_person']:
                needed_id = fio[0]
        insert_messages(needed_id, message.from_user.id, message.from_user.username, user_data['text'], message.date, 0)
        try:
            await bot.send_message(needed_id,
                                   f"Вам прислал уведомление @{message.from_user.username}:\n{user_data['text']}")
            await message.reply(f"Сообщение отправлено")
            await state.finish()
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        except():
            await message.reply(f"Что-то пошло не так...")
            await state.finish()
    elif message.text == "Нет":

        await message.reply("Введите сообщение, которое хотите отправить:")
        await MessageText.waiting_for_text.set()
    elif message.text == "Вернуться в начало":
        cur.execute(""SELECT id FROM Users"")
        result = cur.fetchall()
        if (message.from_user.id,) in result:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
"""


@dp.message_handler(state=SupportText.waiting_for_text, chat_type=types.ChatType.PRIVATE)
async def support_group(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в начало':
        print(6)
        if is_in_admins(message):
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_main_admin)
            await MessageText.waiting_for_name.set()
        else:
            await message.answer("Пожалуйста, выберите что-то из меню ниже",
                                 reply_markup=keyboard_user)
            await MessageText.waiting_for_name.set()
    else:
        await bot.send_message(-4029925124, f'Новый отзыв!\nNickname:@{message.from_user.username}\n{message.text}')
        result = get_id()
        if (message.from_user.id,) in result:
            await message.answer('Сообщение отправлено!', reply_markup=keyboard_main_admin)
        else:
            await message.answer('Сообщение отправлено!', reply_markup=keyboard_user)
        await state.finish()
        await MessageText.waiting_for_name.set()


async def on_startup(_):
    ids = get_id()
    users_ids = get_user_id()
    users_ids += ids
    users_ids = set(users_ids)
    print(users_ids)
    for i in users_ids:
        print(i[0])
        try:
            await bot.send_message(i[0], '❗️❗️❗️*Бот был обновлен, для корректной работы, пожалуйста, напишите* '
                                         '/start❗️❗️❗️\n - Исправлена ошибка при которой сообщение приходит не тому '
                                         'получателю.', parse_mode="Markdown")
        except (CantInitiateConversation, ChatNotFound, BotBlocked) as e:
            print(f'ошибка у пользователя {i}')
            pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
