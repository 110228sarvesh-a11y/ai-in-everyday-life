import tkinter as tk
from tkinter import scrolledtext, filedialog
import ollama
import threading
import queue


# ==============================
# SETTINGS
# ==============================

MODEL = "llama3"

BG = "#050505"
GREEN = "#00ff66"
DARK_GREEN = "#063b1b"
LIGHT_GREEN = "#66ff99"
WHITE = "#eafff0"
RED = "#ff4444"


# ==============================
# APP WINDOW
# ==============================

root = tk.Tk()
root.title("AI IN EVERYDAY LIFE")
root.geometry("1000x700")
root.minsize(800, 550)
root.configure(bg=BG)


# ==============================
# MEMORY
# ==============================

conversation = []

response_queue = queue.Queue()
is_generating = False


# ==============================
# HEADER
# ==============================

header = tk.Frame(
    root,
    bg=BG,
    highlightbackground=GREEN,
    highlightthickness=2
)
header.pack(fill="x", padx=10, pady=(10, 5))

title = tk.Label(
    header,
    text="◆ AI IN EVERYDAY LIFE ◆",
    font=("Courier New", 22, "bold"),
    fg=GREEN,
    bg=BG
)
title.pack(pady=(10, 2))

subtitle = tk.Label(
    header,
    text="LOCAL AI SYSTEM // LLAMA 3 // ONLINE",
    font=("Courier New", 10),
    fg=LIGHT_GREEN,
    bg=BG
)
subtitle.pack(pady=(0, 10))


# ==============================
# TOOLBAR
# ==============================

toolbar = tk.Frame(root, bg=BG)
toolbar.pack(fill="x", padx=10, pady=5)


def button_style(button):
    button.configure(
        font=("Courier New", 9, "bold"),
        fg=GREEN,
        bg=BG,
        activeforeground=BG,
        activebackground=GREEN,
        relief="solid",
        bd=1,
        padx=10,
        pady=6,
        cursor="hand2"
    )


# Mode buttons

study_button = tk.Button(
    toolbar,
    text="[ STUDY ]",
    command=lambda: set_mode("study")
)
button_style(study_button)
study_button.pack(side="left", padx=3)


daily_button = tk.Button(
    toolbar,
    text="[ DAILY LIFE ]",
    command=lambda: set_mode("daily")
)
button_style(daily_button)
daily_button.pack(side="left", padx=3)


ask_button = tk.Button(
    toolbar,
    text="[ ASK AI ]",
    command=lambda: set_mode("ask")
)
button_style(ask_button)
ask_button.pack(side="left", padx=3)


info_button = tk.Button(
    toolbar,
    text="[ AI INFO ]",
    command=lambda: show_ai_info()
)
button_style(info_button)
info_button.pack(side="left", padx=3)


# Save button

save_button = tk.Button(
    toolbar,
    text="[ SAVE CHAT ]",
    command=lambda: save_chat()
)
button_style(save_button)
save_button.pack(side="left", padx=3)


# Clear button

clear_button = tk.Button(
    toolbar,
    text="[ CLEAR MEMORY ]",
    command=lambda: clear_chat()
)
button_style(clear_button)
clear_button.pack(side="left", padx=3)


# Status

status = tk.Label(
    toolbar,
    text="● SYSTEM READY",
    font=("Courier New", 9, "bold"),
    fg=GREEN,
    bg=BG
)
status.pack(side="right", padx=8)


# ==============================
# CHAT AREA
# ==============================

chat_frame = tk.Frame(
    root,
    bg=BG,
    highlightbackground=DARK_GREEN,
    highlightthickness=2
)
chat_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


chat_box = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Courier New", 11),
    bg="#020202",
    fg=GREEN,
    insertbackground=GREEN,
    selectbackground=DARK_GREEN,
    selectforeground=WHITE,
    relief="flat",
    bd=0
)

chat_box.pack(
    fill="both",
    expand=True,
    padx=8,
    pady=8
)


chat_box.insert(
    tk.END,
    "========================================\n"
    "        AI IN EVERYDAY LIFE\n"
    "========================================\n\n"
    "AI > LOCAL AI SYSTEM INITIALIZED.\n"
    "AI > LLAMA 3 ONLINE.\n"
    "AI > MEMORY SYSTEM READY.\n\n"
    "AI > SELECT A MODE OR ASK ME ANYTHING.\n\n"
)


# ==============================
# INPUT AREA
# ==============================

input_frame = tk.Frame(root, bg=BG)
input_frame.pack(fill="x", padx=10, pady=(5, 5))


input_label = tk.Label(
    input_frame,
    text="YOU >",
    font=("Courier New", 11, "bold"),
    fg=GREEN,
    bg=BG
)
input_label.pack(side="left", padx=(0, 5))


user_input = tk.Entry(
    input_frame,
    font=("Courier New", 11),
    bg="#020202",
    fg=GREEN,
    insertbackground=GREEN,
    relief="solid",
    bd=1
)

user_input.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=7
)


send_button = tk.Button(
    input_frame,
    text="[ SEND ]",
    command=lambda: send_message()
)

button_style(send_button)

send_button.pack(
    side="right",
    padx=(5, 0)
)


# ==============================
# MODE
# ==============================

current_mode = "ask"


def set_mode(mode):

    global current_mode

    current_mode = mode

    if mode == "study":

        status.config(
            text="● MODE: STUDY",
            fg=GREEN
        )

        user_input.delete(0, tk.END)
        user_input.insert(
            0,
            "Explain a topic to me"
        )

        user_input.focus()

    elif mode == "daily":

        status.config(
            text="● MODE: DAILY LIFE",
            fg=GREEN
        )

        user_input.delete(0, tk.END)
        user_input.insert(
            0,
            "How is AI used in daily life?"
        )

        user_input.focus()

    else:

        status.config(
            text="● MODE: ASK AI",
            fg=GREEN
        )

        user_input.delete(0, tk.END)
        user_input.focus()


# ==============================
# AI INFO
# ==============================

def show_ai_info():

    chat_box.delete("1.0", tk.END)

    info = """
========================================
          AI IN EVERYDAY LIFE
========================================

WHAT IS AI?

Artificial Intelligence allows computers
to perform tasks that normally require
human intelligence.

----------------------------------------

AI IN EVERYDAY LIFE

01. YOUTUBE
AI recommends videos based on what users
watch, search and interact with.

02. GOOGLE MAPS
AI helps predict traffic and suggests
routes.

03. ONLINE SHOPPING
AI recommends products based on browsing
and shopping activity.

04. SMARTPHONES
AI powers voice assistants, cameras,
face recognition and smart features.

05. EDUCATION
AI can help students understand topics,
generate explanations and practice
questions.

06. ENTERTAINMENT
AI can recommend movies, music, games
and other content.

07. LANGUAGE TOOLS
AI can help with translation, writing,
summarization and learning languages.

08. ACCESSIBILITY
AI can assist people through speech,
text recognition and other technologies.

----------------------------------------

TECH STACK

PYTHON
    Main programming language

TKINTER
    Graphical user interface

OLLAMA
    Runs the AI locally

LLAMA 3
    AI language model

LOCAL AI
    Runs without sending your chat to
    a cloud AI service

----------------------------------------

PROJECT FEATURES

[✓] AI CHAT
[✓] STREAMING RESPONSES
[✓] CONVERSATION MEMORY
[✓] STUDY MODE
[✓] DAILY LIFE MODE
[✓] AI INFORMATION PANEL
[✓] SAVE CHAT
[✓] CLEAR MEMORY

========================================
"""

    chat_box.insert(tk.END, info)

    status.config(
        text="● AI INFO",
        fg=LIGHT_GREEN
    )


# ==============================
# SAVE CHAT
# ==============================

def save_chat():

    filename = filedialog.asksaveasfilename(
        title="Save AI Conversation",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if filename == "":
        return

    chat_content = chat_box.get(
        "1.0",
        tk.END
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(chat_content)

    status.config(
        text="● CHAT SAVED",
        fg=GREEN
    )


# ==============================
# CLEAR MEMORY
# ==============================

def clear_chat():

    global conversation

    conversation = []

    chat_box.delete(
        "1.0",
        tk.END
    )

    chat_box.insert(
        tk.END,
        "AI > CHAT MEMORY CLEARED.\n"
        "AI > SYSTEM READY.\n\n"
    )

    status.config(
        text="● MEMORY CLEARED",
        fg=GREEN
    )


# ==============================
# SEND MESSAGE
# ==============================

def send_message():

    global is_generating

    if is_generating:
        return

    message = user_input.get().strip()

    if message == "":
        return

    # Add user message to screen

    chat_box.insert(
        tk.END,
        "YOU > " + message + "\n\n"
    )

    chat_box.see(tk.END)

    user_input.delete(
        0,
        tk.END
    )

    # Disable send button

    is_generating = True

    send_button.config(
        state="disabled",
        text="[ THINKING... ]"
    )

    status.config(
        text="● AI GENERATING...",
        fg=LIGHT_GREEN
    )

    # Create mode prompt

    if current_mode == "study":

        prompt = (
            "You are a friendly study assistant. "
            "Explain the following topic clearly "
            "for a first-year college student. "
            "Use simple examples.\n\n"
            + message
        )

    elif current_mode == "daily":

        prompt = (
            "Explain how artificial intelligence "
            "relates to everyday life. "
            "Give practical and simple examples.\n\n"
            + message
        )

    else:

        prompt = message

    # Add message to memory

    conversation.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Start AI worker thread

    thread = threading.Thread(
        target=ask_ai,
        daemon=True
    )

    thread.start()

    # Start checking queue

    root.after(
        50,
        process_queue
    )


# ==============================
# AI WORKER
# ==============================

def ask_ai():

    try:

        stream = ollama.chat(
            model=MODEL,
            messages=conversation,
            stream=True
        )

        full_response = ""

        for chunk in stream:

            try:
                text = chunk["message"]["content"]
            except:
                text = ""

            if text:

                full_response += text

                response_queue.put(
                    ("text", text)
                )

        # Save complete response to memory

        conversation.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

        response_queue.put(
            ("done", "")
        )

    except Exception as e:

        response_queue.put(
            (
                "error",
                str(e)
            )
        )


# ==============================
# QUEUE PROCESSOR
# ==============================

def process_queue():

    global is_generating

    try:

        while True:

            message_type, data = response_queue.get_nowait()

            if message_type == "text":

                chat_box.insert(
                    tk.END,
                    data
                )

                chat_box.see(tk.END)

            elif message_type == "done":

                chat_box.insert(
                    tk.END,
                    "\n\n"
                )

                chat_box.see(tk.END)

                is_generating = False

                send_button.config(
                    state="normal",
                    text="[ SEND ]"
                )

                status.config(
                    text="● SYSTEM READY",
                    fg=GREEN
                )

            elif message_type == "error":

                chat_box.insert(
                    tk.END,
                    "\n\n"
                    "AI > ERROR:\n"
                    + data
                    + "\n\n"
                )

                chat_box.see(tk.END)

                is_generating = False

                send_button.config(
                    state="normal",
                    text="[ SEND ]"
                )

                status.config(
                    text="● ERROR",
                    fg=RED
                )

    except queue.Empty:
        pass

    if is_generating:

        root.after(
            50,
            process_queue
        )


# ==============================
# ENTER KEY
# ==============================

user_input.bind(
    "<Return>",
    lambda event: send_message()
)


# ==============================
# START
# ==============================

user_input.focus()

root.mainloop()
