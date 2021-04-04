# Game Of Life
This app takes user inputs from a tkinter gui and uses those inputs to play Conway's Game Of Life.

The aim of the game is to show how natural behaviours like birth, growth and dead of living organisms, who interact with each other in a common environment, can be described with mathematical models and rules.
This game is a zero-player game: the user only has to provide the initial state and this state evolves based on simple rules.

## Rules
The game is played in a board: every tile of the board corresponds to a cell which can be active or inactive, at the initial state. Once the user starts the game, the subsequent states are computed for each cells considering the 8 surrounding neighbours. The rules are:

- Each populated location with one or zero neighbors dies (**loneliness**).
- Each populated location with four or more neighbors dies (**overpopulation**).
- Each populated location with two or three neighbors survives.
- Each unpopulated location becomes populated if it has exactly three populated neighbors (**birth**). 
- All updates are performed simultaneously **in parallel**.


## Implementation
The game has been implemented by using thinter and pygame .

## Functionalities
The GUI appears like: 

<img width="751" src="img/Screenshot from 2021-04-04 10-20-41.png">
<img width="751" src="img/Screenshot from 2021-04-04 10-21-03.png">
The user has to select width and height of the grid and click 'GO' button

This implementation provides some functionalities:
- **Start/Pause **: The user can start playing the game or pasue the game by clicking on the start/pause button.
- **Next Life**: The user can see just the next iteration of life by pasuing the game an clicking 'next life'.
- **Start Over**: The user can reStart the current configuration .
- **Random**: TTo generate random pattern and play.
- **Clear**: The user can clear all the board by clicking on the clear button.
- **Erase/Draw**: The user can toggle between earase mode and draw mode of cursor.



## Instructions
Pre-requisite: You need Python 3+

### Download Pygame
Follow the instructions for downloading the latest 64-bit version of Pygame for Python 3+ [from here](https://www.webucator.com/blog/2015/03/installing-the-windows-64-bit-version-of-pygame/ "Install The Windows 64-bit Version Of Pygame"). 
or
```
pip3 install pygame
```
### Download the script and run it
```
git clone https://github.com/shreyas2000/JdeRobot_challanges.git
cd JdeRobot_challanges
cd ConwaysGOF
python3 main.py
```
