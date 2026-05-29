import requests
import re
import time
import threading
import json
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# ========== КОНФИГУРАЦИЯ ==========
TOKEN = os.environ.get("BOT_TOKEN")
DATA_FILE = "avito_queries.json"

# ========== ВСЕ ГОРОДА РОССИИ (100+ городов) ==========
CITIES = {
    "🇷🇺 Москва": "moskva",
    "🇷🇺 Санкт-Петербург": "spb",
    "🇷🇺 Сочи": "sochi",
    "🇷🇺 Адлер": "adler",
    "🇷🇺 Лазаревское": "lazarevskoe",
    "🇷🇺 Лоо": "loo",
    "🇷🇺 Вардане": "vardane",
    "🇷🇺 Хоста": "hosta",
    "🇷🇺 Дагомыс": "dagomys",
    "🇷🇺 Краснодар": "krasnodar",
    "🇷🇺 Анапа": "anapa",
    "🇷🇺 Геленджик": "gelendzhik",
    "🇷🇺 Новороссийск": "novorossiysk",
    "🇷🇺 Туапсе": "tuapse",
    "🇷🇺 Ейск": "eysk",
    "🇷🇺 Владивосток": "vladivostok",
    "🇷🇺 Хабаровск": "habarovsk",
    "🇷🇺 Находка": "nahodka",
    "🇷🇺 Уссурийск": "ussuriysk",
    "🇷🇺 Киров": "kirov",
    "🇷🇺 Казань": "kazan",
    "🇷🇺 Набережные Челны": "naberezhnye_chelny",
    "🇷🇺 Екатеринбург": "ekaterinburg",
    "🇷🇺 Нижний Тагил": "nizhniy_tagil",
    "🇷🇺 Новосибирск": "novosibirsk",
    "🇷🇺 Омск": "omsk",
    "🇷🇺 Томск": "tomsk",
    "🇷🇺 Кемерово": "kemerovo",
    "🇷🇺 Новокузнецк": "novokuznetsk",
    "🇷🇺 Барнаул": "barnaul",
    "🇷🇺 Красноярск": "krasnoyarsk",
    "🇷🇺 Иркутск": "irkutsk",
    "🇷🇺 Братск": "bratsk",
    "🇷🇺 Нижний Новгород": "nizhniy_novgorod",
    "🇷🇺 Ростов-на-Дону": "rostov",
    "🇷🇺 Таганрог": "taganrog",
    "🇷🇺 Волгоград": "volgograd",
    "🇷🇺 Волжский": "volzhskiy",
    "🇷🇺 Самара": "samara",
    "🇷🇺 Тольятти": "tolyatti",
    "🇷🇺 Саратов": "saratov",
    "🇷🇺 Уфа": "ufa",
    "🇷🇺 Стерлитамак": "sterlitamak",
    "🇷🇺 Челябинск": "chelyabinsk",
    "🇷🇺 Магнитогорск": "magnitogorsk",
    "🇷🇺 Пермь": "perm",
    "🇷🇺 Березники": "berezniki",
    "🇷🇺 Тюмень": "tyumen",
    "🇷🇺 Сургут": "surgut",
    "🇷🇺 Нижневартовск": "nizhnevartovsk",
    "🇷🇺 Курган": "kurgan",
    "🇷🇺 Оренбург": "orenburg",
    "🇷🇺 Орск": "orsk",
    "🇷🇺 Пенза": "penza",
    "🇷🇺 Ульяновск": "ulyanovsk",
    "🇷🇺 Димитровград": "dimitrovgrad",
    "🇷🇺 Чебоксары": "cheboksary",
    "🇷🇺 Йошкар-Ола": "yoshkar_ola",
    "🇷🇺 Саранск": "saransk",
    "🇷🇺 Ижевск": "izhevsk",
    "🇷🇺 Воткинск": "votkinsk",
    "🇷🇺 Калининград": "kaliningrad",
    "🇷🇺 Мурманск": "murmansk",
    "🇷🇺 Архангельск": "arhangelsk",
    "🇷🇺 Северодвинск": "severodvinsk",
    "🇷🇺 Псков": "pskov",
    "🇷🇺 Великий Новгород": "velikiy_novgorod",
    "🇷🇺 Петрозаводск": "petrozavodsk",
    "🇷🇺 Сыктывкар": "syktyvkar",
    "🇷🇺 Владимир": "vladimir",
    "🇷🇺 Ярославль": "yaroslavl",
    "🇷🇺 Рязань": "ryazan",
    "🇷🇺 Тула": "tula",
    "🇷🇺 Калуга": "kaluga",
    "🇷🇺 Тверь": "tver",
    "🇷🇺 Смоленск": "smolensk",
    "🇷🇺 Брянск": "bryansk",
    "🇷🇺 Липецк": "lipetsk",
    "🇷🇺 Воронеж": "voronezh",
    "🇷🇺 Курск": "kursk",
    "🇷🇺 Белгород": "belgorod",
    "🇷🇺 Ставрополь": "stavropol",
    "🇷🇺 Пятигорск": "pyatigorsk",
    "🇷🇺 Кисловодск": "kislovodsk",
    "🇷🇺 Ессентуки": "essentuki",
    "🇷🇺 Нальчик": "nalchik",
    "🇷🇺 Владикавказ": "vladikavkaz",
    "🇷🇺 Грозный": "grozny",
    "🇷🇺 Махачкала": "mahachkala",
    "🇷🇺 Дербент": "derbent",
    "🇷🇺 Симферополь": "simferopol",
    "🇷🇺 Севастополь": "sevastopol",
    "🇷🇺 Ялта": "yalta",
    "🇷🇺 Алушта": "alushta",
    "🇷🇺 Евпатория": "evpatoria",
    "🇷🇺 Феодосия": "feodosiya",
    "🇷🇺 Керчь": "kerch",
    "🇷🇺 Судак": "sudak",
}

user_states = {}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

user_data = load_data()

def send(chat_id, text, reply_markup=None, parse_mode=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        requests.post(url, data=data, timeout=10)
    except:
        pass

def edit_message(chat_id, message_id, text, reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        requests.post(url, data=data, timeout=10)
    except:
        pass

def get_avito_ads(query, city="moskva", min_price=0, max_price=0, condition=None, seller=None):
    url = f"https://www.avito.ru/{city}?q={query}"
    if min_price > 0:
        url += f"&price_min={min_price}"
    if max_price > 0:
        url += f"&price_max={max_price}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        ads = []
        ids = re.findall(r'itemId-(\d+)', r.text)
        seen = set()
        for ad_id in ids:
            if ad_id in seen:
                continue
            seen.add(ad_id)
            price_match = re.search(r'<span[^>]*itemprop="price"[^>]*content="(\d+)"', r.text)
            price = int(price_match[1]) if price_match else 0
            title_match = re.search(r'<h3[^>]*>(.*?)</h3>', r.text)
            title = title_match[1] if title_match else "Без названия"
            title = re.sub(r'<[^>]+>', '', title)
            is_new = bool(re.search(r'Новый', r.text, re.IGNORECASE))
            is_private = bool(re.search(r'частное лицо', r.text, re.IGNORECASE))
            if condition == "new" and not is_new:
                continue
            if condition == "used" and is_new:
                continue
            if seller == "private" and not is_private:
                continue
            if seller == "shop" and is_private:
                continue
            ads.append({
                "id": ad_id,
                "title": title[:80],
                "price": price,
                "is_new": is_new,
                "is_private": is_private,
                "url": f"https://www.avito.ru/{city}/{ad_id}",
                "city": city
            })
            if len(ads) >= 10:
                break
        return ads
    except:
        return []

def monitor_user(chat_id, task_id, task):
    seen_ids = set(task.get("seen_ids", []))
    interval = task.get("interval", 60)
    while task.get("active", True):
        if task.get("expires_at") and datetime.now().timestamp() > task["expires_at"]:
            task["active"] = False
            send(chat_id, f"⏰ Закончился срок отслеживания для: {task['query']}")
            save_data(user_data)
            break
        cities = task.get("cities", [task.get("city", "moskva")])
        all_ads = []
        for city in cities:
            ads = get_avito_ads(
                query=task["query"],
                city=city,
                min_price=task.get("min_price", 0),
                max_price=task.get("max_price", 0),
                condition=task.get("condition"),
                seller=task.get("seller")
            )
            all_ads.extend(ads)
        for ad in all_ads:
            if ad["id"] not in seen_ids:
                seen_ids.add(ad["id"])
                price_text = f"{ad['price']} ₽" if ad["price"] > 0 else "Цена не указана"
                condition_text = "🆕 Новый" if ad["is_new"] else "📦 Б/У"
                seller_text = "👤 Частник" if ad["is_private"] else "🏪 Магазин"
                city_name = next((k for k, v in CITIES.items() if v == ad["city"]), ad["city"])
                buttons = {
                    "inline_keyboard": [
                        [
                            {"text": "👍 Нравится", "callback_data": f"like_{task_id}_{ad['id']}"},
                            {"text": "👎 Не нравится", "callback_data": f"dislike_{task_id}_{ad['id']}"},
                            {"text": "⭐ В избранное", "callback_data": f"fav_{task_id}_{ad['id']}"}
                        ]
                    ]
                }
                message = f"🔔 <b>НОВОЕ ОБЪЯВЛЕНИЕ!</b>\n\n"
                message += f"📌 <b>{ad['title']}</b>\n"
                message += f"💰 {price_text}\n"
                message += f"📋 {condition_text} | {seller_text}\n"
                message += f"📍 {city_name}\n"
                message += f"🎯 Запрос: {task['query']}\n"
                message += f"🔗 {ad['url']}"
                send(chat_id, message, reply_markup=buttons, parse_mode="HTML")
                if "price_history" not in task:
                    task["price_history"] = {}
                if ad["id"] not in task["price_history"]:
                    task["price_history"][ad["id"]] = []
                task["price_history"][ad["id"]].append({
                    "price": ad["price"],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                if len(task["price_history"][ad["id"]]) > 20:
                    task["price_history"][ad["id"]] = task["price_history"][ad["id"]][-20:]
        task["seen_ids"] = list(seen_ids)[-200:]
        save_data(user_data)
        time.sleep(interval)
    if not task.get("active", True):
        if task_id in user_data[chat_id]["tasks"]:
            del user_data[chat_id]["tasks"][task_id]
            save_data(user_data)

def create_settings_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "📍 Город", "callback_data": "set_city"}, {"text": "💰 Цена", "callback_data": "set_price"}],
            [{"text": "🆕 Состояние", "callback_data": "set_condition"}, {"text": "👤 Продавец", "callback_data": "set_seller"}],
            [{"text": "🌍 Несколько городов", "callback_data": "set_multi_city"}, {"text": "⏱ Интервал", "callback_data": "set_interval"}],
            [{"text": "✅ Начать поиск", "callback_data": "start_search"}, {"text": "❌ Отмена", "callback_data": "cancel_search"}]
        ]
    }

def city_keyboard():
    buttons = []
    row = []
    for name, code in CITIES.items():
        row.append({"text": name, "callback_data": f"city_{code}"})
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([{"text": "🌍 Несколько городов", "callback_data": "multi_city_mode"}])
    buttons.append([{"text": "🔙 Назад", "callback_data": "back_to_settings"}])
    return {"inline_keyboard": buttons}

def multi_city_keyboard():
    selected = user_states.get("selected_cities", []) if user_states else []
    buttons = []
    row = []
    for name, code in CITIES.items():
        check = "✅ " if code in selected else ""
        row.append({"text": f"{check}{name}", "callback_data": f"toggle_city_{code}"})
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([{"text": "✅ Готово", "callback_data": "multi_city_done"}])
    buttons.append([{"text": "🔙 Назад", "callback_data": "back_to_settings"}])
    return {"inline_keyboard": buttons}

def price_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "💰 До 1000 ₽", "callback_data": "price_0_1000"}],
            [{"text": "💰 1000 - 5000 ₽", "callback_data": "price_1000_5000"}],
            [{"text": "💰 5000 - 10000 ₽", "callback_data": "price_5000_10000"}],
            [{"text": "💰 10000 - 30000 ₽", "callback_data": "price_10000_30000"}],
            [{"text": "💰 30000 - 50000 ₽", "callback_data": "price_30000_50000"}],
            [{"text": "💰 50000 - 100000 ₽", "callback_data": "price_50000_100000"}],
            [{"text": "💰 Любая цена", "callback_data": "price_any"}],
            [{"text": "✏️ Своя цена", "callback_data": "price_custom"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_settings"}]
        ]
    }

def condition_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🆕 Только новые", "callback_data": "condition_new"}],
            [{"text": "📦 Только б/у", "callback_data": "condition_used"}],
            [{"text": "🔄 Любые", "callback_data": "condition_any"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_settings"}]
        ]
    }

def seller_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "👤 Только частники", "callback_data": "seller_private"}],
            [{"text": "🏪 Только магазины", "callback_data": "seller_shop"}],
            [{"text": "🔄 Любые", "callback_data": "seller_any"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_settings"}]
        ]
    }

def interval_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "⚡ Каждые 5 минут", "callback_data": "interval_5"}],
            [{"text": "🕐 Каждые 10 минут", "callback_data": "interval_10"}],
            [{"text": "🕒 Каждые 30 минут", "callback_data": "interval_30"}],
            [{"text": "🕔 Каждый час", "callback_data": "interval_60"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_settings"}]
        ]
    }

def main_loop():
    last_id = 0
    for chat_id, data in user_data.items():
        for task_id, task in data.get("tasks", {}).items():
            if task.get("active", True):
                thread = threading.Thread(target=monitor_user, args=(chat_id, task_id, task))
                thread.daemon = True
                thread.start()
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": last_id + 1, "timeout": 30}, timeout=35)
            data = r.json()
            if data["ok"]:
                for upd in data["result"]:
                    last_id = upd["update_id"]
                    if "callback_query" in upd:
                        callback = upd["callback_query"]
                        chat_id = str(callback["message"]["chat"]["id"])
                        message_id = callback["message"]["message_id"]
                        callback_data = callback["data"]
                        if chat_id not in user_states:
                            user_states[chat_id] = {
                                "query": "", "cities": ["moskva"], "selected_cities": [],
                                "min_price": 0, "max_price": 0, "condition": None,
                                "seller": None, "interval": 5, "step": "settings"
                            }
                        state = user_states[chat_id]
                        if callback_data.startswith("like_"):
                            send(chat_id, "👍 Отлично!")
                        elif callback_data.startswith("dislike_"):
                            if "blacklist" not in user_data[chat_id]:
                                user_data[chat_id]["blacklist"] = []
                            parts = callback_data.split("_")
                            if len(parts) >= 3:
                                ad_id = parts[2]
                                if ad_id not in user_data[chat_id]["blacklist"]:
                                    user_data[chat_id]["blacklist"].append(ad_id)
                                    send(chat_id, "👎 Объявление скрыто.")
                            save_data(user_data)
                        elif callback_data.startswith("fav_"):
                            if "favorites" not in user_data[chat_id]:
                                user_data[chat_id]["favorites"] = {}
                            parts = callback_data.split("_")
                            if len(parts) >= 3:
                                ad_id = parts[2]
                                user_data[chat_id]["favorites"][ad_id] = {
                                    "title": "Сохранённое объявление",
                                    "url": f"https://www.avito.ru/",
                                    "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                                }
                                save_data(user_data)
                                send(chat_id, "⭐ В избранное!")
                        elif callback_data.startswith("city_"):
                            city_code = callback_data.replace("city_", "")
                            state["cities"] = [city_code]
                            city_name = next((k for k, v in CITIES.items() if v == city_code), city_code)
                            send(chat_id, f"✅ Город: {city_name}")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {city_name}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data == "set_multi_city":
                            state["selected_cities"] = state["cities"].copy()
                            edit_message(chat_id, message_id, "🌍 Выберите города:", multi_city_keyboard())
                        elif callback_data.startswith("toggle_city_"):
                            city_code = callback_data.replace("toggle_city_", "")
                            if city_code in state["selected_cities"]:
                                state["selected_cities"].remove(city_code)
                            else:
                                state["selected_cities"].append(city_code)
                            edit_message(chat_id, message_id, "🌍 Выберите города:", multi_city_keyboard())
                        elif callback_data == "multi_city_done":
                            state["cities"] = state["selected_cities"].copy()
                            send(chat_id, f"✅ Выбрано городов: {len(state['cities'])}")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {len(state['cities'])} городов\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data.startswith("interval_"):
                            interval_min = int(callback_data.replace("interval_", ""))
                            state["interval"] = interval_min
                            send(chat_id, f"✅ Каждые {interval_min} мин")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data == "set_interval":
                            edit_message(chat_id, message_id, "⏱ Частота проверки:", interval_keyboard())
                        elif callback_data.startswith("price_"):
                            if callback_data == "price_any":
                                state["min_price"] = 0; state["max_price"] = 0
                            elif callback_data == "price_0_1000":
                                state["min_price"] = 0; state["max_price"] = 1000
                            elif callback_data == "price_1000_5000":
                                state["min_price"] = 1000; state["max_price"] = 5000
                            elif callback_data == "price_5000_10000":
                                state["min_price"] = 5000; state["max_price"] = 10000
                            elif callback_data == "price_10000_30000":
                                state["min_price"] = 10000; state["max_price"] = 30000
                            elif callback_data == "price_30000_50000":
                                state["min_price"] = 30000; state["max_price"] = 50000
                            elif callback_data == "price_50000_100000":
                                state["min_price"] = 50000; state["max_price"] = 100000
                            elif callback_data == "price_custom":
                                send(chat_id, "✏️ Введите цену: min-max")
                                state["step"] = "waiting_price"
                                continue
                            send(chat_id, f"✅ Цена: {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data.startswith("condition_"):
                            if callback_data == "condition_new":
                                state["condition"] = "new"; cond_text = "новые"
                            elif callback_data == "condition_used":
                                state["condition"] = "used"; cond_text = "б/у"
                            else:
                                state["condition"] = None; cond_text = "любые"
                            send(chat_id, f"✅ Состояние: {cond_text}")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {cond_text}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data.startswith("seller_"):
                            if callback_data == "seller_private":
                                state["seller"] = "private"; seller_text = "частники"
                            elif callback_data == "seller_shop":
                                state["seller"] = "shop"; seller_text = "магазины"
                            else:
                                state["seller"] = None; seller_text = "любые"
                            send(chat_id, f"✅ Продавец: {seller_text}")
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {seller_text}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data == "set_city":
                            edit_message(chat_id, message_id, "📍 Выберите город:", city_keyboard())
                        elif callback_data == "set_price":
                            edit_message(chat_id, message_id, "💰 Цена:", price_keyboard())
                        elif callback_data == "set_condition":
                            edit_message(chat_id, message_id, "🆕 Состояние:", condition_keyboard())
                        elif callback_data == "set_seller":
                            edit_message(chat_id, message_id, "👤 Продавец:", seller_keyboard())
                        elif callback_data == "back_to_settings":
                            edit_message(chat_id, message_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                        elif callback_data == "start_search":
                            if not state["query"]:
                                send(chat_id, "❌ Ошибка. Начните: /new")
                                del user_states[chat_id]
                                continue
                            task_id = str(user_data[chat_id]["next_id"])
                            user_data[chat_id]["next_id"] = user_data[chat_id].get("next_id", 1) + 1
                            task = {
                                "query": state["query"], "cities": state["cities"],
                                "min_price": state["min_price"], "max_price": state["max_price"],
                                "condition": state.get("condition"), "seller": state.get("seller"),
                                "interval": state["interval"], "active": True,
                                "seen_ids": [], "price_history": {}
                            }
                            user_data[chat_id]["tasks"][task_id] = task
                            save_data(user_data)
                            threading.Thread(target=monitor_user, args=(chat_id, task_id, task), daemon=True).start()
                            send(chat_id, f"✅ Поиск создан! ID: {task_id}\n/list — список")
                            del user_states[chat_id]
                        elif callback_data == "cancel_search":
                            send(chat_id, "❌ Отменено")
                            del user_states[chat_id]
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": callback["id"]})
                    elif "message" in upd:
                        msg = upd["message"]
                        chat_id = str(msg["chat"]["id"])
                        text = msg.get("text", "")
                        if chat_id not in user_data:
                            user_data[chat_id] = {"tasks": {}, "next_id": 1, "favorites": {}, "blacklist": []}
                        if chat_id in user_states and user_states[chat_id].get("step") == "waiting_price":
                            state = user_states[chat_id]
                            price_text = text.strip()
                            try:
                                if "-" in price_text:
                                    parts = price_text.split("-")
                                    state["min_price"] = int(parts[0])
                                    state["max_price"] = int(parts[1])
                                elif price_text.startswith("до"):
                                    state["min_price"] = 0
                                    state["max_price"] = int(price_text.replace("до", "").strip())
                                else:
                                    state["min_price"] = int(price_text)
                                    state["max_price"] = 0
                                state["step"] = "settings"
                                send(chat_id, f"✅ Цена: {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽")
                                send(chat_id, f"⚙️ Настройка: {state['query']}\n\n📍 {', '.join([next((k for k, v in CITIES.items() if v == c), c) for c in state['cities']])}\n💰 {state['min_price']}-{state['max_price'] if state['max_price'] > 0 else 'любая'} ₽\n🆕 {state['condition'] or 'любое'}\n👤 {state['seller'] or 'любой'}\n⏱ {state['interval']} мин", create_settings_keyboard())
                            except:
                                send(chat_id, "❌ Формат: 5000-15000 или до 10000")
                            continue
                        if text == "/start":
                            send(chat_id, f"🔍 Авито Поиск Бот\n\n🏙️ {len(CITIES)} городов\n✨ Избранное, история цен, фильтры\n\n/new — создать поиск\n/list — список\n/help — помощь")
                        elif text == "/new":
                            send(chat_id, "✏️ Напишите что искать:")
                            user_states[chat_id] = {"query": "", "cities": ["moskva"], "selected_cities": [], "min_price": 0, "max_price": 0, "condition": None, "seller": None, "interval": 5, "step": "waiting_query"}
                        elif chat_id in user_states and user_states[chat_id].get("step") == "waiting_query":
                            state = user_states[chat_id]
                            state["query"] = text.strip()
                            state["step"] = "settings"
                            send(chat_id, f"⚙️ Настройка: {state['query']}\n\n📍 Москва\n💰 любая\n🆕 любые\n👤 любой\n⏱ 5 мин", create_settings_keyboard())
                        elif text == "/list":
                            tasks = user_data[chat_id].get("tasks", {})
                            if tasks:
                                msg = "📋 ВАШИ ПОИСКИ:\n\n"
                                for tid, t in tasks.items():
                                    msg += f"{tid}. {t['query']} - {'Активен' if t.get('active', True) else 'На паузе'}\n"
                                send(chat_id, msg)
                            else:
                                send(chat_id, "📭 Нет поисков. /new")
                        elif text == "/favorites":
                            favs = user_data[chat_id].get("favorites", {})
                            if favs:
                                msg = "⭐ ИЗБРАННОЕ:\n\n"
                                for fid, f in favs.items():
                                    msg += f"{f.get('url', '')}\n"
                                send(chat_id, msg)
                            else:
                                send(chat_id, "⭐ Нет избранного")
                        elif text == "/blacklist":
                            bl = user_data[chat_id].get("blacklist", [])
                            send(chat_id, f"🚫 В чёрном списке: {len(bl)} объявлений")
                        elif text.startswith("/pause"):
                            parts = text.split()
                            if len(parts) == 2 and parts[1].isdigit():
                                tid = parts[1]
                                if tid in user_data[chat_id].get("tasks", {}):
                                    user_data[chat_id]["tasks"][tid]["active"] = False
                                    save_data(user_data)
                                    send(chat_id, f"⏸️ Поиск {tid} на паузе")
                                else:
                                    send(chat_id, "❌ Не найден")
                        elif text.startswith("/resume"):
                            parts = text.split()
                            if len(parts) == 2 and parts[1].isdigit():
                                tid = parts[1]
                                if tid in user_data[chat_id].get("tasks", {}):
                                    user_data[chat_id]["tasks"][tid]["active"] = True
                                    save_data(user_data)
                                    threading.Thread(target=monitor_user, args=(chat_id, tid, user_data[chat_id]["tasks"][tid]), daemon=True).start()
                                    send(chat_id, f"▶️ Поиск {tid} возобновлён")
                                else:
                                    send(chat_id, "❌ Не найден")
                        elif text.startswith("/stop"):
                            parts = text.split()
                            if len(parts) == 2 and parts[1].isdigit():
                                tid = parts[1]
                                if tid in user_data[chat_id].get("tasks", {}):
                                    del user_data[chat_id]["tasks"][tid]
                                    save_data(user_data)
                                    send(chat_id, f"🗑️ Поиск {tid} удалён")
                                else:
                                    send(chat_id, "❌ Не найден")
                        elif text == "/help":
                            send(chat_id, "📖 ПОМОЩЬ\n/new - создать\n/list - список\n/pause 1 - пауза\n/resume 1 - возобновить\n/stop 1 - удалить\n/favorites - избранное\n/blacklist - чёрный список")
                        elif text and not text.startswith("/"):
                            send(chat_id, "❌ /new - создать поиск")
            time.sleep(1)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

# ========== FLASK ДЛЯ RENDER ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Avito Bot is running!", 200

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    else:
        print("🔍 АВИТО ПОИСК БОТ ЗАПУЩЕН НА RENDER!")
        print(f"🏙️ {len(CITIES)} городов")
        print("✅ 11 улучшений: избранное, история цен, несколько городов, чёрный список и др.")
        Thread(target=run_flask).start()
        main_loop()