# 2048-Versus

This is a multiplayer version of the classic 2048 game developed using `wxPython`. The motivation behind building this project stemmed from the desire to create a competitive version of 2048, as my brother and I enjoyed the game but lacked a structured way to determine who was the better player.

In this version of the classic 2048 game, two players compete side by side on separate 2048 boards to achieve the highest score or tile within a specified time limit. Player 1 controls the game using the WASD keys, while Player 2 uses the arrow keys. The game is designed to be an engaging, head-to-head competition, with the goal of outscoring or out-tiling your opponent before time runs out. The trade-off is speed vs accuracy of moves.

<br/>

## The Game

**Objectives**
- Combine tiles with the same number to form larger numbers.
- Try to reach the highest tile possible (2048 or more).
- The player with the highest tile wins, and in case of a tie, the player with the higher score wins. If both score and tile are tied, the game results in a tie.

**The game ends if either**
  - The timer runs out.
  - Both players have no more valid moves.

<br/>

## Installation

### Prerequisites:
- Python 3.x
- wxPython (for GUI)
- `game.py` and `config/colors.py` (containing game logic and tile color mapping)

### Step 1: Clone the Repository

```bash
git clone https://github.com/madhav1310/2048-Versus.git
cd 2048-Versus
```

### Step 2: Set Up the Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```
pip install -r requirements.txt
```

### Step 4: Run the Game
```
python main.py
```

<br/>

## Gameplay

https://github.com/user-attachments/assets/7f32bcb6-26e0-4722-9c62-5490368adbaa




