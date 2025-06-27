# Author: GouHaoliang
# Date: 2025/6/26
# Time: 14:00

import cv2

# 初始化外接摄像头（通常外接摄像头的索引是1）
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开外接摄像头")
    exit()

# 设置摄像头参数（可选）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 捕获视频流
while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        print("无法接收视频帧")
        break

    # 显示视频帧
    cv2.imshow('External Camera Feed', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()