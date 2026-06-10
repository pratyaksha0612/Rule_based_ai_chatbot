#  DecodeBot Assistant

DecodeBot Assistant is a Rule-Based AI Chatbot developed using Python and Tkinter as part of the DecodeLabs AI Internship.

The chatbot provides interactive conversations through predefined rules and commands while maintaining a simple and user-friendly graphical interface.


##  Features

### User Personalization
- Stores user's name
- Allows changing name
- Personalized greetings and responses

### Date & Time Commands
- Current Time
- Current Date
- Current Day
- Current Year

### Interactive Commands
- Greetings
- Motivational Quotes
- Fun Facts
- Jokes
- Study Tips
- Small Talk Responses

### Feedback System
- User rating before exit
- Suggestion collection feature
- Unknown command handling

### GUI Features
- Modern chat bubble interface
- User messages aligned right
- Bot messages aligned left
- Scrollable chat window
- Fixed-size responsive design
- Sound notifications
- Keyboard Enter support


## Technologies Used

- Python 3
- Tkinter
- Winsound (Windows)
- Datetime Module


## Project Structure

```
Rule_based_ai_chatbot/
│
├── chatbot.py
├── README.md
├── requirements.txt
├── .gitignore
└── assets/
```


## Available Commands

### Greetings

- hello
- hi
- hey
- good morning
- good afternoon
- good evening
- good night

### Information

- time
- date
- day
- year
- creator
- version
- skills

### Fun Commands

- joke
- quote
- motivate
- fun fact
- study

### Personalization

- my name is <name>
- who am i
- about me
- change my name to <name>

### Feedback

- suggest <your suggestion>
- rate 1
- rate 2
- rate 3
- rate 4
- rate 5

### Other

- thanks
- ok
- okay
- cool
- nice
- awesome
- help
- commands
- bye


## How It Works

DecodeBot uses a Rule-Based approach.

Each user input is matched against predefined conditions using Python's conditional statements.

Example:

```python
elif msg == "time":
    return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
```

Unlike AI chatbots, DecodeBot does not use Machine Learning or Large Language Models.


## Running The Project

### Clone Repository

```bash
git clone https://github.com/yourusername/decodebot.git
```

### Open Project

```bash
cd decodebot
```

### Run

```bash
python chatbot.py
```


## Future Improvements

- Store user suggestions in a file
- Export feedback reports
- Theme switching
- User profiles
- SQLite database integration
- Voice interaction

---

## Author

Pratyaksha Singh
Developed during the DecodeLabs AI Internship.

---

## License

This project is for educational and learning purposes.