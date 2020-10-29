# USAGE
# python solve_sudoku_puzzle.py --model output/digit_classifier.h5 --image sudoku_puzzle.jpg

# import the necessary packages
from pyimagesearch.sudoku import extract_digit
from pyimagesearch.sudoku import find_puzzle
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from compute_algorthim import Sudoku
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model",help="path to trained digit classifier",default='C:\\Users\\nguyenbavu\\Desktop\\opencv-sudoku-solver\\output\\digit_classifier.h5')
ap.add_argument("-i", "--image", help="path to input sudoku puzzle image",default='C:\\Users\\nguyenbavu\\Desktop\\opencv-sudoku-solver\\sudoku_puzzle.jpg')
ap.add_argument("-d", "--debug", type=int, default=-1,help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())

# load the digit classifier from disk
print("[INFO] loading digit classifier...")
model = load_model(args["model"])

# load the input image from disk and resize it
print("[INFO] processing image...")
image = cv2.imread(args["image"])
cv2.imshow('sudoku',image)


image = imutils.resize(image, width=600)

# find the puzzle in the image and then 
# puzzleImage là ảnh thường , warped là ảnh xám
(puzzleImage, warped) = find_puzzle(image, debug=args["debug"] > 0) #debug default hiện đang là -1 < 0 nên là false

# initialize our 9x9 sudoku board
board = np.zeros((9, 9), dtype="int")

# a sudoku puzzle is a 9x9 grid (81 individual cells), so we can
# infer the location of each cell by dividing the warped image
# into a 9x9 grid

# ảnh xám có tọa độ y , x
stepX = warped.shape[1] // 9
stepY = warped.shape[0] // 9

arr = np.zeros((9,9))
for y in range(9):
	for x in range(9):
		startX = x * stepX
		startY = y * stepY
		endX = (x + 1) * stepX
		endY = (y + 1) * stepY
		# extract the digit from the cell
		cell = warped[startY:endY, startX:endX]
		digit = extract_digit(cell, debug=args["debug"] > 0)
		if digit is None : 
			continue
		else : 
			roi = cv2.resize(digit, (28, 28))
			roi = roi.astype("float") / 255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi, axis=0)

			# classify the digit and update the sudoku board with the
			# prediction
			pred = model.predict(roi).argmax(axis=1)[0]
			arr[y,x] = pred

arr = arr.astype(int)

my_soduku = Sudoku(arr)
my_soduku.print_board()
cv2.waitKey(0)
cv2.destroyAllWindows()



