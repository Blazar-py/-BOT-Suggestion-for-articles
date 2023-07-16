from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


bot = Bot(token="TOKEN")
admin_id = 123123123123123123   # ТВОЙ ID

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    predlojka = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Здравствуйте! Предложите идею для статьи.')
    await UserState.predlojka.set()


@dp.message_handler(state=UserState.predlojka)
async def predlojka(message: types.Message, state: FSMContext):
    await bot.send_message(admin_id, f'Пришла новая идея от {message.from_user.username}:'
                                     f'\n\n{message.text}')
    await message.answer('Спасибо!')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)