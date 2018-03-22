
from PIL import Image, ImageStat
import numpy, sys 
import greener, grey, blues

# =========
# converged
# =========
#
# Will determine if the centroids have converged or not.
# Essentially, if the current centroids and the old centroids
# are virtually the same, then there is convergence.
#
# Absolute convergence may not be reached, due to oscillating
# centroids. So a given range has been implemented to observe
# if the comparisons are within a certain ballpark
#
def converged(centroids, old_centroids):
	if len(old_centroids) == 0:
		return False


	if len(centroids) <= 5:
		a = 1
	elif len(centroids) <= 10:
		a = 2
	else:
		a = 4

	for i in range(0, len(centroids)):
		cent = centroids[i]
		old_cent = old_centroids[i]

		if ((int(old_cent[0]) - a) <= cent[0] <= (int(old_cent[0]) + a)) and ((int(old_cent[1]) - a) <= cent[1] <= (int(old_cent[1]) + a)) and ((int(old_cent[2]) - a) <= cent[2] <= (int(old_cent[2]) + a)):
			continue
		else:
			return False

	return True

#end converged


# ======
# getMin
# ======
#
# Method used to find the closest centroid to the given pixel.
#
def getMin(pixel, centroids):
	minDist = 9999
	minIndex = 0

	for i in range(0, len(centroids)):
		d = numpy.sqrt(int((centroids[i][0] - pixel[0]))**2 + int((centroids[i][1] - pixel[1]))**2 + int((centroids[i][2] - pixel[2]))**2)
		if d < minDist:
			minDist = d
			minIndex = i

	return minIndex

#end getMin

##-----------
##getDist
##-----------
##This function gives the euclidean distance between two pixels

def getDist(pixel1, pixel2):
    minDist = 9999
    d = numpy.sqrt(int((pixel1[0] - pixel2[0]))**2 + int((pixel1[1] - pixel2[1]))**2 + int((pixel1[2] - pixel2[2]))**2)
    if d < minDist:
        minDist = d

    return minDist

# ============
# assignPixels
# ============
#
# Assigns each pixel to the given centroids for the algorithm.
# Method finds the closest centroid to the given pixel, then
# assigns that centroids to the pixel.
#
def assignPixels(centroids):
	clusters = {}

	for x in range(0, img_width):
		for y in range(0, img_height):
			p = px[x, y]
			minIndex = getMin(px[x, y], centroids)

			try:
				clusters[minIndex].append(p)
			except KeyError:
				clusters[minIndex] = [p]

	return clusters

#end assignPixels


# ===============
# adjustCentroids
# ===============
#
# Method is used to  re-center the centroids according
# to the pixels assigned to each. A mean average is 
# applied to each cluster's RGB values, which is then
# set as the new centroids.
#
def adjustCentroids(centroids, clusters):
	new_centroids = []
	keys = sorted(clusters.keys())
	#print(keys)

	for k in keys:
		n = numpy.mean(clusters[k], axis=0)
		new = (int(n[0]), int(n[1]), int(n[2]))
		print(str(k) + ": " + str(new))
		new_centroids.append(new)

	return new_centroids

#end adjustCentroids


# ===========
# startKmeans
# ===========
#
# Used to initialize the k-means clustering
#
def startKmeans(someK):
	centroids = []
	old_centroids = []
	rgb_range = ImageStat.Stat(im).extrema
	i = 1

	#Initializes someK number of centroids for the clustering
	for k in range(0, someK):

		cent = px[numpy.random.randint(0, img_width), numpy.random.randint(0, img_height)]
		centroids.append(cent)

##	centroids.append((9, 232, 64))
##	centroids.append((200, 200, 195))


	print("Centroids Initialized. Starting Assignments")
	print("===========================================")

	while not converged(centroids, old_centroids) and i <= 20:
		print("Iteration #" + str(i))
		i += 1

		old_centroids = centroids 								#Make the current centroids into the old centroids
		clusters = assignPixels(centroids) 						#Assign each pixel in the image to their respective centroids
		centroids = adjustCentroids(old_centroids, clusters) 	#Adjust the centroids to the center of their assigned pixels


	print("===========================================")
	print("Convergence Reached!")
	print(centroids)
	return centroids

#end startKmeans

def rakhdo(x,y):
        meanR=0
        meanG=0
        meanB=0
        print("old:",px[x,y])
        for i in range(x-250,x+250):
                for j in range(y-250,y+250):
                        r,b,g = px[i,j]
                        meanR += r
                        meanG += g
                        meanB += b
        meanR=(int)(meanR/250000)
        meanG=(int)(meanG/250000)
        meanB=(int)(meanB/250000)
        print(meanR, "  ",meanB, "  ", meanG, "HeHe")
        return (meanR, meanB, meanG)
# ==========
# drawWindow
# ==========
#
# Once the k-means clustering is finished, this method
# generates the segmented image and opens it.
#
def drawWindow(result):
    img = Image.new('RGB', (img_width, img_height), "white")
    p = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            RGB_value = result[getMin(px[x, y], result)]
            p[x, y] = RGB_value
    img.show()
    print(greener.list)
    for i in range(0, 3):
        print(i)
        for x in range(250, img_width-250):
                for y in range(250, img_height-250):
                        if result[i]==p[x,y]:
                                #pix2 = rakhdo(x,y)
                                pix = rakhdo(x,y)
                                min_green = 9999
                                min_grey = 9999
                                min_blue = 9999
                                for j in range(len(greener.list)):
                                        d = getDist(pix,greener.list[j])
                                        if d<min_green:
                                                min_green = d;
                                for j in range(len(grey.list)):
                                        d = getDist(pix,grey.list[j])
                                        if d<min_grey:
                                                min_grey = d;
                                for j in range(len(blues.list)):
                                        d = getDist(pix,blues.list[j])
                                        if d<min_blue:
                                                min_blue = d;
                                print(min_green," ",min_grey," ",min_blue)
                                if min_green < min_grey:
                                        if min_green < min_blue:
                                                result[i]=result[i]+("green",)
                                        else:
                                                result[i]=result[i]+("blue",)
                                else:
                                        if min_grey < min_blue:
                                                result[i]=result[i]+("grey",)
                                        else:
                                                result[i]=result[i]+("blue",)

    print(result)
        

#end drawWindow

##------------
##classify
##------------
##
##
##Once the final centroids are obtained, they require to be classified into either green, cement or water cover.
##This is done by classify.

def classify(result):
    print (result)

##    for i in range(0, k):
##        for x in range(0, img_width):
##            for y in range(0, img_height):
##                if(result[i] == 
            
                    



num_input = (str)(input("Enter image number: "))
k_input = int(input("Enter K value: "))

img = "img/test" + num_input.zfill(2) + ".jpg"
im = Image.open(img)
img_width, img_height = im.size
px = im.load()

result = startKmeans(k_input)
classify(result)

##
##TP = img_width * img_height
##white = TP - numpy.sum(img[1] == 255)
##print ("Total pixels: ", TP, "White", white)
##
drawWindow(result)
