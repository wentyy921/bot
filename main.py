import os
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv


# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("Ошибка: Токен бота не найден. Убедитесь, что вы создали файл .env и добавили в него BOT_TOKEN.")
    exit(1)

# Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения состояний пользователей (String или PinPass)
user_modes = {}

# Летспик: замена 1 или 2 букв на цифры для еще большей уникальности
def leet_speak(text, probability=0.4):
    # Применяем случайную замену с заданной вероятностью, чтобы сохранить "человечность"
    if not text or random.random() > probability:
        return text
        
    subs = {'o': '0', 'e': '3', 'i': '1', 'l': '1', 'a': '4', 's': '5', 'b': '8'}
    possible_indices = [i for i, char in enumerate(text.lower()) if char in subs]
    
    if not possible_indices:
        return text
        
    num_replacements = min(random.randint(1, 2), len(possible_indices))
    indices_to_replace = random.sample(possible_indices, num_replacements)
    
    chars = list(text)
    for i in indices_to_replace:
        # Preserve case somewhat, though leet substitutions are numbers mostly
        chars[i] = subs[chars[i].lower()]
        
    return "".join(chars)

def generate_pinpass():
    # Логин: 8-16 символов, 1-3 цифры, без дублирования слов
    login_words = [
        'vibe', 'coding', 'zone', 'valley', 'jackson', 'stone', 'base', 'core', 'epic', 'nexus', 
        'pulse', 'spark', 'flare', 'echo', 'drift', 'wave', 'storm', 'peak', 'net', 'hub', 'link',
        'forge', 'pixel', 'cipher', 'fluid', 'vertex', 'quantum', 'logic', 'synth', 'hyper', 
        'cyber', 'neon', 'nova', 'aero', 'dynamic', 'static', 'grid', 'prism', 'flux', 'vector',
        'orbit', 'stellar', 'lunar', 'solar', 'astral', 'cosmic', 'omega', 'alpha', 'delta', 
        'sigma', 'apex', 'zenith', 'crest', 'crown', 'shield', 'blade', 'anvil', 'hammer',
        'vault', 'crypt', 'safe', 'key', 'lock', 'code', 'data', 'byte', 'bit', 'node', 'mesh',
        'wire', 'cable', 'fiber', 'optic', 'sonic', 'acoustic', 'visual', 'laser', 'beam',
        'ray', 'flash', 'streak', 'dash', 'rush', 'surge', 'flow', 'tide', 'ripple', 'splash',
        'drop', 'mist', 'fog', 'cloud', 'sky', 'star', 'moon', 'sun', 'dust', 'ash', 'coal',
        'iron', 'steel', 'gold', 'silver', 'bronze', 'copper', 'brass', 'zinc', 'lead', 'tin',
        'wood', 'leaf', 'root', 'branch', 'tree', 'forest', 'grove', 'park', 'field', 'meadow',
        'hill', 'mountain', 'crag', 'cliff', 'rock', 'pebble', 'sand', 'dune', 'desert', 'oasis',
        'ocean', 'sea', 'lake', 'river', 'stream', 'creek', 'brook', 'pond', 'pool', 'puddle',
        'ice', 'snow', 'frost', 'chill', 'cold', 'cool', 'warm', 'hot', 'heat', 'fire', 'flame',
        'burn', 'glow', 'blaze', 'ember', 'smoke', 'fume', 'gas', 'air',
        'wind', 'breeze', 'gale', 'tempest', 'hurricane', 'cyclone', 'tornado', 'twister',
        'hawk', 'wolf', 'bear', 'lion', 'tiger', 'fox', 'lynx', 'raven', 'crow', 'eagle', 'falcon',
        'smith', 'jones', 'miller', 'davis', 'garcia', 'brown', 'wilson', 'moore', 'taylor', 'anderson',
        'thomas', 'white', 'harris', 'martin', 'thompson', 'robinson', 'clark', 'lewis', 'walker',
        'shark', 'snake', 'viper', 'cobra', 'rhino', 'hippo', 'panda', 'koala', 'zebra', 'moose',
        'camel', 'whale', 'seal', 'otter', 'badger', 'skunk', 'dingo', 'sloth', 'puma', 'jaguar',
        'panther', 'cougar', 'leopard', 'cheetah', 'hyena', 'jackal', 'dhole', 'red', 'blue', 'green',
        'yellow', 'orange', 'purple', 'pink', 'black', 'white', 'gray', 'cyan', 'magenta', 'maroon', 
        'olive', 'lime', 'teal', 'navy', 'aqua', 'crimson', 'scarlet', 'ruby', 'amber', 'thunder', 
        'light', 'dark', 'shadow', 'water', 'earth', 'gem', 'jewel', 'diamond', 'crystal', 'pearl',
        'jade', 'onyx', 'quartz', 'meteor', 'comet', 'planet', 'galaxy', 'nebula', 'pulsar', 'quasar', 
        'void', 'abyss', 'williams', 'jackson', 'martinez', 'rodriguez', 'lee', 'hall', 'allen', 
        'young', 'hernandez', 'king', 'wright', 'lopez', 'scott', 'adams', 'baker', 'gonzalez', 
        'nelson', 'carter', 'mitchell', 'perez', 'roberts', 'turner', 'phillips', 'campbell', 'parker', 
        'evans', 'edwards', 'collins', 'stewart', 'sanchez', 'morris', 'rogers', 'reed', 'cook', 'morgan', 
        'bell', 'murphy', 'bailey', 'rivera', 'cooper', 'richardson', 'cox', 'howard', 'ward', 'torres', 
        'peterson', 'gray', 'ramirez', 'james', 'watson', 'brooks', 'kelly', 'sanders', 'price', 
        'bennett', 'barnes', 'ross', 'henderson', 'coleman', 'jenkins', 'perry', 'powell', 'long', 
        'patterson', 'hughes', 'flores', 'washington', 'butler', 'simmons', 'foster', 'gonzales', 
        'bryant', 'alexander', 'russell', 'griffin', 'diaz', 'hayes', 'ping', 'pong', 'click', 'zap', 
        'fizz', 'buzz', 'whiz', 'bang', 'crash', 'smash', 'boom', 'pop', 'snap', 'crack', 'punch', 'kick'
    ]
    
    while True:
        part1, part2 = random.sample(login_words, 2)
        login_base = part1 + part2
        
        login = leet_speak(login_base, probability=0.4)
        
        digit_count = sum(c.isdigit() for c in login)
        
        if digit_count == 0:
            num_digits = random.randint(1, 3)
            num_str = "".join(random.choices("0123456789", k=num_digits))
            if random.choice([True, False]):
                login = part1 + num_str + part2
            else:
                login = login + num_str
            digit_count = sum(c.isdigit() for c in login)
            
        if digit_count > 3:
            continue
            
        if 8 <= len(login) <= 16:
            break

    # Пароль: 8-16 символов, заглавные, строчные, спецсимвол
    pass_words = [
        'Strong', 'Stone', 'Wall', 'Base', 'Core', 'Vibe', 'Code', 'Epic', 'Mega', 'Star', 
        'Wolf', 'Bear', 'Lion', 'Hawk', 'Moon', 'Sun', 'Night', 'Day', 'King', 'Queen', 'Gold', 'Iron',
        'Shield', 'Sword', 'Blade', 'Arrow', 'Bow', 'Spear', 'Lance', 'Axe', 'Hammer', 'Mace',
        'Crown', 'Throne', 'Castle', 'Tower', 'Keep', 'Fort', 'Camp', 'Tent', 'Fire', 'Water',
        'Earth', 'Wind', 'Light', 'Dark', 'Shadow', 'Ghost', 'Spirit', 'Soul', 'Mind', 'Heart',
        'Blood', 'Bone', 'Flesh', 'Skin', 'Scale', 'Feather', 'Fur', 'Hair', 'Claw', 'Tooth',
        'River', 'Ocean', 'Forest', 'Mountain', 'Desert', 'Island', 'Planet', 'Galaxy', 'Universe',
        'Alpha', 'Omega', 'Delta', 'Sigma', 'Prime', 'Apex', 'Zenith', 'Nexus', 'Vertex', 'Matrix',
        'Cyber', 'Neon', 'Nova', 'Aero', 'Aqua', 'Terra', 'Pyro', 'Cryo', 'Electro', 'Chrono',
        'Magic', 'Spell', 'Charm', 'Rune', 'Glyph', 'Sigil', 'Symbol', 'Sign', 'Mark', 'Seal',
        'Secret', 'Hidden', 'Lost', 'Found', 'Wild', 'Tame', 'Free', 'Bound', 'Fast', 'Slow',
        'Quick', 'Swift', 'Brisk', 'Rapid', 'Hasty', 'Fleet', 'Paced', 'Time', 'Hour',
        'Crystal', 'Diamond', 'Ruby', 'Sapphire', 'Emerald', 'Topaz', 'Opal', 'Pearl', 'Quartz',
        'Tiger', 'Fox', 'Lynx', 'Raven', 'Crow', 'Eagle', 'Falcon', 'Snake', 'Viper', 'Cobra', 
        'Shark', 'Whale', 'Dolphin', 'Panther', 'Leopard', 'Jaguar', 'Puma', 'Cougar', 'Cheetah',
        'Book', 'Table', 'Chair', 'Door', 'Window', 'House', 'Home', 'Roof', 'Floor', 'Room', 
        'Bed', 'Desk', 'Lamp', 'Clock', 'Watch', 'Phone', 'Screen', 'Glass', 'Cup', 'Plate', 
        'Bowl', 'Fork', 'Spoon', 'Knife', 'Bell', 'Ring', 'Coin', 'Bill', 'Card', 'Ticket', 
        'Paper', 'Pen', 'Pencil', 'Ink', 'Paint', 'Brush', 'Color', 'Shape', 'Form', 'Size', 
        'Line', 'Dot', 'Love', 'Hate', 'Fear', 'Hope', 'Joy', 'Pain', 'Truth', 'Lies', 'Idea', 
        'Thought', 'Dream', 'Vision', 'Goal', 'Plan', 'Rule', 'Law', 'Right', 'Wrong', 'Good', 
        'Bad', 'Best', 'Worst', 'True', 'Fake', 'Real', 'Fair', 'Just', 'Brave', 'Proud', 
        'Weak', 'Smart', 'Dumb', 'Wise', 'Fool', 'Rich', 'Poor', 'High', 'Low', 'Deep', 'Wide', 
        'Long', 'Short', 'Big', 'Small', 'Fat', 'Thin', 'Thick', 'Hard', 'Soft', 'Red', 'Blue', 
        'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Brown', 'Black', 'White', 'Gray', 'Cyan', 
        'Lime', 'Teal', 'Navy', 'Run', 'Walk', 'Jump', 'Fly', 'Swim', 'Dive', 'Fall', 'Rise', 
        'Stand', 'Sit', 'Lay', 'Sleep', 'Wake', 'Eat', 'Drink', 'Talk', 'Speak', 'Listen', 'Hear', 
        'See', 'Look', 'Touch', 'Feel', 'Taste', 'Smell', 'Give', 'Take', 'Have', 'Hold', 'Keep', 
        'Make', 'Work', 'Play', 'Win', 'Lose', 'Fight', 'Guard', 'Save', 'Kill', 'Heal', 'Help',
        'Smith', 'Jones', 'Miller', 'Davis', 'Garcia', 'Brown', 'Wilson', 'Moore', 'Taylor', 
        'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Robinson', 
        'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 
        'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez'
    ]
    
    while True:
        part1, part2 = random.sample(pass_words, 2)
        part2 = part2.lower()
        
        spec = random.choice(['!', '@'])
        num_str = str(random.randint(10, 99))
        
        # Собираем слова, спецсимвол и число в случайном порядке
        components = [part1, part2]
        # Вставляем спецсимвол (3 возможных места: перед словами, между, после)
        components.insert(random.randint(0, 2), spec)
        # Вставляем число (4 возможных места: с краев или внутри)
        components.insert(random.randint(0, 3), num_str)
        
        base = "".join(components)
            
        password = leet_speak(base, probability=0.7)
        
        if 8 <= len(password) <= 16:
            break
            
    # Пин-код - 4 уникальные цифры (без повторений)
    pin = "".join(random.sample("0123456789", 4))
    
    return f"{login}\n{password}\n{pin}"

def generate_outlook_email(first_name, last_name, dob_string):
    """
    Генерирует 'человечный' email-адрес на домене @outlook.com.
    Использует Имя, Фамилию и Дату рождения (формат MM/DD/YYYY или DD/MM/YYYY).
    """
    # Очищаем входные данные от пробелов и приводим к нижнему регистру
    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()
    
    # Извлекаем год и день/месяц из строки с датой рождения
    try:
        parts = dob_string.split('/')
        if len(parts) >= 3:
            year = parts[2][:4]  # Последняя часть обычно год
            short_year = year[-2:] if len(year) == 4 else year # двузначный год
            day_or_month = parts[0][:2]  # Первую часть берем как число
        else:
            year = "1990"
            short_year = "90"
            day_or_month = "01"
    except Exception:
        year = "1990"
        short_year = "90"
        day_or_month = "01"
        
    # Извлечение случайных сокращений (3-5 букв) для большей уникальности
    short_name = first_name[:random.randint(3, 5)] if len(first_name) >= 3 else first_name
    short_last = last_name[:random.randint(3, 5)] if len(last_name) >= 3 else last_name
    first_letter = first_name[0] if first_name else ''
    last_letter = last_name[0] if last_name else ''

    # Выбираем случайную цифру от 1 до 99 (с ведущим нулем, например '05', '42', '99') для максимальной уникальности
    rand_num = f"{random.randint(1, 99):02d}"

    # Огромный набор уникальных "человечных" слов (более 100 вариантов)
    random_words = [
        'sky', 'star', 'pro', 'guy', 'cool', 'ok', 'win', 'best', 'top', 'fly', 'one', 'mail', 'online', 'web', 'box',
        'hub', 'net', 'now', 'app', 'base', 'zone', 'max', 'mix', 'art', 'biz', 'dev', 'run', 'go', 'up', 'new', 'hot',
        'day', 'sun', 'moon', 'sea', 'tech', 'lab', 'link', 'way', 'key', 'vip', 'fox', 'bro', 'man', 'boy', 'kid',
        'joy', 'fun', 'fan', 'play', 'live', 'life', 'real', 'true', 'good', 'nice', 'fast', 'smart', 'guru', 'hero',
        'boss', 'king', 'epic', 'mega', 'giga', 'mini', 'micro', 'nano', 'beta', 'alpha', 'omega', 'prime', 'core',
        'main', 'root', 'flow', 'wave', 'wind', 'fire', 'ice', 'storm', 'rock', 'stone', 'wood', 'gold', 'silver',
        'iron', 'steel', 'code', 'data', 'byte', 'bit', 'pixel', 'cloud', 'host', 'site', 'page', 'blog', 'news',
        'post', 'note', 'book', 'word', 'text', 'font', 'type', 'vibe', 'gear', 'mode', 'work', 'job', 'team', 'crew'
    ]
    
    def get_name():
        return leet_speak(random.choice([first_name, short_name]))
        
    def get_last():
        return leet_speak(random.choice([last_name, short_last]))
        
    # Вспомогательная функция для выбора "цифровой части"
    def get_num():
        return random.choice([day_or_month, short_year, year, rand_num])
    
    # Паттерн 1: (Имя или короткое имя) + (Фамилия или короткая) + слово + цифры
    # Пример: r0bertbrycefly07, robbryc3base73
    def pattern1():
        word = random.choice(random_words)
        return f"{get_name()}{get_last()}{word}{get_num()}"
        
    # Паттерн 2: (Имя или короткое) + разделитель + (Фамилия или короткая) + разделитель + слово + цифры
    # Пример: r0b.bryc3.pro12, robert-8ry.net73
    def pattern2():
        sep = random.choice(['.', '-', '_'])
        word = random.choice(random_words)
        return f"{get_name()}{sep}{get_last()}{sep}{word}{get_num()}"
        
    # Паттерн 3: Первая буква имени + полная фамилия + слово + цифры
    # Пример: rbryc3box1973, rbrycehu807
    def pattern3():
        word = random.choice(random_words)
        return f"{first_letter}{get_last()}{word}{get_num()}"
        
    # Паттерн 4: Фамилия + (Имя или короткое) + слово + цифры (обратный порядок)
    # Пример: bryc3r0bertfly12, brycer0bzone73
    def pattern4():
        word = random.choice(random_words)
        return f"{get_last()}{get_name()}{word}{get_num()}"
        
    # Паттерн 5: Инициалы + фамилия + слово + цифры (или цифры + слово)
    # Пример: rbbryc3max07, rbbryc307app
    def pattern5():
        word = random.choice(random_words)
        num = get_num()
        # Иногда меняем местами слово и число
        if random.choice([True, False]):
            return f"{first_letter}{last_letter}{get_last()}{num}{word}"
        return f"{first_letter}{last_letter}{get_last()}{word}{num}"
        
    # Выбираем случайный паттерн из предложенных
    patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]
    username = random.choice(patterns)()
    
    return f"{username}@outlook.com"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_str = KeyboardButton("📝 Str")
    btn_pinpass = KeyboardButton("🔐 PinPass")
    markup.add(btn_str, btn_pinpass)
    
    # Устанавливаем дефолтное состояние для нового пользователя
    user_modes[message.chat.id] = 'string'
    
    bot.reply_to(message, "Привет! Выбери нужный режим в меню кнопок внизу:\n\n" 
                          "📝 *Str* - разбитие строк и генерация email (@outlook.com)\n"
                          "🔐 *PinPass* - генерация независимых Login, Password и PIN", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def process_text(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    # Переключение режимов
    if text == "📝 Str":
        user_modes[chat_id] = 'string'
        bot.reply_to(message, "Режим **Str** активирован. Жду строки для обработки!", parse_mode="Markdown")
        return
    elif text == "🔐 PinPass":
        user_modes[chat_id] = 'pinpass'
        bot.reply_to(message, f"Режим **PinPass** активирован.\n\n{generate_pinpass()}", parse_mode="Markdown")
        return
        
    # Получаем текущий режим пользователя
    mode = user_modes.get(chat_id, 'string')
    
    if mode == 'pinpass':
        # В режиме PinPass выдаем случайную генерацию на любое сообщение без парсинга
        bot.reply_to(message, generate_pinpass())
        return
        
    # Ниже идет логика только для режима String
    lines = [line.replace('"', '').strip() for line in message.text.split('\n')]
    response = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue
            
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 9:
                f0, f1, f2, f3, f4, f5, f6, f7, f8 = parts[:9]
                
                # Ищем следующую непустую строку для данных из второй линии (DLS)
                infodls = ""
                j = i + 1
                while j < len(lines) and not lines[j]:
                    j += 1
                
                if j < len(lines) and '|' not in lines[j] and ':' not in lines[j]:
                    tokens = lines[j].split()
                    if len(tokens) >= 2:
                        infodls = f"{tokens[-2]} {tokens[-1]}"
                    else:
                        infodls = lines[j]
                    i = j # Consume that line
                    
                email = generate_outlook_email(f2, f4, f1)
                formatted_line = (
                    f"{f2}|{f3}|{f4}|\n"
                    f"{f5}|{f6}|{f7}|{f8}\n"
                    f"{f1}|\n"
                    f"{f0}|"
                )
                if infodls:
                    formatted_line += f"\n{infodls}"
                formatted_line += f"\n{email}"
                
                response.append(formatted_line)
            else:
                response.append(f"Строка с '|' не соответствует формату (нужно минимум 9 элементов):\n{line}")
            i += 1
            continue
            
        parts = line.split(':')
        
        # Если в строке достаточно элементов (старый String-стиль с двоеточиями)
        if len(parts) >= 10:
            email = generate_outlook_email(parts[0], parts[1], parts[7])
            formatted_line = (
                f"{parts[0]}:{parts[1]}:\n"
                f"{parts[2]}:{parts[3]}:{parts[4]}:{parts[5]}:\n"
                f"{parts[6]}:\n"
                f"{parts[7]}:\n"
                f"{parts[8]}:{parts[9]}"
            )
            if len(parts) > 10:
                formatted_line += ":" + ":".join(parts[10:])
                
            formatted_line += f"\n{email}"
            response.append(formatted_line)
        else:
            # Если строка не подходит по формату, предупреждаем
            response.append(f"Строка не соответствует ожидаемому формату:\n{line}")
            
        i += 1
            
    # Отправляем ответ, разделяя блоки одной пустой строкой
    if response:
        result_text = "\n\n".join(response)
        
        # У Telegram есть лимит на длину сообщения (4096 символов). Разделяем если превышает.
        if len(result_text) > 4096:
            for x in range(0, len(result_text), 4096):
                bot.reply_to(message, result_text[x:x+4096])
        else:
            bot.reply_to(message, result_text)

if __name__ == '__main__':
    print("Бот успешно запущен и готов к работе...")
    try:
        # Устанавливаем кнопку меню команд рядом с полем ввода
        from telebot.types import BotCommand
        bot.set_my_commands([
            BotCommand("start", "Главное меню / Перезапуск")
        ])
        
        # Запускаем бота в бесконечном цикле (режим polling)
        bot.infinity_polling()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
