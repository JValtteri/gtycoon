# gtycoon
A small game made in Python3, about managing a semiconductor company (microprosessors/cpus/gpus).
The player manages research. Outlines products for a year at a time. The player must balanse the 
chip size with the expected yeald, factory overclocking, and chip cost against the competitors.

I'm trying to keep the game platform independent. At minimum so it would run on both **Linux** and 
**Windows**, but Android as well.

**The game has no UI**, but the command line, though one is planned... possibly in Qt.

### This game is in no way complete!

## How to install 

 1. Make sure you have **[Python3.6](https://www.python.org/downloads/)** or newer installed.
 2. Clone or **[download](https://github.com/JValtteri/gtycoon/archive/master.zip)** the game 
 3. and extract in any folder you like.
 4. Install dependencies if you don't have them already (listed in requirements.txt)
     1. Can be done by running *setup.bat* (on Windows) 
     2. or *setup.sh* (on Linux)
 5. You are ready. 
     1. You can run the game by running gtycoon.py directly 
     2. or on linux, run *run.sh*
     
Ideally use one of the **[releases](https://github.com/JValtteri/gtycoon/releases/)**, but genarally anything in the *master* branch should be stable.

## Use

#### Saving
The game is auto-saved at the start of every round (1 year). No seperate *save button* exists.

There is only one save slot, and it is used by the auto-save. 

You can continue the game by choosing *Continue* in the main menu.

#### New Game
By choosing *New Game* You can choose the number of human and AI players for a new game.

Names for players are auto-assigned randomly.

#### Quick Game 
*Quick Game* creates a new game with one human and one AI player. It is the default game mode and what the game was designed for.

## Game status - Current features

 - Sigleplayer vs one AI player is now possible.
 - Each player can have a maximum of 4 products in market.
   Exceding that number causes the oldest chip to be discarded
   or a chip of players choosing.
 - ~~Market is modelled in a dumb way: Customers will buy a more~~
   ~~expensive product, even if there is a cheaper and a much more~~
   ~~powerfull competitor in the market, just because the first~~
   ~~chip is the most expensive in their budjet.~~ (overhauled)
 - Market is still modelled in a sub-optimal way and some customers
   will buy an objectivelly "worse product" over a same priced 
   competitor.
 - Simple "Headlines" for chip announcements
 - Single line of architecture research
 - Node research
 - Autosave and Load game
 - Multiplayer with multiple AI players (multiplayer with humans not tested)

### Planned features:

 - Storymode/Tutorial to help teach the game concepts, but also, above all: **ENTERTAIN!**
 - Multiplayer with multiple human and ~~AI players~~ (sort of implemented but not tested)
 - Random variation in default market and costs
 - "News" game events and acheavements
 - Endgame 
   - scoring system
   - possibility for declared bankruptsy
 - Multiple architecture research options with different pros and conns (and some luck)
 - UI in QT (PySide), PyGame or other...
 - Difficulty levels for AI

### Known bugs:

 - ~~Total market (total sales) go down every year~~ Scaled market size is disabled for now.
 - ~~Ai doesn't research properly~~
 - ~~Entering non-numbers in to numbers fields may cause a crash~~
 - ~~Entering an out of index will cause a crash.~~
 - ~~Performance vs. Price (PVP) metric behaves strangely~~
 - ~~Some "product reviews" are harsher than expected.~~
 - Entering funny stuff to "overdrive" will cause a crash

### **I'm happy to accept contributions, especially: UI and market algorithms as well as bug fixes**
