# gtycoon
A simple game made in Python3, about managing a semiconductor company (microprosessors/cpus/gpus).
The player manages research. Outlines products for a year at a time. The player must balanse the 
chip size with the expected yeald, factory overclocking, and chip cost against the competitors.

The game has no UI, but the command line, though one is planned... possibly in Qt.

## Game status - Current features

 - Sigleplayer vs one AI player is now possible.
 - Each player can have a maximum of 3 products in market.
   Exceding that number causes the oldest chip to be discarded
 - Market is modelled in a dumb way: Customers will buy a more 
   expensive product, even if there is a cheaper and a much more 
   powerfull competitor in themarket, just because the first 
   chip is the most expensive in their budjet.
 - Simple "Headlines" for chip announcements (broken)
 - Single line of architecture research
 - Node research

### Planned features:

 - Multiplayer with AI players
 - Saving games
 - Random variation in default market and costs
 - "News" game events and acheavements
 - Endgame scoring system
 - Multiple architecture research options with different pros and conns (and some luck)
 - UI in QT or other...
