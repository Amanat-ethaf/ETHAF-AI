# ==========================================
# ETHAF AI PROFESSIONAL v2.0
# Part 1 - Foundation
# Programmer: Salaar ur Amanat
# ==========================================
import os
import json
import math
from langdetect import detect
from deep_translator import GoogleTranslator
import time
import requests
import wikipedia

wikipedia.set_lang("en")
from pypdf import PdfReader
import datetime
import logging
import os

print(os.listdir("/storage"))

# ==========================
# AI INFORMATION
# ==========================

APP_NAME = "ETHAF AI"
VERSION = "1.0"
OWNER = "Amanat"
# ==========================
# LANGUAGE ENGINE
# ==========================

USER_LANGUAGE = "en"
COUNTRY = "India"

print("=" * 50)
print(APP_NAME)
print("Version :", VERSION)
print("Owner   :", OWNER)
print("Country :", COUNTRY)
print("=" * 50)

# ==========================
# MEMORY
# ==========================
# ==========================
# STORAGE PATHS
# ==========================

LOCAL_MEMORY_FILE = "ai_memory.json"

# Yahan apni pendrive ka path likho
PENDRIVE_MEMORY_FILE = "/storage/76E8-CACF/ai_memory.json"
MEMORY_FILE = "ai_memory.json"

memory = {}
	

if os.path.exists(PENDRIVE_MEMORY_FILE):

    try:
        with open(PENDRIVE_MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

    except:
        memory = {}

elif os.path.exists(LOCAL_MEMORY_FILE):

    try:
        with open(LOCAL_MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

    except:
        memory = {}
        
# ==========================
# SAVE MEMORY
# ==========================

def save_memory():

    # Local Save
    try:
        with open(LOCAL_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Local Save Error:", e)

    # Pendrive Save
    try:
        with open(PENDRIVE_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4, ensure_ascii=False)
    except Exception:
        pass
    try:

        with open(HISTORY_FILE, "w", encoding="utf-8") as h:

            json.dump(history, h, indent=4, ensure_ascii=False)

    except:

        pass
# ==========================
# USER PROFILE
# ==========================

user_profile = {}

HISTORY_FILE = "chat_history.json"
NOTES_FILE = "notes.txt"
# ==========================
# WORKSPACE
# ==========================

WORKSPACE = "ETHAF_WORKSPACE"

if not os.path.exists(WORKSPACE):
    os.makedirs(WORKSPACE)

if os.path.exists(HISTORY_FILE):

    try:

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:

            history = json.load(f)

    except:

        history = []

else:

    history = []

# ==========================
# LEARNING SYSTEM
# ==========================

def load_dataset():

    global memory

    try:
        with open("dataset.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0

        for item in data:

            q = item["question"].strip().lower()
            a = item["answer"].strip()

            memory[q] = a
            count += 1

        save_memory()

        return f"Loaded {count} training examples."

    except Exception as e:

        return f"Dataset Error: {e}"


print(load_dataset())   # ← YAHAN
# ==========================
# LEARNING SYSTEM
# ==========================

#def learn(text):

  #  try:

      #  question, answer = text.split("=", 1)

      #  question = question.strip().lower()

       # answer = answer.strip()

       # memory[question] = answer

     #   save_memory()

     #   return "✅ I learned successfully."

   # except:

        #return "Usage : learn: question = answer"
# ==========================
# DELETE MEMORY
# ==========================

def forget(text):

    text = text.lower().strip()

    if text in memory:

        del memory[text]

        save_memory()

        return "Memory deleted successfully."

    return "Memory not found."
# ==========================
# NOTES MANAGER
# ==========================

def save_note(text):

    with open(NOTES_FILE, "a", encoding="utf-8") as f:

        f.write(text + "\n")

    return "Note saved successfully."



def read_note():

    if not os.path.exists(NOTES_FILE):

        return "No notes found."

    with open(NOTES_FILE, "r", encoding="utf-8") as f:

        data = f.read()

    if data.strip()=="":

        return "No notes found."

    return data



def clear_note():

    with open(NOTES_FILE, "w", encoding="utf-8") as f:

        f.write("")

    return "All notes deleted."

# ==========================
# FILE MANAGER
# ==========================

def create_file(filename):

    path = os.path.join(WORKSPACE, filename)

    if os.path.exists(path):
        return "File already exists."

    with open(path, "w", encoding="utf-8") as f:
        f.write("")

    return "File created successfully."


def read_file(filename):

    path = os.path.join(WORKSPACE, filename)

    if not os.path.exists(path):
        return "File not found."

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def delete_file(filename):

    path = os.path.join(WORKSPACE, filename)

    if not os.path.exists(path):
        return "File not found."

    os.remove(path)

    return "File deleted successfully."


def list_files():

    files = os.listdir(WORKSPACE)

    if len(files) == 0:
        return "Workspace is empty."

    return "\n".join(files)
# ==========================
# INTERNET STATUS
# ==========================

def internet_status():

    try:

        requests.get("https://www.google.com", timeout=5)

        return "✅ Internet is Connected."

    except:

        return "❌ No Internet Connection."


# ==========================
# PUBLIC IP
# ==========================

def public_ip():

    try:

        data = requests.get("https://api.ipify.org").text

        return "Your Public IP : " + data

    except:

        return "Unable to fetch IP."

# ==========================
# WIKIPEDIA SEARCH
# ==========================
def wiki_search(query):

    try:

        result = wikipedia.summary(query, sentences=3)

        return result

    except Exception:

        return "No information found."


def duckduckgo_search(query):

    try:

        url = "https://api.duckduckgo.com/"

        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        if data.get("Answer"):
            return data["Answer"]

        return None

    except Exception:

        return None
# ==========================
# PART 15.15 - SMART INTERNET ROUTER
# ==========================

def internet_engine(question):

    q = question.lower().strip()

    # ===== 1. Research & Papers =====
    research_keywords = [
        "paper", "research", "doi", "journal",
        "study", "scientific", "arxiv"
    ]

    if any(k in q for k in research_keywords):

        result = arxiv_search(question)
        if result:
            return result

        result = crossref_search(question)
        if result:
            return result


    # ===== 2. Books =====
    book_keywords = [
        "book", "novel", "author", "read"
    ]

    if any(k in q for k in book_keywords):

        result = openlibrary_search(question)
        if result:
            return result


    # ===== 3. Countries =====
    country_keywords = [
        "capital", "population", "currency",
        "country", "region", "language"
    ]

    if any(k in q for k in country_keywords):

        result = country_search(question)
        if result:
            return result


    # ===== 4. Universities =====
    if "universit" in q or "college" in q:

        result = universities_search(question)
        if result:
            return result


    # ===== 5. Maps / Location =====
    map_keywords = [
        "map", "location", "where is",
        "coordinates", "latitude", "longitude"
    ]

    if any(k in q for k in map_keywords):

        result = osm_search(question)
        if result:
            return result


    # ===== 6. Space =====
    space_keywords = [
        "spacex", "rocket", "starship",
        "falcon", "launch", "nasa"
    ]

    if any(k in q for k in space_keywords):

        result = spacex_search(question)
        if result:
            return result


    # ===== 7. TV / Anime =====
    tv_keywords = [
        "anime", "series", "show",
        "season", "episode", "netflix"
    ]

    if any(k in q for k in tv_keywords):

        result = tvmaze_search(question)
        if result:
            return result


    # ===== 8. Pokémon =====
    pokemon_keywords = [
        "pokemon", "pikachu", "charizard",
        "bulbasaur", "squirtle"
    ]

    if any(k in q for k in pokemon_keywords):

        result = pokemon_search(question)
        if result:
            return result


    # ===== 9. Dictionary =====
    if len(q.split()) == 1:

        result = dictionary_search(question)
        if result:
            return result


    # ===== 10. General Knowledge =====
    result = wiki_search(question)
    if result != "No information found.":
        return result

    result = duckduckgo_search(question)
    if result:
        return result

    result = wikidata_search(question)
    if result:
        return result


    # ===== Nothing Found =====
    return None
     # ==========================
# PART 15.4 - WIKIDATA
# ==========================

def wikidata_search(query):

    try:

        url = "https://www.wikidata.org/w/api.php"

        params = {
            "action": "wbsearchentities",
            "search": query,
            "language": "en",
            "format": "json",
            "limit": 1
        }

        data = requests.get(url, params=params, timeout=10).json()

        if data.get("search"):

            item = data["search"][0]

            return f"{item['label']}\n{item.get('description','No description')}"

        return None

    except:

        return None
    if result:
        return result

    # Future Backup APIs
    # result = wikidata_search(question)
    # result = dictionary_search(question)
    # result = openlibrary_search(question)

    return None 
# ==========================
# PART 15.5 - DICTIONARY
# ==========================

def dictionary_search(word):

    try:

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        data = requests.get(url, timeout=10).json()

        if isinstance(data, list):

            meaning = data[0]["meanings"][0]
            definition = meaning["definitions"][0]["definition"]

            return f"{word}\nMeaning: {definition}"

        return None

    except:

        return None
        
# ==========================
# PART 15.6 - OPEN LIBRARY
# ==========================

def openlibrary_search(query):

    try:

        url = "https://openlibrary.org/search.json"

        params = {
            "q": query,
            "limit": 1
        }

        data = requests.get(url, params=params, timeout=10).json()

        if data.get("docs"):

            book = data["docs"][0]

            title = book.get("title", "Unknown")
            author = ", ".join(book.get("author_name", ["Unknown"]))
            year = book.get("first_publish_year", "Unknown")

            return (
                f"Book: {title}\n"
                f"Author: {author}\n"
                f"First Published: {year}"
            )

        return None

    except:
        return None
# ==========================
# PART 15.7 - REST COUNTRIES
# ==========================

def country_search(query):

    try:

        url = f"https://restcountries.com/v3.1/name/{query}"

        data = requests.get(url, timeout=10).json()

        if isinstance(data, list):

            country = data[0]

            name = country.get("name", {}).get("common", "Unknown")
            capital = ", ".join(country.get("capital", ["Unknown"]))
            population = country.get("population", "Unknown")
            region = country.get("region", "Unknown")

            currencies = country.get("currencies", {})
            currency_names = []

            for c in currencies.values():
                currency_names.append(c.get("name", "Unknown"))

            currency = ", ".join(currency_names) if currency_names else "Unknown"

            languages = country.get("languages", {})
            language = ", ".join(languages.values()) if languages else "Unknown"

            return (
                f"Country: {name}\n"
                f"Capital: {capital}\n"
                f"Population: {population}\n"
                f"Region: {region}\n"
                f"Currency: {currency}\n"
                f"Language: {language}"
            )

        return None

    except:
        return None

# ==========================
# PART 15.8 - UNIVERSITIES API
# ==========================

def universities_search(country):

    try:

        url = "http://universities.hipolabs.com/search"

        params = {
            "country": country
        }

        data = requests.get(url, params=params, timeout=10).json()

        if data:

            result = f"Top Universities in {country}:\n\n"

            for uni in data[:5]:  # sirf pehli 5 universities
                result += f"• {uni.get('name', 'Unknown')}\n"

            return result

        return None

    except:
        return None
        
# ==========================
# PART 15.9 - OPENSTREETMAP
# ==========================

def osm_search(place):

    try:

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": place,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "ETHAF-AI/1.0"
        }

        data = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        ).json()

        if data:

            place_data = data[0]

            name = place_data.get("display_name", "Unknown")
            lat = place_data.get("lat", "Unknown")
            lon = place_data.get("lon", "Unknown")

            return (
                f"Place: {name}\n"
                f"Latitude: {lat}\n"
                f"Longitude: {lon}"
            )

        return None

    except:
        return None

# ==========================
# PART 15.10 - CROSSREF
# ==========================

def crossref_search(query):

    try:

        url = "https://api.crossref.org/works"

        params = {
            "query": query,
            "rows": 1
        }

        headers = {
            "User-Agent": "ETHAF-AI/1.0 (mailto:ethaf@example.com)"
        }

        data = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        ).json()

        items = data.get("message", {}).get("items", [])

        if items:

            paper = items[0]

            title = paper.get("title", ["Unknown"])[0]

            authors = []

            for a in paper.get("author", [])[:3]:
                name = f"{a.get('given','')} {a.get('family','')}".strip()
                authors.append(name)

            author_text = ", ".join(authors) if authors else "Unknown"

            year = "Unknown"
            if "published-print" in paper:
                year = paper["published-print"]["date-parts"][0][0]
            elif "published-online" in paper:
                year = paper["published-online"]["date-parts"][0][0]

            doi = paper.get("DOI", "Unknown")

            return (
                f"Research Paper: {title}\n"
                f"Authors: {author_text}\n"
                f"Year: {year}\n"
                f"DOI: {doi}"
            )

        return None

    except:
        return None
 # ==========================
# PART 15.11 - ARXIV
# ==========================

def arxiv_search(query):

    try:

        url = "http://export.arxiv.org/api/query"

        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": 1
        }

        response = requests.get(url, params=params, timeout=15)

        text = response.text

        # Simple XML parsing
        title_start = text.find("<title>", text.find("<entry>")) + 7
        title_end = text.find("</title>", title_start)

        summary_start = text.find("<summary>", title_end) + 9
        summary_end = text.find("</summary>", summary_start)

        if title_start > 6 and title_end != -1:

            title = text[title_start:title_end].strip()
            summary = text[summary_start:summary_end].strip()

            summary = " ".join(summary.split())[:300]

            return (
                f"arXiv Paper: {title}\n\n"
                f"Summary: {summary}..."
            )

        return None

    except:
        return None
 
# ==========================
# PART 15.12 - SPACEX
# ==========================

def spacex_search(query):

    try:

        q = query.lower()

        # Sirf space related queries par chale
        keywords = [
            "spacex", "rocket", "falcon", "starship",
            "launch", "nasa", "space mission"
        ]

        if not any(k in q for k in keywords):
            return None

        # Latest launch
        url = "https://api.spacexdata.com/v5/launches/latest"

        launch = requests.get(url, timeout=10).json()

        mission = launch.get("name", "Unknown")
        date = launch.get("date_utc", "Unknown")
        success = launch.get("success", None)

        status = "Unknown"
        if success is True:
            status = "Successful"
        elif success is False:
            status = "Failed"

        return (
            f"🚀 SpaceX Latest Launch\n\n"
            f"Mission: {mission}\n"
            f"Date (UTC): {date}\n"
            f"Status: {status}"
        )

    except:
        return None

# ==========================
# PART 15.13 - TVMAZE
# ==========================

def tvmaze_search(query):

    try:

        q = query.lower()

        # TV related keywords
        keywords = [
            "tv", "show", "series", "anime",
            "episode", "season", "netflix"
        ]

        if not any(k in q for k in keywords):
            return None

        # Query clean
        clean_query = q.replace("tv", "").replace("show", "").replace("series", "").strip()

        url = "https://api.tvmaze.com/search/shows"

        params = {
            "q": clean_query
        }

        data = requests.get(url, params=params, timeout=10).json()

        if data:

            show = data[0]["show"]

            name = show.get("name", "Unknown")
            rating = show.get("rating", {}).get("average", "N/A")
            genres = ", ".join(show.get("genres", []))
            premiered = show.get("premiered", "Unknown")

            summary = show.get("summary", "")
            summary = summary.replace("<p>", "").replace("</p>", "")
            summary = summary[:250]

            return (
                f"📺 TV Show: {name}\n"
                f"⭐ Rating: {rating}\n"
                f"🎭 Genres: {genres}\n"
                f"📅 Premiered: {premiered}\n\n"
                f"Summary: {summary}..."
            )

        return None

    except:
        return None

# ==========================
# FREE NAVIGATION (NO API KEY)
# ==========================

def route_search(start_place, end_place):

    try:
        # Start coordinates
        s = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": start_place, "format": "json", "limit": 1},
            headers={"User-Agent": "ETHAF-AI/1.0"},
            timeout=10
        ).json()

        # End coordinates
        e = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": end_place, "format": "json", "limit": 1},
            headers={"User-Agent": "ETHAF-AI/1.0"},
            timeout=10
        ).json()

        if not s or not e:
            return "Location not found."

        s_lat, s_lon = s[0]["lat"], s[0]["lon"]
        e_lat, e_lon = e[0]["lat"], e[0]["lon"]

        # Route from OSRM
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{s_lon},{s_lat};{e_lon},{e_lat}"
        )

        data = requests.get(
            url,
            params={"overview": "false"},
            timeout=15
        ).json()

        if data.get("routes"):

            route = data["routes"][0]

            distance_km = round(route["distance"] / 1000, 1)
            duration_hr = round(route["duration"] / 3600, 1)

            return (
                f"🗺️ Route: {start_place} → {end_place}\n"
                f"Distance: {distance_km} km\n"
                f"Estimated Time: {duration_hr} hours\n"
                f"Travel Mode: Driving"
            )

        return "Route not found."

    except Exception as e:
        return f"Navigation Error: {e}"
# ==========================
# MATH ENGINE
# ==========================

def math_engine(q):

    try:

        # Basic Calculator
        if any(op in q for op in ["+", "-", "*", "/", "%", "**"]):
            return f"Answer : {eval(q)}"

        # Square Root
        if q.startswith("sqrt"):
            num = int(q.split()[1])
            return f"Square Root = {math.sqrt(num)}"

        # Factorial
        if q.startswith("factorial"):
            num = int(q.split()[1])
            return f"Factorial = {math.factorial(num)}"

        # LCM
        if q.startswith("lcm"):
            nums = [int(x) for x in q.split()[1:]]
            return f"LCM = {math.lcm(*nums)}"

        # HCF / GCD
        if q.startswith("hcf") or q.startswith("gcd"):
            nums = [int(x) for x in q.split()[1:]]
            ans = nums[0]
            for i in nums[1:]:
                ans = math.gcd(ans, i)
            return f"HCF = {ans}"

    except Exception as e:
        return f"Math Error : {e}"

    return None

# ==========================
# BASIC KNOWLEDGE
# ==========================

knowledge = {
    "hello": "Hello! I am ETHAF AI.",
    "hi": "Hello!",
    "who is your owner": OWNER,
    "what is your name": APP_NAME,
    "country": COUNTRY,
    "bye": "Good Bye 😊"

}
# ==========================
# KNOWLEDGE BASE
# ==========================

topics = {

    # English
    "noun": "A noun is a naming word. Example: Ram, India, Book.",

    "verb": "A verb is an action word. Example: run, eat, play.",

    "adjective": "An adjective describes a noun. Example: beautiful, red, tall.",

    "pronoun": "A pronoun replaces a noun. Example: he, she, they.",

    "tense": "Tense tells the time of an action. Present, Past and Future.",

    # Science

    "gravity": "Gravity is the force that attracts objects towards the Earth.",

    "photosynthesis": "Plants prepare food using sunlight, water and carbon dioxide.",

    "force": "Force is a push or pull.",

    "friction": "Friction opposes motion between two surfaces.",

    "sound": "Sound is produced due to vibrations.",

    "light": "Light travels in a straight line.",

    "atom": "Atom is the smallest unit of an element.",

    "cell": "Cell is the basic unit of life.",

    # Maths

    "pi": "Value of Pi = 3.1415926535",

    "table of 2": "2 4 6 8 10 12 14 16 18 20",

    "table of 5": "5 10 15 20 25 30 35 40 45 50",

    # GK

    "india": "Capital: New Delhi",

    "president of india": "Current President information should be updated manually if needed.",

    "computer": "Computer is an electronic machine.",

    "python": "Python is a high-level programming language."
}

# ==========================
# TIMER
# ==========================

def timer(seconds):

    try:

        seconds = int(seconds)

        print(f"Timer Started : {seconds} seconds")

        while seconds > 0:

            print(seconds)

            time.sleep(1)

            seconds -= 1

        return "⏰ Time is over!"

    except:

        return "Invalid timer value."


# ==========================
# STOPWATCH
# ==========================

def stopwatch():

    start = time.time()

    input("Press ENTER to stop stopwatch...")

    end = time.time()

    return f"Elapsed Time : {round(end-start,2)} seconds"

# ==========================
# ETHAF BRAIN v1.0
# ==========================

def brain(question):

    q = question.lower().strip()

    decision = {

        "memory": False,

        "knowledge": False,

        "math": False,

        "file": False,

        "note": False,

        "internet": False,

        "learn": False,

        "unknown": False

    }

    # -------- Learn --------

    if q.startswith("learn:"):

        decision["learn"] = True

        return decision

    # -------- Math --------

    if any(op in q for op in ["+","-","*","/","sqrt","lcm","hcf","gcd","**"]):

        decision["math"] = True

        return decision

    # -------- Knowledge --------

    for topic in topics_qa:

        if topic in q:

            decision["knowledge"] = True

            return decision

    # -------- Notes --------

    if "note" in q:

        decision["note"] = True

        return decision

    # -------- Files --------

    if "file" in q:

        decision["file"] = True

        return decision

    # -------- Internet --------

    if "wiki" in q or "wikipedia" in q:

        decision["internet"] = True

        return decision

    # -------- Memory --------

    if question in memory:

        decision["memory"] = True

        return decision

    decision["unknown"] = True

    return decision
    
# ==========================
# PDF READER
# ==========================
# PDF Memory
PDF_TEXT = ""
def read_pdf(pdf_path):

    global PDF_TEXT

    try:

        reader = PdfReader(pdf_path)

        PDF_TEXT = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                PDF_TEXT += page_text + "\n"

        if PDF_TEXT.strip():

            return f"✅ PDF Loaded Successfully\nPages : {len(reader.pages)}"

        return "PDF me text nahi mila."

    except Exception as e:

        return f"PDF Error : {e}"
        
        
def pdf_summary():

    global PDF_TEXT

    if PDF_TEXT == "":

        return "Pehle PDF load karo."

    words = PDF_TEXT.split()

    total_words = len(words)

    preview = " ".join(words[:150])

    return (
        f"===== PDF SUMMARY =====\n\n"
        f"Total Words : {total_words}\n\n"
        f"{preview}..."
    )
# ==========================
# SAFETY FILTER
# ==========================

def safety_filter(text):

    blocked = [
        "hack", "phishing", "malware", "virus",
        "steal password", "ddos", "ransomware",
        "bypass otp", "crack account"
    ]

    t = text.lower()

    for word in blocked:
        if word in t:
            return "⛔ This request is blocked for safety."

    return None    
       
# ==========================
# REPLY
# ==========================

def detect_language(text):

    global USER_LANGUAGE

    try:
        lang = detect(text)
        USER_LANGUAGE = lang
        return lang

    except:
        USER_LANGUAGE = "en"
        return "en"
def translate_to_english(text):

    try:

        return GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

    except:

        return text
def translate_reply(text):

    global USER_LANGUAGE

    try:

        if USER_LANGUAGE == "en":
            return text

        return GoogleTranslator(
            source="en",
            target=USER_LANGUAGE
        ).translate(text)

    except:

        return text

def reply(question):

    q = question.lower().strip()

    detect_language(question)

    english_question = translate_to_english(question)
    q = english_question.lower().strip().replace("?", "").replace(".", "")

    q = english_question.lower().strip()
    print("Translated:", q)
        
    # ===== Language Engine =====

    detect_language(question)

    english_question = translate_to_english(question)

    q = english_question.lower().strip()
    
     

    # baaki code...
        # ==========================
    # PDF COMMAND
    # ==========================

    if q.startswith("read pdf:"):

        pdf_file = question[9:].strip()

        return read_pdf(pdf_file)
    
    # ==========================
    # TIMER
    # ==========================

    if q.startswith("timer:"):

        sec = question[6:].strip()

        return timer(sec)

    # ==========================
    # STOPWATCH
    # ==========================

    if q == "stopwatch":

        return stopwatch()
        # ==========================
    # WIKIPEDIA
    # ==========================

    if q.startswith("search:"):

        topic = question[7:].strip()

        return wiki_search(topic)

    # ==========================
    # INTERNET STATUS
    # ==========================

    if q == "internet status":

        return internet_status()

    
    # ==========================
    # PUBLIC IP
    # ==========================

    if q == "ip":

        return public_ip()
    
        # ==========================
    # CREATE FILE
    # ==========================

    if q.startswith("create file:"):

        return create_file(question[12:].strip())

    # ==========================
    # READ FILE
    # ==========================

    if q.startswith("read file:"):

        return read_file(question[10:].strip())

    # ==========================
    # DELETE FILE
    # ==========================

    if q.startswith("delete file:"):

        return delete_file(question[12:].strip())

    # ==========================
    # LIST FILES
    # ==========================

    if q == "list files":

        return list_files()

    # ==========================
    # SAVE NOTE
    # ==========================

    if q.startswith("save note:"):

        return save_note(question[10:].strip())



    # ==========================
    # READ NOTE
    # ==========================

    if q=="read note":

        return read_note()



    # ==========================
    # CLEAR NOTE
    # ==========================

    if q=="clear note":

        return clear_note()
    # ==========================
    # REMEMBER
    # ==========================

    if q.startswith("remember:"):

        try:

            text = question[9:]

            key, value = text.split("=",1)

            key = key.strip().lower()

            value = value.strip()

            user_profile[key] = value

            memory["profile"] = user_profile

            save_memory()

            return "I will remember that."

        except:

            return "Usage : remember: key = value"

    # ==========================
    # WHO AM I
    # ==========================

    if q == "who am i":

        if "profile" in memory:

            txt = ""

            for k,v in memory["profile"].items():

                txt += f"{k} : {v}\n"

            return txt

        return "I don't know you yet."

    # ==========================
    # HISTORY
    # ==========================

    if q == "history":

        if not history:

            return "No history."

        text=""

        for item in history[-10:]:

            text += f"You : {item['user']}\n"

            text += f"AI : {item['ai']}\n\n"

        return text

    # ==========================
    # CLEAR HISTORY
    # ==========================

    if q=="clear history":

        history.clear()

        save_memory()

        return "History Cleared."
    # ==========================
    # LIST MEMORY
    # ==========================

    if q == "list memory":

        if len(memory) == 0:

            return "No memory saved."

        text = ""

        for item in memory:

            text += item + "\n"

        return text
    # ==========================
    # DELETE ALL MEMORY
    # ==========================

    if q == "delete all memory":

        memory.clear()

        save_memory()

        return "All memory deleted."
    # ==========================
    # MATH
    # ==========================

    result = math_engine(q)

    if result:

        return result
         # ==========================
    # KNOWLEDGE SEARCH
    # ==========================

    if q in topics:

        return topics[q]
    # ==========================
    # HELP
    # ==========================

    if q == "help":

        return """
===== ETHAF AI COMMANDS =====

help

learn: question = answer

forget: question

memory

date

time

owner

version

bye

=============================
"""

    # ==========================
    # MEMORY COUNT
    # ==========================

    if q == "memory":

        return f"Total Saved Memory : {len(memory)}"

    # ==========================
    # DELETE MEMORY
    # ==========================

    if q.startswith("forget:"):

        return forget(question[7:].strip())

    # ==========================
    # DATE
    # ==========================

    if q == "date":

        return str(datetime.date.today())

    # ==========================
    # TIME
    # ==========================

    if q == "time":

        return datetime.datetime.now().strftime("%H:%M:%S")

    # ==========================
    # OWNER
    # ==========================

    if q == "owner":

        return OWNER

    # ==========================
    # VERSION
    # ==========================

    if q == "version":

        return VERSION
    # ==========================
    # Learn Command
    # ==========================
    #if q.startswith("learn:"):
    #    return learn(question[6:].strip())

    if q in knowledge:
        return knowledge[q]

    if q in memory:
        return memory[q]

    for k, v in memory.items():
        if q == k:
            return v
     # Internet Engine Backup
    result = internet_engine(question)

    if result:
            return result

    # DuckDuckGo Backup Search
    result = duckduckgo_search(question)

    if result:
        return result

    return "Sorry, I don't know this yet."
# ==========================
# MAIN LOOP
# ==========================

#print("\nETHAF AI Ready\n")

#while True:

   # user = input("You : ").strip()

   # if user == "":
 #       print("ETHAF AI : Please enter a question.")
#        continue

    #answer = reply(user)

   # print("ETHAF AI :", answer)

   # if user.lower() == "bye":
        #break
 #       
#history.append({

   # "user": user,

   # "ai": answer

#})

#save_memory()
#
# ==========================
# ETHAF WEB SERVER
# ==========================

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    ai_reply = reply(user_message)

    return jsonify({
        "reply": ai_reply
    })

print("🌐 ETHAF AI Web Server Started")
print("📱 Open your HTML page in TrebEdit")
print("🔗 API running at: http://127.0.0.1:5000/chat")

app.run(host="0.0.0.0", port=5000, debug=False)