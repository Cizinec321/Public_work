import requests
import copsci 

# Add a connection.txt file with your conenction details so:
# username=username@mail.com
# password=apipswd
connect = {}

with open("connection.txt", "r") as f:
    for line in f:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            connect[key] = value


#This class:
# 1) dowloads 2 images at different dates
# 2) converts them to black and white
# 3) substract one imagge from another generating a grayscale difference
# 4) Above a certain treshold of a pixel value (20), all pixels are set to 255 and all below or equal are set to 0 (black)
# 5) Generates a mask out of the graysclae difference forced to black& white
# 6) Draws elipses and using a DBSCAN algorithm, groups elipses that overlap on the more recent image
# 7) Saves new image with grouped elipses drawn over it



#How to use:
#image_comparison_test=copsci.copsci(
#  name, --mandatory name of instance
#  uname, --mandatory copernicus api username
#  pw, --mandatory copernicus api password
#  new_yyyy_mm_dd, --mandatory new date for recent image
#  old_yyyy_mm_dd="2017-08-25", --optional date for old image vs which the recent one will be compared, defaulted to 2017-08-25
#  bbox = [1066100.29, 4987982.08, 1079625.59, 5005331.26], --optional defaulted to these values which are of interest to me, pass any bbox of interest: http://bboxfinder.com/
#  ignore_mask=[(0,90,200,150), (820,0,560,400), (520,0,300,400),(0,300,100,200)] --optional list of X,Y,W,H coordinates, defaulted to these values which cover vilalges where annual changes are common so I don't want to analyse them
# ) 


image_comparison_test=copsci.copsci('test name', connect["username"],connect["password"],"2025-06-29")

copsci.cv2.imshow('comparison',image_comparison_test.diff_img)
copsci.cv2.imshow('new immage',image_comparison_test.new_image)
copsci.cv2.imshow('old immage',image_comparison_test.old_image)
copsci.cv2.waitKey(0)
copsci.cv2.destroyAllWindows()