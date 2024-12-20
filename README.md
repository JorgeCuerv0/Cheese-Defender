# Cheese Defender

Cheese Defender is a fun and challenging survival game where you must protect your precious cheese from waves of invading roaches. Different roach types with unique behaviors add variety and difficulty, keeping players on their toes. Your goal? Swat as many roaches as you can and rack up points before the cheese gets taken over!

## Game Overview

In Cheese Defender, the player is tasked with protecting a piece of cheese from an onslaught of roaches. You earn points for every roach you successfully swat, but watch out—each roach type behaves differently, and the game gets progressively harder. The game ends when a single roach touches the cheese.

### Objective

- **Protect the cheese for as long as possible.**
- **Swat roaches to gain points.**

### Game Over Condition

- The game ends if a roach touches the cheese.

---

## Gameplay Mechanics

### Game Entities

1. **Cheese**
   - **Position:** Center of the screen.
   - **Condition:** Game ends if a roach touches it.

2. **Roaches**
   - **Normal Roach:** Moves directly toward the cheese at a standard speed.
   - **Fast Roach:** Smaller in size and moves faster than the normal roach.
   - **Tipsy Roach:** Moves in a curvy, unpredictable path, making it harder to hit.
   - **Big Boy Roach:** 
     - Takes two hits to kill.
     - First hit reduces speed and makes it jump to a new position.
     - Second hit eliminates it.

3. **Player Actions**
   - **Swat:** Click on roaches to swat them.
     - Normal and tipsy roaches die in one hit.
     - Big Boy roaches require two hits.

4. **Difficulty Scaling**
   - Over time, the number of roaches increases, and their speed scales up.

---

## Features

### Heads-Up Display (HUD)
- **Timer:** Tracks the time elapsed since the start of the game.
- **Score Counter:** Displays points earned from kills.

### Event Handling
- **Mouse Clicks:** Used to swat roaches.
- **Timer Events:** Updates the game state, including roach movement and difficulty scaling.

### Win/Lose Conditions
- **Win:** Survival game—there is no winning state.
- **Lose:** A roach touches the cheese.

---

## Controls

- **Mouse Click:** Swat roaches.
- **R Key:** Restart the game after a game over.
- **Q Key:** Quit the game.

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/JorgeCuerv0/Cheese-Defender.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Cheese-Defender
   ```
4. Install required dependencies:
   ```bash
   pip install pygame
   ```
5. Run the game:
   ``` bash
   python cheese_defender.py
   ```
## How to Play

Protect the cheese at the center of the screen by clicking on approaching roaches.  
Each swat earns points:  
- **Normal Roach:** 1 hit  
- **Fast Roach:** 1 hit  
- **Tipsy Roach:** 1 hit  
- **Big Boy Roach:** 2 hits  

The game **ends** when any roach reaches the cheese.  
Restart the game by pressing `R` or quit by pressing `Q`.

---

## Challenges Overcome

- Implementing different behaviors for each roach type (e.g., swirling movement for tipsy roaches).  
- Managing increasing difficulty through dynamic roach spawning and scaling speed.  
- Designing an intuitive user interface with real-time score and time tracking.

---

## Future Enhancements

- Add power-ups (e.g., freeze all roaches for a few seconds).  
- Include leaderboard functionality for high scores.  
- Implement additional roach types for variety.  
- Introduce sound effects for swats and game over events.

---

## Credits

- **Author:** Jorge Sandoval  
- **Assignment:** SMC CS 87 - Assignment 9  
- **Date:** November 14, 2024  

---

## License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute as per the terms of the license.

---

Enjoy defending your cheese!


 

