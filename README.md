# StarChaser
Welcome to StarChaser! A 3D platformer built in a 2D game engine.

Play it here:
http://www.codeskulptor.org/#user40_8JsR8RS3rmVcn5N.py

Game includes two modes. “Chase” mode (two player) and “Time Trial” mode (single player). 

Chase mode utilizes split screen multiplayer (extremely optimized for codeskulptor, but not enough to run decently). Beware of keyboard ghosting with two player, keyboard buttons can be adjusted through constants at top of program. 

In single player mode players must try and go a set distance as fast as possible. Game records your fastest time and displays it on top of screen. Typically a player is competing against themselves: I found in this situation a separate high score page is less engaging than a “flappy bird” style highscore. Unskilled players may find it difficult to reach the required distance. Annoying death messages are there as motivation.

I keep two player mode as a feat of technical prowess; Single player is more fun. Two player mode can be disabled with the below TWO_PLAYER_ENABLED constant below. I recommend, in general, disabling two player. Maybe some day in the future codeskulptor will run fast enough for two player mode. I look forward to that day.

Note on code: it's pretty bad. Proper object oriented programming paradigms are not followed. Lots of global variables do obscure things. I would not expect someone to be able to figure out what's going on. Objects in this final version is very specifically made for this game. Earlier versions may better show 3D rendering engine at its best. (Note that I did not get polygon trimming right until very late versions) Here are links to the project at various stages to illustrate how 3D rendering is accomplished (there may be bugs):
Basic 3D OOP rendering:
http://www.codeskulptor.org/#user40_n76nGsSke6_20.py
Split Screen Multiplayer:
http://www.codeskulptor.org/#user40_3lQsilJfED_27.py
http://www.codeskulptor.org/#user40_3lQsilJfED_42.py
Prototype Game:
http://www.codeskulptor.org/#user40_X0HATLAfLW_12.py

For full version history see github:
https://github.com/Avery-Whitaker/Python-Game
Please forgive me on my crappy commit messages. I don’t expect anyone to need them ever anyway.

Original Pitch Sheet (Concept has since been revised)
http://www.averyw.me/RunNGunPoster.pdf
