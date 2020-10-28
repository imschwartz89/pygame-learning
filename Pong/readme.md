# Pong
Using pygame to create the simple game Pong. 

## Requirements
Python 3 (tested on Python 3.6.8)
<br />pygame (tested on version 1.9.6)
<br />*NOTE: Will not work with Python 2*

## Files
**pong.py** - the 'final product' (still a work in progress)
<br />**betaPong.py** - testing place (the beta version) before putting new code into **pong.py**
<br />**squares.py** - testing place for anything to do with pygame, to avoid messing up **pong.py** or **betaPong.py**

## How to Use
Execute the code using on the terminal(UNIX): `python3 <filename>.py`
<br />Example: `python3 pong.py`
<br />This will run the pong file and allow you to play pong.

<br />The left paddle is controlled with W and S keys.
<br />The right paddle is controlled with the UP and DOWN arrow keys.

## Future Work
- [ ] Fix ball trapped in paddle bug
- [ ] Fix direction ball travels after point is scored
- [ ] Find "best" speed for the game
- [ ] Use blit instead of drawing everything
