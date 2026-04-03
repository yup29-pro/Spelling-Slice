# ✂️ Spelling Slice

An educational gamified spelling game built with Python & Pygame-CE.
Slice the flying letters to spell the target word — designed for kids aged 5–10!

---

## 🎮 How to Play

1. A target word is shown on screen
2. Letters fly around — slice the correct ones in order
3. Complete the word → hear it spelled out loud!
4. Wrong slice = lose a heart ❤️
5. Beat the timer for bonus points!

---

## 🏆 Levels

| Level           | Words                  | Speed  | Time |
|-----------------|------------------------|--------|------|
| 🟢 Beginner     | CAT, DOG, APPLE        | Slow   | 45s  |
| 🟡 Intermediate | MANGO, TIGER, GRAPE    | Medium | 35s  |
| 🔴 Advanced     | ELEPHANT, DOLPHIN      | Fast   | 25s  |

---

## 🛠️ Tech Stack

- Python 3.14
- [Pygame-CE](https://pyga.me/) — Game engine
- [gTTS](https://pypi.org/project/gTTS/) — Google Text to Speech

---

## ⚙️ Installation
```bash
# Clone the repo
git clone https://github.com/yup29-pro/Spelling-Slice.git
cd Spelling-Slice

# Install dependencies
pip install pygame-ce gtts

# Run the game
python main.py
```

---

## 📁 Project Structure
Spelling-Slice/
├── assets/
│   └── sounds/       # Generated audio files
├── settings.py       # Colors, screen size, constants
├── words.py          # Word lists for all 3 levels
├── menu.py           # Main menu screen
├── game.py           # Core slicing game logic
└── main.py           # Entry point

---

## 🔮 Future Scope

- Mobile version
- Leaderboard system
- More word categories
- Background music & animations

---

## 👨‍💻 Author

**Yashwanth R** — yup29-pro
(https://github.com/yup29-pro)
