import tkinter as tk
from datetime import datetime
import random
import threading
from unicodedata import name

# MAIN WINDOW
root = tk.Tk()
root.title("DecodeBot  |  DecodeLabs AI Assistant")

window_width  = 520
window_height = 620
screen_width  = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width  / 2) - (window_width  / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#EAF4FF")
root.minsize(420, 500)
root.resizable(True, True)

# SOUNDS  (winsound on Windows, silent elsewhere)
# Each sound runs in its own thread so it never
# blocks the UI.

def _beep_thread(sequence):
    """sequence = list of (freq_hz, duration_ms) tuples"""
    try:
        import winsound
        for freq, dur in sequence:
            winsound.Beep(freq, dur)
    except Exception:
        pass

def play_sound(kind):
    sequences = {
        # Window opens: warm rising chime  C5 E5 G5
        "startup":  [(523, 120), (659, 120), (784, 180)],
        # Message sent: short crisp tick
        "send":     [(1046, 60)],
        # Bot replies: soft two-note  E5 → A5
        "receive":  [(659, 90), (880, 110)],
        # Window closing: descending farewell  G5 E5 C5
        "bye":      [(784, 130), (659, 130), (523, 200)],
    }
    seq = sequences.get(kind, [])
    if seq:
        threading.Thread(target=_beep_thread, args=(seq,), daemon=True).start()

# RESPONSE DATABASE
def pick(lst):
    return random.choice(lst)

RESPONSES = {
    "greetings": [
        lambda n: f"Hey {n}! 👋 Great to see you. What's on your mind today?",
        lambda n: f"Hello {n}! 😊 DecodeBot is online and ready to help.",
        lambda n: f"Hi {n}! 🤖 How can I assist you today?",
        lambda n: f"Yo {n}! 👊 What are we building today?",
        lambda n: f"Welcome back, {n}! 🌟 Fire away.",
    ],
    "how_are_you": [
        "All circuits running at 100%! 💻 How are you doing?",
        "I'm fantastic. Just processed a million if-else conditions for fun. 😄 You?",
        "Living my best deterministic life! 🤖 Thanks for asking.",
        "Feeling optimized and ready to help! Any task you want me to tackle?",
    ],
    "name": [
        "My name is DecodeBot, your rule-based AI assistant from DecodeLabs! 🤖",
        "I go by DecodeBot. Simple, logical, and always on point. 😎",
        "DecodeBot at your service! Built with pure control flow and logic. ⚙️",
    ],
    "creator": [
        "I was crafted by Pratyaksha Singh during the DecodeLabs AI Internship, Batch 2026. 🛠️",
        "Pratyaksha Singh built me from scratch as part of the DecodeLabs AI program. Pretty cool, right? 😊",
        "My creator is Pratyaksha Singh, a future AI engineer making waves at DecodeLabs! 🚀",
    ],
    "joke": [
        "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛😄",
        "How many programmers does it take to change a light bulb?\nNone. That's a hardware problem! 💡😂",
        "A SQL query walks into a bar, sees two tables and asks:\n'Can I join you?' 🍺😄",
        "Why did the AI cross the road?\nBecause it was in its training data. 🤖😂",
        "I told my computer I needed a break...\nNow it won't stop sending me Kit-Kat ads. 🍫😅",
        "Why do Java developers wear glasses?\nBecause they don't C#! 🤓",
    ],
    "quote": [
        '"Success is the sum of small efforts repeated day in and day out."\n  — Robert Collier 💪',
        '"The best way to predict the future is to invent it."\n  — Alan Kay 🔮',
        '"First, solve the problem. Then, write the code."\n  — John Johnson 🧩',
        '"Any fool can write code that a computer can understand.\n Good programmers write code that humans can understand."\n  — Martin Fowler 📖',
        '"Code is like humor. When you have to explain it, it\'s bad."\n  — Cory House 😄',
        '"Programs must be written for people to read,\n and only incidentally for machines to execute."\n  — Harold Abelson 🎓',
    ],
    "motivate": [
        lambda n: f"{n}, every expert was once a beginner.\nKeep writing that code. Your future self will thank you. 🚀",
        lambda n: f"{n}, DecodeLabs picked you because you have potential.\nNow go prove them right! 💪",
        lambda n: f"Remember {n}: bugs are just features you haven't understood yet.\nDebug. Learn. Repeat. 🔥",
        lambda n: f"{n}, in this industry consistency beats talent every single time.\nShow up, build, and grow! 🌱",
        lambda n: f"The only bad code is the code you never wrote, {n}.\nStart. Iterate. Ship! ⚡",
    ],
    "ai_fact": [
        "🧠 AI Fact: The first rule-based AI system, DENDRAL (1965),\nidentified chemical compounds using pure logic. No neural networks!",
        "🧠 AI Fact: The term 'Artificial Intelligence' was coined by\nJohn McCarthy in 1956 at the Dartmouth Conference.",
        "🧠 AI Fact: Modern LLMs have billions of parameters, yet they're\nstill guided by rule-based guardrails like the ones you're building!",
        "🧠 AI Fact: A rule-based chatbot is called a 'white box' system.\nEvery decision is transparent and traceable. That's power!",
        "🧠 AI Fact: ELIZA (1966) was one of the earliest chatbots. It used\npattern matching and substitution, exactly what you're coding today.",
    ],
    "fun_fact": [
        "🎲 Fun Fact: Honey never spoils. Archaeologists found 3000-year-old\nhoney in Egyptian tombs and it was still edible!",
        "🎲 Fun Fact: A group of flamingos is called a 'flamboyance.'\nAbsolutely iconic. 🦩",
        "🎲 Fun Fact: The first computer bug was an actual bug, a moth stuck\nin Harvard's Mark II computer in 1947! 🦟",
        "🎲 Fun Fact: Bananas are slightly radioactive due to potassium-40.\nYou're basically eating a tiny reactor. 🍌☢️",
        "🎲 Fun Fact: There are more possible chess games than atoms in the\nobservable universe. 10^120 vs 10^80. ♟️",
    ],
    "thanks": [
        lambda n: f"You're welcome, {n}! 😊 Always here if you need me.",
        lambda n: f"Happy to help, {n}! That's what I'm here for. 🤖",
        lambda n: f"Anytime, {n}! Keep building! 💪",
    ]
}

FALLBACKS = [
    lambda n:  "🤔 I don't know how to respond to that yet.\n\n"
        "Type HELP to see available commands.\n\n"
        "You can also suggest new features using:\n"
        "suggest <your idea>"
        ]

# Clean, non-wrapping help text with consistent column width
HELP_TEXT = (
    "AVAILABLE COMMANDS\n"
    "💬  hello / hi / hey\n"
    "❓  name  |  creator\n"
    "👤  about me  |  how are you\n"
    "⏰  time  |  date  |  day  |  year\n"
    "😄  joke  |  fun fact  |  quote\n"
    "🧠  ai fact  |  what is ai\n"
    "💻  python  |  tkinter\n"
    " •   motivate\n"
    " •  rule-based  |  ipo model\n"
    " •  skills\n"
    " •  dictionary vs if-else\n"
    "👋  bye\n"
    "\n"
    "Commands are case-insensitive ✨"
)

suggestions = []
# RESPONSE LOGIC
user_name = None

def get_response(message):
    global user_name

    raw = message.strip()

    # First message = name collection
    if user_name is None:
        cleaned = raw.lower()
        for prefix in ["i am ", "i'm ", "my name is ", "call me "]:
            if cleaned.startswith(prefix):
                raw = raw[len(prefix):]
                break
        user_name = raw.strip().title()
        return (
            f"Welcome aboard, {user_name}! 👋\n\n"
            "I'm DecodeBot, your rule-based AI assistant from DecodeLabs.\n"
            "Type 'help' to see everything I can do, or just start chatting!"
        )

    n   = user_name
    msg = raw.lower().strip().rstrip("!?,.'")

    if msg in {"hello", "hi", "hey", "sup", "heya", "howdy", "hii", "helo"}:
        return pick(RESPONSES["greetings"])(n)

    if msg in {"how are you", "how are you doing", "how r u",
               "hows it going", "how do you do", "how are u"}:
        return pick(RESPONSES["how_are_you"])

    if msg in {"name", "what is your name", "what are you called",
               "who are you", "your name"}:
        return pick(RESPONSES["name"])

    if msg in {"creator", "who made you", "who created you",
               "who built you", "who is your creator", "made by"}:
        return pick(RESPONSES["creator"])

    if msg in {"joke", "tell me a joke", "make me laugh", "say a joke", "funny"}:
        return pick(RESPONSES["joke"])

    if msg in {"quote", "give me a quote", "inspire me", "a quote", "say a quote"}:
        return pick(RESPONSES["quote"])

    if msg in {"motivate", "motivate me", "give me motivation",
               "i need motivation", "motivation"}:
        return pick(RESPONSES["motivate"])(n)

    if msg in {"ai fact", "tell me an ai fact", "ai trivia", "artificial intelligence fact"}:
        return pick(RESPONSES["ai_fact"])

    if msg in {"fun fact", "tell me a fun fact", "random fact", "funfact", "interesting fact"}:
        return pick(RESPONSES["fun_fact"])

    if msg in {"thanks", "thank you", "thx", "ty", "cheers", "appreciate it", "thankyou"}:
        return pick(RESPONSES["thanks"])(n)

    if msg in {"about me", "who am i", "tell me about me", "my info"}:
        return (
            f"📋 Here's what I know about you:\n"
            f"  Name    : {n}\n"
            f"  Program : DecodeLabs AI Internship\n"
            f"  Status  : Future AI Engineer "
        )

    if msg in {"date", "what's the date", "what is the date", "today's date"}:
        return f"📅 Today is {datetime.now().strftime('%A, %d %B %Y')}."

    if msg in {"time", "what time is it", "current time", "what's the time"}:
        return f"⏰ Current time: {datetime.now().strftime('%I:%M:%S %p')}."

    if msg in {"day", "what day is it", "what day is today"}:
        return f"📅 Today is {datetime.now().strftime('%A')}."

    if msg in {"year", "what year is it", "current year"}:
        return f"📅 Current year: {datetime.now().year}."

    if msg in {"what is ai", "what is artificial intelligence", "explain ai", "define ai"}:
        return (
            "AI (Artificial Intelligence) is the simulation of human\n"
            "intelligence by machines, enabling them to learn, reason,\n"
            "and make decisions.\n\n"
            "You're literally building it right now at DecodeLabs! 🔥"
        )

    if msg in {"rule based", "what is rule based ai", "rule-based",
               "rule based ai", "rule based system"}:
        return (
            "A rule-based AI is a 'white box' system.\n"
            "It follows explicit if-else logic you define.\n\n"
            "Advantages:\n"
            " - Zero hallucination risk\n"
            " - Fully traceable: Input → Logic → Output\n"
            " - Great for compliance in finance and healthcare\n\n"
            "That's what makes Project 1 so powerful!"
        )

    if msg in {"ipo model", "ipo", "input process output", "what is ipo"}:
        return (
            "The IPO Model: Input → Process → Output\n\n"
            "  INPUT   : Sanitize and normalize raw user text\n"
            "  PROCESS : Match intent via your logic skeleton\n"
            "  OUTPUT  : Generate and display the response\n\n"
            "It's the foundational blueprint for all AI systems!"
        )

    if msg in {"skills", "what skills", "key skills", "what will i learn"}:
        return (
            "Key skills you're building in Project 1:\n"
            "  • Control flow and decision-making logic\n"
            "  • Input sanitization (lower + strip)\n"
            "  • Dictionary lookups: O(1) vs if-elif O(n)\n"
            "  • State management (user name, session)\n"
            "  • GUI development with tkinter\n"
            "  • Basic AI concepts"
        )

    if msg in {"dictionary vs if-else", "dictionary vs ifelse",
               "hash map vs ifelse", "why dictionary",
               "why not if else", "dict vs if"}:
        return (
            "If-elif chains have O(n) complexity.\n"
            "They slow down linearly as rules grow.\n\n"
            "Dictionaries use hash maps, giving you O(1)\n"
            "constant-time lookup regardless of rule count.\n\n"
            "That's why dict.get() is the professional approach. 🏆"
        )

    if msg in {"decodelabs", "decode labs", "about decodelabs", "what is decodelabs"}:
        return (
            "DecodeLabs is a tech training and internship\n"
            "platform based in Greater Lucknow, India.\n\n"
            "  📍 www.decodelabs.tech\n"
            "  📞 +91 89330 06408\n"
            "  ✉   decodelabs.tech@gmail.com\n\n"
            "Training the next generation of AI engineers,\n"
            "including you!"
        )

    if msg in {"python", "what is python", "python language", "about python"}:
        return (
            "Python is the go-to language for AI thanks to\n"
            "its simplicity and massive ecosystem.\n\n"
            "Libraries you'll explore in later projects:\n"
            "  NumPy · Pandas · scikit-learn · TensorFlow\n\n"
            "For now, you're already writing solid Python\n"
            "with tkinter. Keep going!"
        )

    if msg in {"tkinter", "what is tkinter", "tkinter library", "about tkinter"}:
        return (
            "Tkinter is Python's built-in GUI toolkit.\n"
            "No extra installation needed!\n\n"
            "You used: Canvas · Frame · Label · Entry\n"
            "          Scrollbar · Button\n\n"
            "Great foundation for desktop app development!"
        )

    if msg in {"help", "commands", "what can you do", "options", "menu"}:
        return HELP_TEXT

    if msg in {"bye", "goodbye", "see you", "later", "exit", "quit", "good bye", "cya"}:
        play_sound("bye")
        return (
        "Before you leave,\n"
        "please rate DecodeBot:\n\n"
        "rate 1\n"
        "rate 2\n"
        "rate 3\n"
        "rate 4\n"
        "rate 5"
    )
    if msg.startswith("rate "):
        rating = msg.replace("rate ", "")
        if rating in ["1","2","3","4","5"]:
            root.after(1500, root.destroy)
            root.after(2000, root.destroy)
            return (
                f"⭐ Thank you for rating DecodeBot "
                f"{rating}/5.\n\n"
                "Goodbye! 👋 Keep coding and keep building.\nSee you next time"
            )
        
    elif msg in ["good afternoon","good evening"]:
        return f"Hello {n}! Hope you're having a great day."
    
    if msg in ["ok", "okay", "cool","nice", "great","awesome", "good"]:
        return "😊 Glad to hear that!"
    
    elif msg == "thank you":
        return "You're most welcome! 😊"

    elif msg == "welcome":
        return "Thank you! 😄"

    elif msg == "haha":
        return "😂 Glad you liked it."

    elif msg == "lol":
        return "😆"
    
    elif msg.startswith("suggest "):
        suggestion = message[8:].strip()
        suggestions.append(suggestion)
        return (
            "✅ Thank you!\n\n"
            "Your suggestion has been noted:\n"
            f"{suggestion}"
        )

    # Partial / fuzzy fallbacks
    if any(g in msg for g in ["hello", "hi ", "hey "]):
        return pick(RESPONSES["greetings"])(n)
    if "joke"       in msg: return pick(RESPONSES["joke"])
    if "motivat"    in msg: return pick(RESPONSES["motivate"])(n)
    if "quote"      in msg: return pick(RESPONSES["quote"])
    if "time"       in msg: return f"⏰ Current time: {datetime.now().strftime('%I:%M:%S %p')}."
    if "date"       in msg: return f"📅 Today is {datetime.now().strftime('%A, %d %B %Y')}."
    if "thank"      in msg: return pick(RESPONSES["thanks"])(n)
    if "decodelabs" in msg: return (
        "DecodeLabs, Greater Lucknow, India.\n"
        "Visit www.decodelabs.tech "
    )
    if "fact"       in msg: return pick(RESPONSES["ai_fact"])
    if "skill"      in msg or "learn" in msg: return (
        "Type 'skills' to see what you're learning in Project 1!"
    )

    return pick(FALLBACKS)(n)

# UI – HEADER
header = tk.Frame(root, bg="#CFE8FF", height=60)
header.place(relx=0, rely=0, relwidth=1)
header.pack_propagate(False)

tk.Label(
    header,
    text="🤖  DecodeBot",
    font=("Segoe UI", 17, "bold"),
    bg="#CFE8FF", fg="#1a3a5c"
).pack(pady=(10, 0))

tk.Label(
    header,
    text="DecodeBot Assistant  |  DecodeLabs AI Internship  |  Batch 2026",
    font=("Segoe UI", 9),
    bg="#CFE8FF", fg="#3a6080"
).pack()

# UI – CHAT AREA
outer_frame = tk.Frame(root, bg="#EAF4FF")
outer_frame.pack(fill="both", expand=True, pady=(62, 0))

canvas = tk.Canvas(outer_frame, bg="#EAF4FF", highlightthickness=0)
scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)

messages_frame = tk.Frame(canvas, bg="#EAF4FF")
messages_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")

def on_canvas_resize(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", on_canvas_resize)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Two-finger / mouse-wheel scroll
def _on_mousewheel(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")
    else:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

for widget in [canvas, messages_frame]:
    widget.bind("<MouseWheel>", _on_mousewheel)
    widget.bind("<Button-4>",   _on_mousewheel)
    widget.bind("<Button-5>",   _on_mousewheel)

# ADD MESSAGE BUBBLE
def add_message(text, sender):
    is_user = sender == "user"
    ts      = datetime.now().strftime("%I:%M %p")

    row = tk.Frame(messages_frame, bg="#EAF4FF")
    row.pack(fill="x", padx=12, pady=5)

    col = tk.Frame(row, bg="#EAF4FF")

    bubble = tk.Label(
        col,
        text=text,
        bg="#2563EB" if is_user else "#FFFFFF",
        fg="#ffffff"  if is_user else "#1a3a5c",
        font=("Segoe UI", 11),
        padx=12, pady=9,
        wraplength=int(root.winfo_width() * 0.60),
        justify="left",
        relief="flat",
        anchor="w"
    )
    bubble.pack(anchor="e" if is_user else "w")

    tk.Label(
        col, text=ts,
        font=("Segoe UI", 8),
        bg="#EAF4FF", fg="#9ab4cc"
    ).pack(anchor="e" if is_user else "w", padx=2)

    if is_user:
        tk.Frame(row, bg="#EAF4FF").pack(side="left", fill="x", expand=True)
        col.pack(side="right", anchor="e")
    else:
        col.pack(side="left", anchor="w")
        tk.Frame(row, bg="#EAF4FF").pack(side="right", fill="x", expand=True)

    root.update_idletasks()
    canvas.yview_moveto(1.0)

    for w in [row, col, bubble]:
        w.bind("<MouseWheel>", _on_mousewheel)
        w.bind("<Button-4>",   _on_mousewheel)
        w.bind("<Button-5>",   _on_mousewheel)


# SEND LOGIC
def send_message(event=None):
    message = user_input.get().strip()
    if not message:
        return
    play_sound("send")
    add_message(message, "user")
    user_input.delete(0, tk.END)
    response = get_response(message)
    play_sound("receive")
    add_message(response, "bot")

# UI – INPUT BAR
bottom_frame = tk.Frame(root, bg="#EAF4FF", pady=10)
bottom_frame.pack(fill="x", padx=14, side="bottom")

user_input = tk.Entry(
    bottom_frame,
    font=("Segoe UI", 12),
    relief="solid", bd=1
)
user_input.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
user_input.bind("<Return>", send_message)

tk.Button(
    bottom_frame,
    text="Send  ➤",
    command=send_message,
    bg="#2563EB", fg="#ffffff",
    activebackground="#1D4ED8",
    activeforeground="#ffffff",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    padx=16, pady=6,
    cursor="hand2"
).pack(side="right")


# BOOT  (startup sound + staggered messages)
def boot():
    play_sound("startup")
    add_message("Hey there! I'm DecodeBot. 🤖", "bot")
    root.after(700,  lambda: add_message(
        "I'm a rule-based AI assistant built for the DecodeLabs AI Internship.", "bot"))
    root.after(1400, lambda: add_message(
        "Before we begin, what's your name? 😊", "bot"))

root.after(300, boot)
user_input.focus()
root.mainloop()