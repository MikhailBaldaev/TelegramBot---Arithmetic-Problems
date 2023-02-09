import random
import telebot

from config import *

token = token

bot = telebot.TeleBot(token)

list_problems = []
count = 0

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    global list_problems

    for i in range(2):
        problem_plus1 = random.randint(100, 999)
        problem_plus2 = random.randint(100, 999)
        plus = [f'{problem_plus1}+{problem_plus2}=', problem_plus1 + problem_plus2]
        list_problems.append(plus)
        sent = bot.send_message(cid, plus)

        problem_minus1 = random.randint(100, 999)
        problem_minus2 = random.randint(problem_minus1, 999)
        minus = [f'{problem_minus2}-{problem_minus1}=', problem_minus2 - problem_minus1]
        list_problems.append(minus)
        sent = bot.send_message(cid, minus)

        problem_mult1 = random.randint(0, 10)
        problem_mult2 = random.randint(0, 10)
        mult = [f'{problem_mult1}*{problem_mult2}=', problem_mult1 * problem_mult2]
        list_problems.append(mult)
        sent = bot.send_message(cid, mult)

    sent = bot.send_message(cid, 'Напиши ответы на примеры через запятую. Например, так: 100, 32, 654, 987')
    bot.register_next_step_handler(sent, call)


def call(message):
    global list_problems
    global count

    right_answers = [str(i[1]) for i in list_problems]
    answers = [i.strip() for i in message.text.split(',')]
    answers = [i if i.isdigit() else 0 for i in answers]

    if len(answers) < len(list_problems):
        for i in range(len(list_problems) - len(answers)):
            answers.append(0)
    elif len(answers) > len(list_problems):
        for i in range(len(answers) - len(list_problems)):
            answers.pop()

    if answers == right_answers:
        sent = bot.send_message(message.chat.id, 'Все верно!')
        for i in list_problems:
            sent = bot.send_message(message.chat.id, f'{i[0]}{i[1]}')
        list_problems = []
        sent = bot.send_message(message.chat.id, 'Можно начать заново: нажми на /start!')
    else:

        if count == 4:
            sent = bot.send_message(message.chat.id, f'Что-то у тебя не выходит. Правильные ответы:')
            for i in list_problems:
                sent = bot.send_message(message.chat.id, f'{i[0]}{i[1]}')
            return

        sent = bot.send_message(message.chat.id, 'Есть ошибки')

        for i in range(len(list_problems)):
            if answers[i] == str(list_problems[i][1]):
                sent = bot.send_message(message.chat.id, f' Верно: {list_problems[i][0]}{list_problems[i][1]}')
            elif answers[i] != str(list_problems[i][1]):
                sent = bot.send_message(message.chat.id, f' Неверно: {list_problems[i][0]}')

        sent = bot.send_message(message.chat.id, f'Попробуй еще раз!')
        count += 1
    bot.register_next_step_handler(sent, call)


bot.polling(none_stop=True)
