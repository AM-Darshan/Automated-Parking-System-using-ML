def imageDetection(img_path):
    from easyocr import Reader
    import cv2
    import imutils
    import time
    import pandas as pd
   
    image = cv2.imread(img_path) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (5,5), 0) 
    edged = cv2.Canny(blur, 10, 200) 


    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    
    n_plate_cnt = None
    
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            n_plate_cnt = approx
            break        
    
    
    if  n_plate_cnt is None:
        detected = 0
        print ("No contour detected", img_path)
        text = "Unable to detect"
        cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        image = cv2.resize(image, (500, 350))
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return
    
    (x, y, w, h) = cv2.boundingRect(n_plate_cnt)
    license_plate = gray[y:y + h, x:x + w]

    
    reader = Reader(['en'])
    detection = reader.readtext(license_plate)


    if len(detection) == 0:
        text = "Unable to detect"
        cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        image = cv2.resize(image, (500, 350))
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    else:
        cv2.drawContours(image, [n_plate_cnt], -1, (0, 255, 0), 3)
        text = detection[0][1]
        accu = f"{detection[0][2] * 100:.2f}%"
        final_text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"

        cv2.putText(image,final_text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 3)
        image = cv2.resize(image, (500,350))
        cv2.imshow('license plate', license_plate)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
            'v_number': [text]}

        df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
        df.to_csv('data.csv',mode='a',index=False, header=False)

        print(img_path,final_text)
    
for i in range(1,16):
    imageDetection('images/'+str(i)+'.jpg')
