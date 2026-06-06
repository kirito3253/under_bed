import cv2
import numpy as np
from gpiozero import Robot
import time
import colorsys

#カメラの設定
width = 320
height = 240
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("Y", "U", "Y", "V"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, 30)

wait_secs = int(1000 / cap.get(cv2.CAP_PROP_FPS))

#モータの設定
robot=Robot(left=(17,18), right=(19,20))
robot.stop()

#背景差分の設定
model = cv2.bgsegm.createBackgroundSubtractorMOG()

#色抽出の設定
AREA_RATIO_THRESHOLD=0.005

#動体検知
def obj_detect(frame):
    mask = model.apply(frame)
    # 輪郭抽出する。
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # 小さい輪郭は除く
    contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))
    # 輪郭を囲む外接矩形を取得する。
    bboxes = list(map(lambda x: cv2.boundingRect(x), contours))
    # 矩形を描画する。
    for x, y, w, h in bboxes:
        return x,y

#任意の色の検知
def find_specific_color(frame, AREA_RATIO_THRESHOLD,LOW_COLOR,HIGH_COLOR):
    h,w,c=frame.shape
    #hsv色空間に変換
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #色を抽出
    ex_img=cv2.inRange(hsv,LOW_COLOR,HIGH_COLOR)
    #輪郭抽出
    contours, hierarchy=cv2.findContours(ex_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #面積計算
    areas=np.array(list(map(cv2.contourArea,contours)))
    
    if len(areas)==0 or np.max(areas)/(h*w) < AREA_RATIO_THRESHOLD:
        return None
    else:
        #最大面積の重心
        max_idx=np.argmax(areas)
        max_area=areas[max_idx]
        result=cv2.moments(contours[max_idx])
        x=int(result["m10"]/result["m00"])
        y=int(result["m01"]/result["m00"])
        return (x,y)

#モータ制御
def motor(x):
    sp=x/640+0.3 #スピードはxに依存(0.3~0.8)
    robot.forward(sp)
    time.sleep(0.1)
    robot.stop()

while True:
    while True:
        ret,frame = cap.read() #カメラ画像の取得
        if not ret:
            break
        cv2.imshow("camera",frame) #カメラ画像の表示
        
        tup = obj_detect(frame) #背景差分
        if tup is not None:
            x=tup[0]
            y=tup[1]
            
            #r,g,bを抽出
            color=frame[y,x]
            r=color[2]
            g=color[1]
            b=color[0]
            #hsvに変換
            hsv=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            h=int(hsv[0]*180)
            s=int(hsv[1]*255)
            v=int(hsv[2]*255)
            #色の誤差
            LOW_COLOR=np.array([h-10,75,75])
            HIGH_COLOR=np.array([h+10,255,255])
            #赤色は検知しない(例外)
            if((0<=h and h<=30) or (150<=h and h<=179)):
                continue
            else:
                break

        if cv2.waitKey(wait_secs) & 0xff == ord("q"):
            break #qキーが入力されたらwhileループを抜ける

    while True:
        ret,frame = cap.read() #カメラ画像の取得
        if not ret:
            break
        cv2.imshow("camera",frame) #カメラ画像の表示

        #背景差分後に取得した色を探す
        pos=find_specific_color(frame, AREA_RATIO_THRESHOLD, LOW_COLOR, HIGH_COLOR)
        if pos is not None:
            cv2.circle(frame,pos,10,(0,0,255),-1) #色を見つけた部分にマーク
            x=pos[0]
            y=pos[1]
        
            if(x>15): #x座標が15より大きかったらモータを動かす
                motor(x)
            else:
                break

        else:
            break
        
        cv2.imshow("camera",frame)

        if cv2.waitKey(wait_secs) & 0xff == ord("q"):
            break #qキーが入力されたらwhileループを抜ける
    
    if cv2.waitKey(wait_secs) & 0xff == ord("q"):
            break #qキーが入力されたらwhileループを抜ける

robot.stop()
cv2.destroyAllWindows()
cap.release()