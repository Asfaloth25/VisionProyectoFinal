import cv2
import numpy as np

# get the harris corner detector from lab 3 part A
def harris_corner_detector(image: np.array, blockSize: int, ksize: int, k: float):
    """
    function to get Corners of an image via harris
    input:
        image - Input image 
        blockSize - Size of neighborhood considered for corner detection
        ksize - Aperture parameter of the Sobel derivative used
        k - Harris detector free parameter in the equation.
    output:
        corners of harris algorithm
    """

    # Input image to Harris corner detector should be grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Input image to Harris corner detector should be float32 type
    gray = np.float32(gray)
    gray = cv2.GaussianBlur(gray, (9,9), 0)
    
    # Apply Harris corner detection
    harris = cv2.cornerHarris(gray, blockSize, ksize,k)
    
    harris = cv2.dilate(harris, None)
    
    # Apply filter
    # Threshold for an optimal value of 1% of maximal R value
    threshold = 0.01*harris.max()

    return harris>threshold


# get shi tomasi corner detector from lab 3 part A
def shi_tomasi_corner_detection(image: np.array, maxCorners: int, qualityLevel:float, minDistance: int):
    """
    function to get corners of an image via shi tomasi
    imput:
        image - Input image
        maxCorners - Maximum number of corners to return. 
                    If there are more corners than are found, the strongest of them is returned. 
                    maxCorners <= 0 implies that no limit on the maximum is set and all detected corners are returned
        qualityLevel - Parameter characterizing the minimal accepted quality of image corners. 
                    The parameter value is multiplied by the best corner quality measure, which is the minimal eigenvalue or the Harris function response. 
                    The corners with the quality measure less than the product are rejected. 
                    For example, if the best corner has the quality measure = 1500, and the qualityLevel=0.01 , then all the corners with the quality measure less than 15 are rejected
        minDistance - Minimum possible Euclidean distance between the returned corners
        corner_color - Desired color to highlight corners in the original image
        radius - Desired radius (pixels) of the circle
    output:
        corners of shitomasi algorithm
    """

    # Input image to Tomasi corner detector should be grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply cv2.goodFeaturesToTrack function (shi tomasi)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance)

    # Corner coordinates conversion to integers
    return corners
    
def paint_shi_tomasi(corners:list ,image: np.array, corner_color: tuple, radius: int):
    corners = np.intp(corners)
    for corner in corners:
        # Multidimensional array into flattened array, if necessary
        x, y = corner.ravel()
        # Circle corners
        cv2.circle(image, (x,y), radius, corner_color)
    return image

def paint_harris(image, harris):
    image[harris] = [0,0,255]
    return image


def main(image: np.array, harris: bool):
    if harris:
        corners = harris_corner_detector(image, blockSize = 2, ksize = 9, k = 0.1)
        painted_image = paint_harris(image,corners)
        return painted_image, len(corners)
    else:
        corners = shi_tomasi_corner_detection(image, maxCorners = 100, qualityLevel = 0.1, minDistance = 4)
        painted_image = paint_shi_tomasi(corners, image, corner_color = (255, 0, 255), radius = 4)
        return painted_image, len(corners)

