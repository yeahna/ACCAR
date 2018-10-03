import cv2  
import numpy as np 

def grayscale(img): 
	return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
					
def canny(img, low_threshold, high_threshold):
	return cv2.Canny(img, low_threshold, high_threshold) 
				
def gaussian_blur(img, kernel_size): 
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): 

	mask = np.zeros_like(img) 
	
	if len(img.shape) > 2:  
		color = color3 
	else:  
		color = color1 

	cv2.fillPoly(mask, vertices, color) 

	ROI_image = cv2.bitwise_and(img, mask) 
	
	return ROI_image 
	
def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
	for line in lines: 
		for x1,y1,x2,y2 in line: 
			cv2.line(img, (x1, y1), (x2, y2), color, thickness) 

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10): 
	cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness) 

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): 
	''' 'img' should be the output of Canny transform.
		 Returns an image with hough lines drawn'''
	lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap) 

	#line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8) 

	#draw_lines(line_img, lines) 
	
	return lines 

def weighted_img(img, initial_img): 
	return cv2.addWeighted(initial_img, 1, img, 1, 0) 

def get_fitline(img, f_lines):
	lines = np.squeeze(f_lines) 
	lines = lines.reshape(lines.shape[0]*2,2) 
	rows,cols = img.shape[:2] 
	output = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01) 
	vx, vy, x, y = output[0], output[1], output[2], output[3] 

	x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1 
	x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100) 
	result = [x1, y1, x2, y2, (x1 + x2) / 2, (y1 + y2) / 2] 
	
	return result 

def get_lane(image):

	height, width = image.shape[:2] 
	
	gray_img = grayscale(image) 
	blur_img = gaussian_blur(gray_img, 3) 
	canny_img = canny(blur_img, 70, 210) 
	
#vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32) 
	vertices = np.array([[(0,500),(0, 200), (width, 200), (width,500)]], dtype=np.int32) 
#vertices = np.array([[(500,height),(500, height/2), (width, height/2), (width,height)]], dtype=np.int32) 
	
	ROI_img = region_of_interest(canny_img, vertices) 
	ROI_img2 = region_of_interest(image, vertices)
	cv2.imshow('ROI_img2', ROI_img2)

	# for DEBUG
	cv2.polylines(image,vertices,True,(255,0,0),5)
	
	# 허프 변환
	line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) 
	line_arr = np.squeeze(line_arr) 

	if line_arr is None:
		return image

	slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi 

	#ignore horizontal slope lines
	line_arr = line_arr[np.abs(slope_degree)<160] 
	slope_degree = slope_degree[np.abs(slope_degree)<160] 

	#ignore vertical slope lines
	line_arr = line_arr[np.abs(slope_degree)>95] 
	slope_degree = slope_degree[np.abs(slope_degree)>95] 


	# 필터링된 직선 버리기
	L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:] 
	temp = np.zeros((ROI_img2.shape[0], ROI_img2.shape[1], 3), dtype=np.uint8) 
	L_lines, R_lines = L_lines[:,None], R_lines[:,None] 

	# if cant find any lines
	'''if L_lines is None and R_lines is None:
		return image'''
	'''	print("here1")
		return image, int(-1)
	elif L_lines is None and R_lines is not None:
		print("here2")
		return image, int(-2)
	elif L_lines is not None and R_lines is None:
		print("here3")
		return image, int(-3)
	'''
	#print(L_lines, "...", R_lines)

	if len(L_lines) == 0 and len(R_lines) == 0:
		return image, -1
	elif len(L_lines) == 0 and len(R_lines) != 0:
		return image, -2
	elif len(L_lines) != 0 and len(R_lines) == 0:
		return image, -3


	left_fit_line = get_fitline(ROI_img2,L_lines) 
	right_fit_line = get_fitline(ROI_img2,R_lines) 

	draw_fit_line(temp, left_fit_line) 
	draw_fit_line(temp, right_fit_line) 
	
	result = weighted_img(temp, image) 
#cv2.imshow('result',result) 

	center_x_point = int((left_fit_line[4] + right_fit_line[4]) / 2)
	center_y_point = int((left_fit_line[5] + right_fit_line[5]) / 2)

	result = cv2.circle(result, (center_x_point, center_y_point), 5, (0, 0, 255), -1)

	return result, center_x_point
