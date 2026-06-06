import cv2

cap = cv2.VideoCapture("vtest.avi")
wait_secs = int(1000 / cap.get(cv2.CAP_PROP_FPS))

model = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask = model.apply(frame)

    # 輪郭抽出する。
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # 小さい輪郭は除く
    contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))

    # 輪郭を囲む外接矩形を取得する。
    bboxes = list(map(lambda x: cv2.boundingRect(x), contours))

    # 矩形を描画する。
    for x, y, w, h in bboxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.waitKey(wait_secs)

cap.release()
cv2.destroyAllWindows()