#!/usr/bin/env python3
import curses  #pip install curses -> linux | pip install windows-curses
from curses import textpad
import curses.ascii
import time, os, json
from random import randint, choice
import threading

#creating global variables
MENU = ['Home','Play','Help','Exit']
MARGIN = 3
SYSTEM = os.name.upper()
SNAKE_BODY = chr(9604) if SYSTEM=='NT' else chr(10074)
SNAKE_FOOD = [9455,9689,111] if SYSTEM=='NT' else [10083,10022,111,10038] 
_thread = False
confirmn_options = ['yes','no']

def print_menu(stdscr, current_row):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	for i,r in enumerate(MENU):
		x = w//2 - len(r)
		y = h//2 - (len(MENU)//2) + i + i  
		if i == current_row:
			stdscr.addstr(y,x,f'< {r} >'.upper().center(8) )
			stdscr.chgat(y,x+2,4, curses.color_pair(1) | curses.A_BOLD)
		else:
			stdscr.addstr(y,x,r.center(8))
	stdscr.refresh()

def get_highscore():
	global highscore
	try:
		if os.path.exists('.high_score.json'):
			with open('.high_score.json') as file:
				info = json.loads(file.readline())
			if info['exec']['hs'].isdigit(): highscore = info['exec']['hs']
			else: highscore = 0 
		else: info=None; highscore=0
	except:
		highscore = 0; info=None
	return info

def home(stdscr):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	title='Home Page'.upper()
	player = os.getlogin() if os == "name" else os.getenv('USER')
	info = get_highscore()
	lastplayed=info['exec']['time'] if info !=None else ' --- '
	stdscr.addstr(h//4,w//2-len(title)//2, title, curses.A_BOLD | curses.color_pair(3) )
	stdscr.addstr(h//4+2, w//2-len(''.center(20))//2,f'System Name: {SYSTEM}')
	stdscr.addstr(h//4+4,w//2-len(''.center(20))//2,f'Player Name: {player.upper()}')
	stdscr.addstr(h//4+6, w//2-len(''.center(20))//2,f'Last Played: {lastplayed}')
	stdscr.addstr(h//4+8, w//2-len(f'High Score : {highscore}'.center(20))//2,f'High Score: {highscore}')
	stdscr.getch()
	
def show_doc(stdscr):
	#curses.newwin(nlines, ncols, start_y, start_x)
	screen = curses.newwin(curses.LINES - 2, curses.COLS - 2 , 1, 1)
	window = screen.subwin(curses.LINES - 4, curses.COLS - 4 , 2, 2)
	text = 'Help Menu:\n\n  Home -> Just the Home page with Options\n\n  Play -> Take you to play a game\n\n  Help -> Display docs of the options\n\n  Exit -> Exit from the program\n\n  Esc  -> Quit from the program\n\n  Q    -> Move back to main page.'
	window.addstr(text)
	window.chgat(0,0,10, curses.color_pair(2) | curses.A_BOLD | curses.A_TOP)
	window.refresh()
	screen.refresh()
	while 1:
		key = screen.getch()
		if key == ord('q'):
			break

def rotate_text(stdscr,w):
	stdscr.addstr(3,w//2 - len('Have some fun')//2, 'Have-Some-Fun')
	text = 'Keeping Playing with snake.  '
	for i in range(50):
		if _thread is True:
				break
		else:
			for j in range(len(text)+2):
				p = (i+j)%len(text)
				stdscr.addstr(0,w//2 - len(text)//2 + j ,text[p],curses.color_pair(2) | curses.A_UNDERLINE)
		stdscr.refresh()
		time.sleep(0.3)
	stdscr.addstr(0,1,' '*int(curses.COLS-2))
	stdscr.refresh()	

def print_score(stdscr, score):
	h, w = stdscr.getmaxyx()
	text = f'Your Score: {score}'
	stdscr.addstr(1,w//2 - len(text)//2, text)
	stdscr.refresh()

def create_food(snake,uly,ulx,lry,lrx):
	food = None
	while food is None:
		food = [randint(uly+1,lry-1), randint(ulx+1,lrx-1)]
		if food in snake:
			food = None
	return food

def play(stdscr):
	stdscr.nodelay(1)
	stdscr.timeout(150)
	sh,sw = stdscr.getmaxyx()
	box = [MARGIN,MARGIN,sh-MARGIN, sw-MARGIN]
	dict_box = {'uly':MARGIN,'ulx':MARGIN,'lry':sh-MARGIN ,'lrx':sw-MARGIN}
	textpad.rectangle(stdscr, **dict_box)
	
	#initializing snaze direction to move
	snake = [[sh//2,sw//2+1],[sh//2,sw//2],[sh//2,sw//2-1]]
	direction = curses.KEY_RIGHT
	allowedDirections = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]
	
	for i,j in enumerate(snake):
		y=j[0]; x=j[1]
		stdscr.addstr(y,x,SNAKE_BODY)
	
	#creating position
	food_pos = create_food(snake, **dict_box)
	food = chr(choice(SNAKE_FOOD))
	stdscr.addstr(food_pos[0], food_pos[1], food, curses.color_pair(3))

	#initializing the score
	score = 0 
	print_score(stdscr, score)
	get_highscore()
	thread_1  = threading.Thread(target=rotate_text, args=(stdscr,sw), daemon=True)
	thread_1.start()
	
	#infinite loop 
	while 1:
		key = stdscr.getch()
		if key == ord('q'):
			return;
		
		head = snake[0]
		if key in allowedDirections:
			direction = key

		#changing direction according the arrow keys
		if direction == curses.KEY_RIGHT:
			new_head = [head[0], head[1]+1]
		elif direction == curses.KEY_LEFT:
			new_head = [head[0], head[1]-1]
		elif direction == curses.KEY_UP:
			new_head = [head[0]-1, head[1]]
		elif direction == curses.KEY_DOWN:
			new_head = [head[0]+1, head[1]]

		snake.insert(0, new_head)
		stdscr.addstr(new_head[0], new_head[1],SNAKE_BODY)
		
		#creates a new food when snake reaches the food
		if snake[0] == food_pos:
			food_pos = create_food(snake, **dict_box)
			food = chr(choice(SNAKE_FOOD))
			stdscr.addstr(food_pos[0], food_pos[1], food, curses.color_pair(3))
			score+=1
			print_score(stdscr,score)
		else:
			stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
			snake.pop()

		#condition to check whether snake touched the boundry
		if (snake[0][0] in [3,sh-3] or snake[0][1] in [3,sw-3] or snake[0] in snake[1:]):
			
			msg1 = "Game Over!!"; msg2='Press "Q" to quit'
			score = score if score > int(highscore) else int(highscore)
			localtime=time.localtime()
			t=time.strftime(r'%d/%m/%y %I:%M:%S %p',localtime)
			dic = {'exec':{'hs':str(score),'time':t}}
			
			with open('.high_score.json','w') as file:
				file.write(json.dumps(dic))
			
			stdscr.addstr(sh//2,(sw//2 - len(msg1)//2),msg1, curses.A_BOLD | curses.color_pair(1) | curses.A_BLINK)
			stdscr.addstr(sh//2 + 3,(sw//2 -len(msg2)//2),msg2)
			stdscr.nodelay(0)
			key = stdscr.getch()
			if key == ord('q'):
				break
		stdscr.addstr(curses.LINES - 2, 3, 'Press "Q" to quit.')
		stdscr.addstr(curses.LINES - 2, curses.COLS - 10, f'Hit: {highscore}')
		stdscr.chgat(curses.LINES -2, 10, 1, curses.A_BOLD| curses.color_pair(1))
		stdscr.refresh()


def main(stdscr):
	curses.curs_set(0)
	curses.mousemask(1)
	curses.init_color(curses.COLOR_BLACK, 150, 150, 150)
	curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
	current_row=0
	print_menu(stdscr,current_row)
	while 1:
		try:
			_, mouse_x, mouse_y, _, _ = curses.getmouse()
		except Exception as e:
			pass
		
		h, w = stdscr.getmaxyx()

		key = stdscr.getch()
		stdscr.clear()
		
		try:
			if (mouse_y == h//2 - (len(MENU)//2)+2) and mouse_x==(w//2 - 4):
				home(stdscr)
		except:
			pass
		if key == curses.KEY_UP and current_row > 0:
			current_row-=1
		elif key == curses.KEY_DOWN and current_row < len(MENU)-1:
			current_row+=1
		elif key == curses.KEY_ENTER or key in [10,13]:
			if current_row == len(MENU) -1:
				break
			elif current_row == 0:
				home(stdscr)
			elif current_row == 1:
				play(stdscr)
			elif current_row == 2:
				show_doc(stdscr)
		elif key == 27 or key == ord('q'):
			break
		print_menu(stdscr,current_row)
		stdscr.refresh()


curses.wrapper(main)