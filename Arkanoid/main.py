import math
from tkinter import *


class Window:
	"""Класс Окно"""
	
	def __init__(self, width, height, color = "black"):
		"""Конструктор Окна принимает ширину окна, высоту окна, цвет фона.
				Создает холст. Создает заготовки различных надписей"""
		# Создание и сохранения холста, на котором будут располагаться все графические примитивы:
		self.canvas = Canvas(root, width = width, height = height, bg = color)
		self.canvas.pack()  # Упаковка холста в окно
		self.canvas.focus_set()  # Фокусировка ввода (например, нажатия клавиш) на холсте.
		self.width = width
		self.height = height
		self.text_HP = self.canvas.create_text(60, 20, fill = "dark red", text = "Health: 3", font = "Tahoma 18")
		self.text_end_game = self.canvas.create_text(self.getCenterX(), self.getCenterY() + 100, fill = "green",
		                                             text = "", font = "Tahoma 62")
		
	def getCanvas(self):
		return self.canvas
	
	def getWidth(self):
		return self.width
	
	def getHeight(self):
		return self.height
	
	def getCenterX(self):
		return self.width / 2
	
	def getCenterY(self):
		return self.height / 2


class Ball:
	"""Класс Мяч"""
	
	def __init__(self, window, radius, position_X, position_Y, color = "white"):
		"""Конструктор Мяча принимает объект класса Window, в котором мяч будет отрисовываться,
				радиус мяча, начальную позицию по X и Y, цвет мяча.
				Задает мячу начальную скорость, сохраняет значения радиуса, ссылку на холст.
				Создает графический примитив (овал) для отрисовки мяча на холсте."""
		self.speed_X = 0
		self.speed_Y = 0
		self.canvas = window.getCanvas()
		self.radius = radius
		self.oval = self.canvas.create_oval(position_X - radius, position_Y - radius, position_X + radius,
		                                    position_Y + radius, fill = color)
	
	def changePosition(self, x, y):
		"""Метод принимает вектора по X и Y, на которые изменит текущее местоположение мяч."""
		self.canvas.move(self.oval, x, y)
	
	def setPosition(self, x, y):
		self.canvas.coords(self.oval, x - self.radius, y - self.radius, x + self.radius, y + self.radius)
	
	def fly(self):
		"""Метод перемещает мяч в зависимости от текущей скорости."""
		self.changePosition(self.speed_X, self.speed_Y)
	
	def getSpeedX(self):
		return self.speed_X
	
	def getSpeedY(self):
		return self.speed_Y
	
	def setSpeed(self, x, y):
		"""Метод принимает числа - скорости по оси X и Y.
		Устанавливает мячу принятые скорости."""
		self.speed_X = x
		self.speed_Y = y
	
	def bounce(self, axis):
		"""Метод принимает строку - ось, по которой мяч отобьется.
		Изменяет скорость на противопожную по принятой оси."""
		if axis == 'x':
			self.speed_X *= -1
		elif axis == 'y':
			self.speed_Y *= -1
	
	def getCoords(self, side):
		"""Метод принимает строку-сторону.
		Возвращает координаты крайней точки запрашиваемой стороны."""
		if side in (0, 'l', 'left'):
			return self.canvas.coords(self.oval)[0]
		elif side in (1, 't', 'top'):
			return self.canvas.coords(self.oval)[1]
		elif side in (2, 'r', 'right'):
			return self.canvas.coords(self.oval)[2]
		elif side in (3, 'b', 'bottom'):
			return self.canvas.coords(self.oval)[3]
		elif side in ('cx', 'center-x'):
			return (self.getCoords('l') + self.getCoords('r')) / 2
		elif side in ('cy', 'center-y'):
			return (self.getCoords('t') + self.getCoords('b')) / 2
	
	def angular_bounce(self, angle):
		S = math.sqrt(self.speed_X ** 2 + self.speed_Y ** 2)
		self.speed_Y = -S * math.sin(math.radians(angle))
		self.speed_X = S * math.cos(math.radians(angle))

class Pad:
	"""Класс Ракетка"""
	
	def __init__(self, window, width, height, position_X, position_Y, color = "white"):
		"""Конструктор Ракетки принимает объект класса Window, в котором ракетка будет отрисовываться,
			ширину, высоту, начальную позицию по осям X и Y, цвет ракетки.
			Задает ракетке начальную нулевую скорость, сохраняет значения размера, ссылку на холст.
			Создает графический примитив (прямоугольник) для отрисовки ракетки на холсте."""
		self.speed = 0
		self.canvas = window.getCanvas()
		self.size = width
		self.rectangle = self.canvas.create_rectangle(position_X - width / 2, position_Y - height / 2,
		                                              position_X + width / 2, position_Y + height / 2, fill = color)
	
	def changePosition(self, x, y):
		"""Метод принимает вектора по X и Y, на которые изменит текущее местоположение ракетка."""
		self.canvas.move(self.rectangle, x, y)
	
	def move(self):
		"""Метод перемещает ракетку в зависимости от текущей скорости."""
		self.changePosition(self.speed, 0)
	
	def setSpeed(self, x):
		self.speed = x
	
	def getSize(self):
		return self.size
	
	def getCoords(self, side):
		"""Метод принимает строку-сторону.
		Возвращает координаты крайней точки запрашиваемой стороны."""
		if side in (0, 'l', 'left'):
			return self.canvas.coords(self.rectangle)[0]
		elif side in (1, 't', 'top'):
			return self.canvas.coords(self.rectangle)[1]
		elif side in (2, 'r', 'right'):
			return self.canvas.coords(self.rectangle)[2]
		elif side in (3, 'b', 'bottom'):
			return self.canvas.coords(self.rectangle)[3]
		assert False, "Wrong side"


class Brick:
	
	def __init__(self, window, width, height, pos_x, pos_y, color = "green"):
		self.__canvas = window.getCanvas()
		self.__width = width
		self.__height = height
		self.__rectangle = self.__canvas.create_rectangle(pos_x - self.__width / 2, pos_y - self.__height / 2,
		                                                  pos_x + self.__width / 2, pos_y + self.__height / 2,
		                                                  fill = color, outline = None)
	
	def get_wight(self):
		return self.__width
	
	def get_height(self):
		return self.__height
	
	def getCoords(self, side):
		"""Метод принимает строку-сторону.
		Возвращает координаты крайней точки запрашиваемой стороны."""
		if side in (0, 'l', 'left'):
			return self.__canvas.coords(self.__rectangle)[0]
		elif side in (1, 't', 'top'):
			return self.__canvas.coords(self.__rectangle)[1]
		elif side in (2, 'r', 'right'):
			return self.__canvas.coords(self.__rectangle)[2]
		elif side in (3, 'b', 'bottom'):
			return self.__canvas.coords(self.__rectangle)[3]
	
	def __del__(self):
		try:
			self.__canvas.delete(self.__rectangle)
		except:
			pass

class Controller:
	"""Класс Контроллер.
		Сущность, управляющая игровыми объектами (мяч, ракетка, кирпичи).
		Отслеживает состояние игры (победа, поражение, гол, попадание по кирпичу)."""
	
	def __init__(self, window, ball, pad, bricks):
		"""Конструктор Контроллера.
			Принимает объекты, которыми будет управлять контроллер: окно, мяч, ракетку.
			Устанавливает начальное состояние игры: начальную скорость мяча.
			Сохраняет ссылки на контролируемые объекты."""
		self.window = window
		self.ball = ball
		self.ball.setSpeed(0, 10)
		self.pad = pad
		self.bricks = bricks
		self.HP = 3
	
	def ballMovement(self):
		"""Управление движением мяча."""
		self.ball.fly()
		
		# Отбитие мяча от стен:
		if (self.ball.getCoords('l') <= 0) or (
				self.ball.getCoords('r') >= self.window.getWidth()):  # Если мяч касается или входит в боковые стенки,
			self.ball.bounce('x')  # отбиться по горизонтали.
		elif self.ball.getCoords('t') <= 0:  # Если мяч касается или входит в верхнюю стенку,
			self.ball.bounce('y')  # отбиться по вертикали
		
		# Отбитие мяча от ракетки:
		if (self.pad.getCoords('t') <= self.ball.getCoords('b') <= self.pad.getCoords('b')) and (
				self.pad.getCoords('l') <= self.ball.getCoords('cx') <= self.pad.getCoords(
			'r')):  # Если мяч касается или входит в ракетку,
			# self.ball.bounce('y')  # отбиться по вертикали
			self.ball.angular_bounce(self.get_pos_ball_pad())
		
		# Breaking bricks
		for brick in self.bricks:
			pos = self.get_pos_ball_brick(self.ball, brick)
			if pos != None:
				if pos in {0, 180}:
					self.ball.bounce('x')
					self.bricks.remove(brick)
				elif pos in {90, 270}:
					self.ball.bounce('y')
					self.bricks.remove(brick)
				else:
					assert False, "Wrong returned position of touch"
		
		if self.goal():
			self.ball.setPosition(self.window.getCenterX(), self.window.getCenterY())
			self.HP -= 1
			self.window.canvas.itemconfig(self.window.text_HP, text = "Health: {}".format(self.HP))
			if not self.HP:
				self.ball.setSpeed(0, 0)
				self.window.canvas.itemconfig(self.window.text_end_game, text = "YOU LOSE", fill = "red")
		
		if self.win():
			self.ball.setPosition(self.window.getCenterX(), self.window.getCenterY())
			self.ball.setSpeed(0, 0)
			self.window.canvas.itemconfig(self.window.text_end_game, text = "YOU WIN")
	
	def win(self):
		return not len(self.bricks)
	
	def goal(self):
		return self.ball.getCoords("cy") > self.window.getHeight()
		
	def get_pos_ball_pad(self):
		delta_x = self.pad.getCoords("r") - self.ball.getCoords("cx")
		angle = 30 + ((150 - 30) / self.pad.getSize()) * delta_x
		return angle
	
	def get_pos_ball_brick(self, ball, brick):
		br_x_1, br_x_2 = brick.getCoords('l'), brick.getCoords('r')
		br_y_1, br_y_2 = brick.getCoords('t'), brick.getCoords('b')
		for angle in range(0, 360, 90):
			if angle == 0:
				x = self.ball.getCoords('r')
				y = self.ball.getCoords('cy')
				if (br_x_1 <= x <= br_x_2) and (br_y_1 <= y <= br_y_2):
					return 0
			elif angle == 90:
				x = self.ball.getCoords('cx')
				y = self.ball.getCoords('t')
				if (br_x_1 <= x <= br_x_2) and (br_y_1 <= y <= br_y_2):
					return 90
			elif angle == 180:
				x = self.ball.getCoords('l')
				y = self.ball.getCoords('cy')
				if (br_x_1 <= x <= br_x_2) and (br_y_1 <= y <= br_y_2):
					return 180
			elif angle == 270:
				x = self.ball.getCoords('cx')
				y = self.ball.getCoords('b')
				if (br_x_1 <= x <= br_x_2) and (br_y_1 <= y <= br_y_2):
					return 270
			else:
				assert False
	
	def padMovement(self):
		"""Управление движением ракетки."""
		# Двигать ракетку с текущей скоростью
		self.pad.move()
	
	def padStartMove(self, event):
		"""Задание ракетке скорости движения при нажатии клавиш управления."""
		if event.keysym == "Left":
			self.pad.setSpeed(-10)
		elif event.keysym == "Right":
			self.pad.setSpeed(10)
	
	def padStopMove(self, event):
		"""Аннулирование скорости движения ракетки при отпускании клавиш управления."""
		if event.keysym in ("Left", "Right"):
			self.pad.setSpeed(0)


def main():
	"""Главная функция"""
	c.ballMovement()  # Двигать мяч
	c.padMovement()  # Двигать ракетку
	root.after(30, main)  # Повторно вызвать главную функцию через 30 мсек


root = Tk()  # Создание окна
root.title('GeekSchool Arkanoid')  # Изменение заголовка окна

w = Window(1200, 800)  # Создание окна арканоида

level = []
level.append(Brick(w, 100, 50, 150, 100, "blue"))
level.append(Brick(w, 120, 60, 450, 150, "red"))
level.append(Brick(w, 100, 60, 650, 150, "red"))
level.append(Brick(w, 100, 60, 850, 150, "red"))

# Создание контроллера:
c = Controller(w, Ball(w, 10, w.getCenterX(), w.getCenterY(), "dark red"),
               Pad(w, 200, 30, w.getCenterX(), w.getHeight() - 30, "dark blue"), level)

# Привязка нажатия и отпускания клавиш к функциям изменения скорости ракетки:
w.getCanvas().bind("<KeyPress>", c.padStartMove)
w.getCanvas().bind("<KeyRelease>", c.padStopMove)

main()
root.mainloop()
