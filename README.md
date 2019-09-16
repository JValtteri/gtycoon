# gtycoon
A small game made in Python3, about managing a semiconductor company (microprosessors/cpus/gpus).
The player manages research. Outlines products for a year at a time. The player must balanse the 
chip size with the expected yeald, factory overclocking, and chip cost against the competitors.

I'm trying to keep the game platform independent. At minimum so it would run on both **Linux** and 
**Windows**, but Android as well.

**The game has no UI**, but the command line, though one is planned... possibly in Qt.

### This game is in no way complete!

## Game status - Current features

 - Sigleplayer vs one AI player is now possible.
 - Each player can have a maximum of 3 products in market.
   Exceding that number causes the oldest chip to be discarded
 - Market is modelled in a dumb way: Customers will buy a more 
   expensive product, even if there is a cheaper and a much more 
   powerfull competitor in themarket, just because the first 
   chip is the most expensive in their budjet.
 - Simple "Headlines" for chip announcements (buggy)
 - Single line of architecture research
 - Node research

### Planned features:

 - Multiplayer with multiple human and AI players
 - Saving/loading games
 - Random variation in default market and costs
 - "News" game events and acheavements
 - Endgame 
   - scoring system
   - possibility for declared bankruptsy
 - Multiple architecture research options with different pros and conns (and some luck)
 - UI in QT (PySide), PyGame or other...

### Known bugs:

 - Total market (total sales) go down every year
 - Ai doesn't research properly
 - Entering non-numbers in to numbers fields may cause a crash
 - Entering an out of index will cause a crash.
 
### **I'm happy to accept contributions, especially: UI and market algorithms as well as bug fixes**
