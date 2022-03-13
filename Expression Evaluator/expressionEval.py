PRECEDENCES = { '*': 3, '/': 3, '+': 2, '-': 2, '(': 1, ')': 1 }
OPERATORS = [ '*', '/', '+', '-', '(' ]
VALIDCHARS = "+-*/()1234567890 "

from typing import List, Union
import pytesseract  # wrapper for Google's Tesseract OCR engine
import cv2
import numpy as np

def parseExpression(expression: str) -> List[Union[str, float]]:
	"""
	Converts a string of an infix (regular) expression into a list of strings/numbers.
	Eg:
	>>> parseExpression("1+2-3*(3-4)")
	[1.0, '+', 2.0, '-', 3.0, '*', '(', 3.0, '-', 4.0, ')']
	"""
	lst = []
	current = ""

	# Converting the string into a list of tokens (numbers and operators)
	for char in expression:
		if char == " ":  # ignore spaces, might be included in the input string unintentionally
			continue
		if char.isdigit() or char == ".":  # If the expression is a number or part of a number (eg float)
			current += char
		else:
			if current != "":
				lst.append(float(current))
				current = ""

			if char in PRECEDENCES:
				if (char in "+-") and (len(lst) == 0 or lst[-1] in OPERATORS):
					current = char
				else:
					lst.append(char)

	if current != "":
		lst.append(float(current))

	return lst


def infixToPostfix(expression: str) -> List[Union[str, float]]:
	"""
	Converts a string of an infix expression into a list of operators/numbers in postfix order.
	Eg:
	>>> infixToPostfix("1+2-3*(3-4)")
	[1.0, 2.0, '+', 3.0, 3.0, 4.0, '-', '*', '-']
	"""
	outlst = []
	stack = []

	for item in parseExpression(expression):
		# Handling right parenthesis:
		if item == ")":
			while stack[-1] != "(":
				outlst.append(stack.pop())
			stack.pop()

		# Handling numbers:
		elif type(item) == float or type(item) == int:
			outlst.append(item)

		# Handling let parenthesis:
		elif item == "(":
			stack.append(item)

		# Handling regular operators:
		else:
			while not len(stack) == 0 and PRECEDENCES[stack[-1]] >= PRECEDENCES[item]:
				outlst.append(stack.pop())
			stack.append(item)

	while len(stack) != 0:
		outlst.append(stack.pop())

	return outlst


def evalExpression(expression: str) -> float:
	"""
	Evaluates a basic math expression and returns the result
	Eg:
	>>> evalExpression("1+2-(3*4)/6")
	1.0
	"""
	stack = []

	for item in infixToPostfix(expression):
		if type(item) == float:
			stack.append(item)
		else:
			num1 = stack.pop()
			num2 = stack.pop()

			if item == "+":
				stack.append(num2 + num1)

			elif item == "-":
				stack.append(num2 - num1)

			elif item == "*":
				stack.append(num2 * num1)

			elif item == "/":
				stack.append(num2 / num1)

	return stack.pop()


def solveExpression(filename: str) -> str:
	"""
	Reads an expression from an image, and attemps to evaluate the expression. 
	Returns a string of an equation, where the left side is the expression from
		the image, while the right side is the evaluated expression of the left
		side. 
	"""
	# Extracting the expression from the image:
	exprStr = pytesseract.image_to_string(filename)

	# Removing illegal characters: 
	for char in exprStr:
		if char not in VALIDCHARS:
			exprStr = exprStr.replace(char, "")

	try:
		output = f"{exprStr} = {str(evalExpression(exprStr))}"
		return output
	except:
		return f"Error: String read from file was: {exprStr}, but this expression could not be evaluated."


def solveExpressionImg(filename: str) -> np.ndarray:

	# Opening the original image:
	try:
		img1 = cv2.imread(filename, 1)
	except:
		print(f"Error file {filename} could not be found.")
		return

	# Creating a 2nd image to annotate with the answer:
	(height, width, channels) = img1.shape
	img2 = np.zeros((height, width, channels), np.uint8)

	# Annotating the second image with the solved expression
	cv2.putText(img2, solveExpression(filename), (5, 50), cv2.QT_FONT_NORMAL, 1, (255, 0, 0), 1)
	"""
	# Combining the original image with the annotated image with the solved expression
	img = np.concatenate((img1, img2), axis=0)
	return img"""
	cv2.imshow("Original Image", img1)
	cv2.imshow("Solved Expresion", img2)
	cv2.waitKey(0)
	return

if __name__ == "__main__":
	filename = "expression.png"
	solveExpressionImg(filename)