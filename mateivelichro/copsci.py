import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from datetime import datetime, timedelta
import requests

class copsci:
    def __init__(self, name, uname, pw, new_yyyy_mm_dd, old_yyyy_mm_dd="2017-08-25", bbox = [1066100.29, 4987982.08, 1079625.59, 5005331.26], ignore_mask=[(0,90,200,150), (820,0,560,400), (520,0,300,400),(0,300,100,200)]):

        #API connection details and payload
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.img_url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        self.bbox = bbox
        self.ignore_mask=ignore_mask
        self.new_date_obj = datetime.strptime(new_yyyy_mm_dd, "%Y-%m-%d")
        self.old_date_obj = datetime.strptime(old_yyyy_mm_dd, "%Y-%m-%d")
        self.request_payload={
                                "input": {
                                    "bounds": {
                                        "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/32633"},
                                                    "bbox": self.bbox,
                                    },
                                    "data": [
                                        {
                                            "type": "sentinel-2-l2a",
                                            "dataFilter": {
                                                "timeRange": {
                                                    "from": self.new_date_obj.strftime("%Y-%m-%d") + "T00:00:00Z",
                                                    "to": (self.new_date_obj + timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00Z",
                                                },
                                                "maxCloudCoverage": 0
                                            },
                                        }
                                    ],
                                },
                                "output": {
                                    "resx": 10, #And this probably needs to be adjusted
                                    "resy": 10,
                                },
                                "evalscript": """
                                                //VERSION=3
                                                function setup() {
                                                return {
                                                    input: ["B02", "B03", "B04"],
                                                    output: { bands: 3 },
                                                }
                                                }

                                                function evaluatePixel(sample) {
                                                return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
                                                }
                                                """,
                            }
        self.request_payload_OLD={
                                "input": {
                                    "bounds": {
                                        "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/32633"},
                                                    "bbox": self.bbox,
                                    },
                                    "data": [
                                        {
                                            "type": "sentinel-2-l2a",
                                            "dataFilter": {
                                                "timeRange": {
                                                    "from": "2017-08-25T00:00:00Z",
                                                    "to":   "2017-08-26T00:00:00Z",
                                                    "from": self.old_date_obj.strftime("%Y-%m-%d") + "T00:00:00Z",
                                                    "to": (self.old_date_obj + timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00Z",
                                                },
                                                "maxCloudCoverage": 0
                                            },
                                        }
                                    ],
                                },
                                "output": {
                                    "resx": 10, #And this probably needs to be adjusted
                                    "resy": 10,
                                },
                                "evalscript": """
                                                //VERSION=3
                                                function setup() {
                                                return {
                                                    input: ["B02", "B03", "B04"],
                                                    output: { bands: 3 },
                                                }
                                                }

                                                function evaluatePixel(sample) {
                                                return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
                                                }
                                                """,
                            }
        self.username = uname
        self.token_payload = {
                            'client_id': 'cdse-public',
                            'username': self.username,
                            'password': pw,
                            'grant_type': 'password'
                        }
        self.access_token = self.__get_access_token()
        self.headers = {
                            "Authorization": f"Bearer {self.access_token}",
                            "Content-Type": "application/json"
                        }
        

        self.name = name
        self.old_image=self.__get_sat_img(self.request_payload_OLD, "output_image_old.png")
        self.new_image=self.__get_sat_img(self.request_payload, "output_image.png")
        self.diff_img=self.__compare_img(self.new_image,self.old_image,self.ignore_mask)


        

    def __get_access_token(self):
        
        response = requests.post(self.token_url, data=self.token_payload)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            print("Retrieved access token succesfully.")
        else:
            access_token=''
            print("Failed to retrieve token:", response.status_code, response.text)

        return access_token
    
    def __get_sat_img(self, jsn, out_nm):
        response = requests.post(self.img_url, json=jsn, headers=self.headers)

        # Save the image if successful
        if response.status_code == 200:
            with open(out_nm, "wb") as f:
                f.write(response.content)
            print("Image downloaded successfully.")
            return cv2.imread(out_nm)
            
        else:
            print("Error:", response.status_code, response.text)

            

    def __compare_img (self, img1, img2, ignore_rects):
        # Define ellipse parameters
        start_angle = 0                  # Starting angle of the arc
        end_angle = 360                  # Ending angle of the arc (360 for full ellipse)
        color = (255, 255, 255)              # Color in BGR (white)
        alt_color = (0, 0, 255)          # Color in BGR (red)

        #copying new image so that we edit a copy and not the original array
        img_output=img1.copy()
        #convert to grayscale
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        #substract one grayscale from another to get difference
        img_diff=cv2.subtract(img1_gray, img2_gray)

  
        (thresh,bandw) = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)

        # Build ignore mask, same size as bandw
        ignore_mask = np.zeros_like(bandw, dtype=np.uint8)  # 0 = keep, 255 = ignore
        for (x, y, w, h) in ignore_rects:
            x1, y1 = int(x), int(y)
            x2, y2 = int(x + w), int(y + h)
            cv2.rectangle(ignore_mask, (x1, y1), (x2, y2), color=255, thickness=-1)
        #substract ignore mask
        bandw = cv2.bitwise_and(bandw, cv2.bitwise_not(ignore_mask))

        #get white pixels
        white_pixels = np.argwhere(bandw == 255)

        #Removing first 20 lines of pixels since they contain dates
        white_pixels = np.array([item for item in white_pixels if item[0]>20])

        clustering = DBSCAN(eps=5, min_samples=5).fit(white_pixels)
        labels = clustering.labels_





        #a collection to save all the clustered white pixels
        clusters = []
    
        for label in set(labels):
            if label != -1:  # -1 is noise
                cluster = white_pixels[labels == label]
                clusters.append(cluster)
        #create an empty mask on which we will draw the elipses
        height, width = img1.shape[:2]
        mask = np.zeros((height, width,3), dtype=np.uint8)
        
    # --------------------------   drawing elipses ---------------------------------------------------------#
        #initiate a colleaction for centroids to draw elipses
        centroid=[]
        #for each cluster in collection
        for cluster in clusters:

            #principal component analysis to calcualte orientation angle
            pca = PCA(n_components=2)
            pca.fit(cluster)        
            pc1 = pca.components_[0]
            #Angle in radials
            angle_rad = np.arctan2(pc1[1], pc1[0])
            #Angle in degrees
            angle_deg = np.degrees(angle_rad)
            
            x_coords = [x for x, y in cluster]
            y_coords = [y for x, y in cluster]    

            #calcualte range of clustered pixels on x and Y axes    
            x_range = max(x_coords) - min(x_coords)
            y_range = max(y_coords) - min(y_coords)

            # center of cluster is the middle of the x ands y coordiantes
            centroid = [int(sum(x_coords) / len(cluster)), int(sum(y_coords) / len(cluster))]
            # draw elipse on mask
            cv2.ellipse(mask, centroid[::-1], (x_range,y_range), angle_deg, start_angle, end_angle, color)
        #Convert mask with elipses to grayscale
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        
        # Threshold to binary (black and white)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the merged contour on original imagge
        cv2.drawContours(img_output, contours, -1, alt_color, 1)

        

        return img_output

