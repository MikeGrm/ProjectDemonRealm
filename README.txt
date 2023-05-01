Files:

ProjectDemonRealmv2 - 30fps.py
>This file is the main game file, it was created originally as a test file that stemmed from the original game file to improve performance during gameplay. Game physics behaved
differently in 30fps so a lot of things had to be tweaked. This copy of the game became the main file after testing proved to improve performance.
It has v2 in it because it is the second version of my game with improved code. The original v1 was scrapped but in memory of it I have kept the v2 in the files name.

ProjectDemonRealmv2 - 120fps - outdated.py
>The original version of v2 that was created in an 120 fps limit environment. Severely outdated and is missing tons of key features. 

Assets
> These are the sprites and sound files that are used to create the images that display on your screen. This file is essential to running the game as without it
a ton of features would not load in. This folder makes up the environment, characters, hazards, and enemies that are present in the game aswell
as the sound effects, ambient noise, and music featured in the game. 

Project Overview:
This project is a 2d action platformer similar to many metroidvania type games where you control a main character that has the ability to attack with his katana and jump around, interacting with
the environment and enemy entities. The setting takes place in hell where you battle with mindless skeletons that patrol the game screen in an attempt to prevent you from effectively maneuvering around the map.
In addition to the hazard that are the enemies, fireballs will come flying in from offscreen as a product of the endless pools of lava and brimstone that occupy hell. These
projectiles are harmful and will do massive damage to your character. To fight back, the hero, hiei, can use his katana infused with demon energy, yoki, to cut down any foes that cross his path.
Your weapons will be ineffective against the balls of fire flying towards you though. As time progresses, and as you rack up points from being alive and killing enemies, more fireballs will
join the onslaught of projectiles and make it much more difficult to survive. After acquiring 50 points more fireballs will appear at 25 point intervals up to a maximum of 10. 
When you take damage your health with update in the GUI and you will enter a state of 'invincibility' where enemies will be unable to attack you to avoid them chaining together
attacks that deplete the entirety of your health bar in an absurd amount of time. When you get hit you will also bounce back and be disrupted, unable to take any action. 
When the game ends you will be met with a 'GAME OVER' screen that shows you your high score and allows you to restart the game back to square one. Upon initially starting up the game you
will be met with a start screen that introduces the game and informs you about the controls. A unique, overlooked, feature that is implemented is the ability to perform a 'soft jump' that
reduces your jump height to allow for greater player control and precision. Sound effects are implemented and add weight to your actions. The player character will grunt when performing
a jump, cry out in pain as he is hit, and whistle in the air as you swing your katana so fast you slice even the air in front of you. The ambient noise of a burning landscape softly plays in the
background under the theme music of the game as you fight to survive this thrilling assault in hell. 

How to start:
Simply run the code and you will be put into the action, no additional arguments or inputs are required to begin your journey.

Python packages:
Before starting you will need to download pygame onto your system as it is the core library that enables the game to run.

No output files are created by the code and the game runs entirely in the python file that is ProjectDemonRealmv2 - 30fps.py