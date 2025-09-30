import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram import F
import re

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
dp = Dispatcher()
bot = Bot(token="8239441221:AAHyBufL2Mevz8AJopaBp4QygZ50", default=DefaultBotProperties(parse_mode='html'))


@dp.message(F.text, F.chat.type.in_({"group", "supergroup"}))
async def message_handler(message: types.Message):
    print(message.chat)
    if "=" not in message.text and "-" not in message.text and "+" not in message.text:
        return

    print(message)
    lst = []
    if not message.reply_to_message is None:
        lst += await get_digits(message.reply_to_message.text.split("=")[-1])
    lst += await get_digits(message.text)
    out = []
    cntr = 0
    for q in lst:
        if q[0]:  # если число
            cntr += q[2]
            q[2] = abs(q[2])
        else:  # если слово
            out.append(q)
    if cntr != 0:
        out.append((True, ("+" if cntr > 0 else "-"), cntr))

    out_str = ""
    for q in lst:
        out_str += f"{q[1]} <b>{q[2]}</b> "
    if len(out) == 1:
        out_str += f"= <u>{out[0][2]}</u>"
    elif len(out) == 0:
        out_str += f"= <u>{cntr}</u>"
    else:
        out_str += "\n=\n<u>"
        for q in out:
            out_str += f"{q[1]} <b>{q[2]}</b> "
        out_str += "</u>"

    print(out)
    print(out_str)
    await message.answer(out_str)

@dp.message(F.text)
async def message_handler(message: types.Message):
    await message.answer("Иди в жепу")


async def get_digits(text):
    lst = [(q[0], q[1:].strip()) for q in re.findall(r'[\+\-][^\+-]+', "+" + text)]
    lst2 = []
    for q in lst:
        try:
            lst2.append([True, q[0], int(q[1]) * (-1 if q[0] == "-" else 1)])
        except ValueError:
            numbers = re.findall(r"\d+", q[1])
            if len(numbers) == 1:
                lst2.append([True, q[0], int(numbers[0]) * (-1 if q[0] == "-" else 1)])
            else:
                if len(q[1]) != 0:
                    lst2.append([False, q[0], q[1]])

    return lst2


async def main(_bot):  # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(_bot)


def start_bot():
    asyncio.run(main(bot))


start_bot()
