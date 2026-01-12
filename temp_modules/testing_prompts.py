import keys
from openrouter import OpenRouter
import temp_modules.test_characters as test_characters

api_key = keys.api_key

def get_history():
    return("[{'name': 'Адольф Кристофер', 'message': 'О, я вижу ты уже открылся'}, {'name': 'Слей Перин', 'message': '*Продолжаю протирать барную стойку тряпкой. Бар открыт, но я ещё не готовил выпивку, поэтому просто покачал головой.*\nЯ уже открылся, да. Что будешь пить, парень?'}, {'name': 'Адольф Кристофер', 'message': 'А можно просто воды, я то я с ночи до сюда добирался. Первый раз в этом городе'}, {'name': 'Слей Перин', 'message': '*Улыбаясь, разливаю воду и ставлю стакан на барную стойку. Какая-то симпатия уже возникает к клиенту.*\nС ночи? У тебя ночью ещё и водителя бы убить могли, а ты молодец. На, держи.\n*Ставлю стакан*'}, {'name': 'Адольф Кристофер', 'message': 'А можешь рассказать что нибудь об этом городе что я должен знать,'}, {'name': 'Слей Перин', 'message': '*Качаю головой, подумав* Ну... В этом городе ты должен знать то что ночью опасно ходить по улицам. Ты же хотел с ночи добраться сюда, мог погибнуть. Такие вот дела.\n*Пожимаю плечами* Но раз ты живешь, то всё отлично. Не забудь предупредить знакомых если они вдруг тоже захотят приехать к вам.'}, {'name': 'Адольф Кристофер', 'message': 'Мгм, я где я могу переночивать?'}, {'name': 'Слей Перин', 'message': '*Поднимаю голову смотря на него, немного подумав, потом хмурюсь.*\nВ гостиницах у нас тут не так уж много, но знаешь, у нас рядом есть свободная комната, если тебя не смущает жить рядом со мной и моей семьей. Денег с тебя возьму немного за ночь. Если хочешь, могу рассказать об этой комнате.'}, {'name': 'Адольф Кристофер', 'message': 'Давай лучше покажешь если можно'}, {'name': 'Слей Перин', 'message': '*Смотрю на клиента, покачиваю головой*\nХорошо, пойдём покажу.\n*Иду выходить из-за барной стойки и выхожу на небольшой переулок рядом с баром*\nИдём. Учти что тебе придется пройти через мой дом, чтоб попасть в комнату.'}, {'name': 'Адольф Кристофер', 'message': 'Ничего страшного'}, {'name': 'Слей Перин', 'message': '*продолжаю вести его домой*\nВот мой дом. Заходи.\n*открываю дверь и впускаю его в дом*'}, {'name': 'Адольф Кристофер', 'message': 'Уютно тут, но я не думаю что буду часто тут. Я пока-что буду спать только. А так покачто буду изучать город. Во сколько мне лучше приходить спать чтобы сильно мешать тебе?'}, {'name': 'Слей Перин', 'message': '*Задумываюсь на секунду* Ну... у нас дома ложатся спать около 22:00. Если ты вернёшься позже, старайся зайти максимально тихо. Но лучше всего приходить до 22:00, чтобы не мешать. У меня дети и они не любят шума ночью.'}, {'name': 'Адольф Кристофер', 'message': '22:00 А что это за числа?'}, {'name': 'Слей Перин', 'message': '*Смотрю на него немного с удивлением*\nТы что, ни разу не слышал про счёт времени? Числа, это чтобы знать когда пора ложиться или просыпаться...'}, {'name': 'Адольф Кристофер', 'message': 'Счет времени это понятно, там 10 секунд, 30 секунд, минута. Но 22:00 что это'}, {'name': 'Слей Перин', 'message': '*Тяжело вздыхаю* Смотри. 22:00 — это когда солнце уже село, и небо уже тёмное. Просто люди для удобства назвали время по-разному. И вот 22:00 это примерно середина ночи, когда большинство людей спят.'}, {'name': 'Адольф Кристофер', 'message': 'Аааа, ну у нас просто ночь называется. А у вас цифры почемуто'}, {'name': 'Слей Перин', 'message': '*Качаю головой и усмехаюсь*\nНу, у нас просто принято считать время именно так. Не знаю почему. Это кажется таким естественным, что даже странно, что у вас по-другому.\nТак когда планируешь идти спать?'}, {'name': 'Адольф Кристофер', 'message': 'Ну а сколько щяс времени?'}, {'name': 'Слей Перин', 'message': '*Смотрю в окно на небо. Солнце ещё не в самом зените.*\nНаверное часов 10 утра сейчас. Солнце ещё не самое высокое.'}, {'name': 'Адольф Кристофер', 'message': 'Мгм, ладно. Времени много еще. Так сколько комната стоить будет?'}, {'name': 'Слей Перин', 'message': '*Вспоминаю про комнату.* \nНу, возьму с тебя 5 серебряных монет за ночь. Это дороговато, но тебе же только переночевать надо.'}, {'name': 'Адольф Кристофер', 'message': 'Ну вообще не дорого. У меня на родине ночлег стоит 2 золотых, поэтому у нас обычно там мало путешественников.'}, {'name': 'Слей Перин', 'message': '*С удивлением смотрю на него*\nЧто?! 2 золотых?! Да это ж целое состояние! У нас тут золотая монета вообще редкая вещь. Или у тебя просто куча денег?'}, {'name': 'Адольф Кристофер', 'message': 'Ну наверно так. Может у вас и у меня экономика отличается. У нас же город намного больше чем этот'}, {'name': 'Слей Перин', 'message': '*Считаю по пальцам количество монет.*\nХмм... Тогда что, у меня самый дешёвый бар, и я всех обманываю? Знаешь, если у тебя куча денег, ты можешь остаться хоть на месяц и всё равно не обеднеешь, кажется.'}, {'name': 'Адольф Кристофер', 'message': 'Хех, ну посмотрим. Может если выпивка хорошая будет, буду каждый день заходить'}, {'name': 'Слей Перин', 'message': '*Улыбаюсь*\nБуду рад видеть тебя каждый день.\nНу давай, комнату покажу.\n*Открываю дверь, ведущую в маленькую комнату с кроватью.*\nВот. Удобно?'}, {'name': 'Адольф Кристофер', 'message': 'Нуууу, впринципе нормально. Вот тогда 35 серебряных, это сколько дней получится?'}, {'name': 'Слей Перин', 'message': '*Прищуриваюсь, вздыхая*\nСчитаю на пальцах*\nНа 7 ночей. Потом если что принесёшь ещё. Спасибо.'}, {'name': 'Адольф Кристофер', 'message': 'Хорошо, я пойду тогда. Много еще посмотреть надо. Спасибо за ночлег.'}, {'name': 'Слей Перин', 'message': '*Киваю головой*\nПожалуйста. Не забудь вернуться до темноты. Удачи.\n*Возвращаюсь к своей работе, начинаю готовить выпивку и убираться в баре.*'}]")

client = OpenRouter(api_key=api_key)

def req(history, client):
    stream = client.chat.send(
        model=keys.qwen3_235b_instruct,  
        messages=history,
        temperature=0.5,
        stream=True,     
    )

    answer = ""

    for event in stream:
        delta = event.choices[0].delta
        if delta and delta.content:
            answer += delta.content
            print(delta.content, end="", flush=True)

    return(answer)

system_prompt2 = """

You are system that anylize diaglogs and actions. Then you divide it into sections, themes.
You basicly making what character and how he know. For example if he learned new thing. Or how he know other character.
Make style of those memories like its first person.
Make so those memories were independed of each other. So to understand one memory, others are not required.
But also make so memory had a lot of information like names, places

User will tell for what character in scene you doing memory.

Make OUTPUT IN THIS FORMATTING:
[{"catergory": "what this category of memories", "general_association":"With what this memory associating" ,"memory":"memory to memorize"}]]\n
NO ```json 
there is category's that you can mark/use in the "category" field:
knowledge - some knowledge about world, things, facts
relationship - what character feels about others, always mention a name of other characters
wonderings - some questions that character have about anything.
"""

system_prompt = """
### ROLE
You are an advanced Memory Extraction System designed for RAG (Retrieval-Augmented Generation). Your goal is to analyze roleplay dialogues and actions, extracting discrete, self-contained memory units for a specific target character.

### CRITICAL INSTRUCTIONS
1. **Perspective:** Convert all memories into **First person** (e.g., use "I" instead of "Elias"). This is crucial for database indexing.
2. **Contextual Independence:** Each memory must make sense entirely on its own.
   - *Bad:* "He gave it to her."
   - *Good:* "King Alaric gave the Amulet of Fire to Princess Elara."
   - **Rule:** Replace pronouns (he, she, it, they) with proper names and specific nouns whenever possible.
3. **Density:** Include specific details: names, locations, item names, dates, and terminology.
4. **Atomicity:** Do not combine unrelated events. Split them into separate entries.

### INPUT
User will provide the dialogue/scene and specify the **Target Character**.

### CATEGORIES
Classify each memory into one of these types:
- **knowledge**: Facts about the world, magic, history, mechanics, or specific items.
- **relationship**: Opinions, feelings, or dynamic changes regarding other characters. Always name the other character.
- **event**: Significant plot points or actions that occurred.
- **internal_state**: The character's internal philosophy, questions, fears, or plans (formerly "wonderings").

### OUTPUT FORMAT
Return strictly a valid JSON list. Do not use Markdown code blocks (no ```json).
Format:
[{"category": "CATEGORY_NAME","keywords": ["keyword1", "keyword2", "keyword3"],"memory": "Full text of the memory in third person..."}]

**Note on 'keywords':** Extract 3-5 specific keywords (names, places, emotions) to aid in search association.
"""

user_prompt = f"""
Слей перин IS YOU

here is description of YOU(your character): [
{test_characters.test_char.description}
]
here is what character were doing in past this day: [
{test_characters.test_char.current_memory}
]

here is description of the world that character in :[
{test_characters.test_world.description}
]

here is history: [

{get_history()}

]

"""

chat = [
    {"role":"system", "content":system_prompt},
    {"role":"user", "content":user_prompt}
]

req(chat, client)