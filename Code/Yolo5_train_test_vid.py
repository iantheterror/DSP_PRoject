
import torch
import cv2
from playsound import playsound
batch = "exp7"
# exp4 is 10 epoch, exp5 is 50 epoch,  exp6 is the special dataset
# path = path = 'F:\\Git\\DSP\\DSP_PRoject\\Code\\yolov5-master\\'  #Your File PAth HEre
path = 'F:\\Git\\DSP\\DSP_PRoject\\Code\\yolov5-master\\'
pathapp = path + f'\\runs\\train\\{batch}\\weights\\last.pt'
trig_class = 2 # 0: Ian 1: Tara 2: Ruby 3: Stop
trig_thresh = 80
run1 = False
activate = False
class_ = 5
trig_Count = 0
#model = torch.hub.load('C:\\Users\\luisa\\Dropbox\\UVMstuff\\AIR lab\\Yolo8_Training\\yolov5', 'last', source = 'local')
model = torch.hub.load(path, 'custom', path=pathapp, force_reload=True,source='local') 

cap = cv2.VideoCapture(0) 
img2 = cv2.imread('RR.jpg')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    img = frame
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    result = model(img)
   # print(result)  

    df = result.pandas().xyxy[0]
    print(df)  
    for ind in df.index:
        x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
        x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
        label = df['name'][ind]
        class_ = df['class'][ind]
        confidence = int(df['confidence'][ind]*100)
        conf = f'Confidence: {confidence}%'
        if confidence < 50 :
            
            cv2.rectangle(img, (x1, y1), (x2,y2), (255, 0, 0), 2)
            cv2.putText(img, "Low Confidence", (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (0,0 , 255), 2)
            cv2.putText(img, conf, (x2, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        elif confidence >= 50 :
            if confidence >= 70:
                cv2.rectangle(img, (x1, y1), (x2,y2), (255, 255, 0), 2)
                cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(img, conf, (x1+100, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x1, y1), (x2,y2), (255, 255, 0), 2)
                cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                cv2.putText(img, conf, (x1+100, y1-5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
    
    

    
    if class_ == trig_class:
        if run1 == False:
            if confidence >= trig_thresh:
                trig_Count +=1
                if trig_Count >= 10:
                    activate = True 
                    run1 = True
                    img = img2
        
    cv2.imshow('IMAGE', img)
    cv2.waitKey(10)
    if activate == True:
        playsound('RR.mp3')
        activate = False


          
    
'''

python train.py --img 416 --batch 16 --epochs 100 --data custom_data.yaml --weights yolov5s.pt --nosave --cache

python detect.py --weights runs/train/exp6/weights/best.pt --img 416 --conf 0.4 --source 'C:\\Users\\luisa\\Dropbox\\UVMstuff\\AIR lab\\Yolo8_Training\\test_BCCD.jpg'


cap = cv2.VideoCapture('video.mp4')

while True:
    img = cap.read()[1]
    if img is None:
        break
    result = model(img)
    df = result.pandas().xyxy[0]

    for ind in df.index:
        x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
        x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
        label = df['name'][ind]
        conf = df['confidence'][ind]
        text = label + ' ' + str(conf.round(decimals= 2))
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

    cv2.imshow('Video',img)
    cv2.waitKey(10)
 '''   