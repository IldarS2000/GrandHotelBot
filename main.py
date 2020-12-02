from aiogram.utils import executor

from bot import dp
import handlers


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
