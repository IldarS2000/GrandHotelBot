from aiogram import types

from bot import dp, bot
from states import MainForm, ServicesForm
from keyboards import back_to_main_menu_keyboard, keyboard_with_back_button, services_button, back_button

services = [('Тренажерный зал',
             """Здесь представлены различные модели спортивных тренажеров: все кардио (эллиптический, степпер, беговые дорожки, велотренажеры). Имеются все необходимые тренажеры на все группы мышц, а также свободные веса (блины, гантели, штанги).\n\nРежим работы: с 7.00 до 23.00 ежедневно.""",
             'images/services/gym.jpg'),
            ('Бассейн',
             """За те тысячелетия, что люди пользуются сауной и водными процедурами, они стали играть в их жизни очень значимую роль. Сауна и бассейн - это места, где можно снять усталость, расслабиться и набрать новые силы. Приятное тепло, возможность, способствующая полному расслаблению, потрясающее ощущение чистоты и отличного самочувствия может дать только сауна. А почувствовать приятную свежесть и легкость вам поможет плаванье в нашем небольшом, но комфортном бассейне. Бассейн: длина – 20м, ширина - 4м, глубина – 170 см.\n\nРежим работы: с 7.00 до 23.00 ежедневно.""",
             'images/services/swim_pool.jpg'),
            ('Бильярд',
             """Если Вы хотите приятно провести вечер и отдохнуть в компании своих друзей, мы приглашаем Вас в развлекательный центр гостиницы АМАКС Сафар отель. К Вашим услугам - бильярдная зона на первом этаже. Увлекательная и изысканная игра, которую ценят миллионы людей по всему миру поможет Вам расслабиться и насладиться приятным вечером в компании своих друзей.\n\nРежим работы: круглосуточно""",
             'images/services/pool.jpg'),
            ('Бар',
             """Тёплая атмосфера «Piano Bar» - это идеальное место  для проведения деловой встречи за чашкой ароматного кофе или для завершения рабочего дня за бокалом изысканного коньяка. Мягкие комфортные диваны помогут расслабиться и полноценно ощутить атмосферу уюта и непринужденности. Меню бара включает также множество сортов чая, кофе, горячего шоколада, прохладительные и алкогольные напитки. Каждый вечер, в приглушенном свете волшебных фонарей для Вас звучит живая фортепианная музыка в виртуозном исполнении пианиста!\n\nБар работает для Вас ежедневно и круглосуточно.""",
             'images/services/bar.jpg'),
            ('Ресторан',
             """В ресторане 100 посадочных мест, для VIP-гостей предусмотрен отдельный зал на 25 человек. В меню включены такие блюда, как стейк из говядины с соусом, баранина на кости, филе норвежского лосося, северная форель, тигровые креветки и любимые блюда Федора Ивановича Шаляпина. Ресторан «Капелла» прекрасное место для проведения романтического ужина, банкетов, свадеб и деловой встречи с партнерами.\n\nВремя работы: с 7.00 до 23.00, ежедневно""",
             'images/services/restaurant.jpg')]


@dp.message_handler(lambda message: message.text in services_button + back_button,
                    state=[MainForm.menu, ServicesForm.checking_service],
                    content_types=types.ContentTypes.TEXT)
async def choose_service(message: types.Message):
    await ServicesForm.menu.set()

    services_titles = [f'{i}. {value[0]}\n' for i, value in enumerate(services, 1)]
    titles = ''.join(services_titles)
    await message.answer(f'Введите порядковое число развлечения, о котором хотите узнать подробнее, например "1"\n'
                         f'{titles}', reply_markup=back_to_main_menu_keyboard)


def filter_service_number(message: types.Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= len(services):
            return True
    return False


@dp.message_handler(lambda message: not filter_service_number(message), state=ServicesForm.menu)
async def choose_service_invalid(message: types.Message):
    await message.reply('введен не существующий номер, попробуйте снова')


@dp.message_handler(filter_service_number, state=ServicesForm.menu)
async def show_service(message: types.Message):
    await ServicesForm.checking_service.set()

    service_number = message.text
    service = services[int(service_number) - 1]

    await message.answer(service[1])
    await bot.send_photo(message.chat.id, open(service[2], 'rb'))
    await message.answer('пожалуйста внимательно изучите время работы, спасибо!',
                         reply_markup=keyboard_with_back_button)
