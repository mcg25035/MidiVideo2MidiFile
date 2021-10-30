import cv2

def get_images_from_video(video_name, time_F):
    video_images = []
    vc = cv2.VideoCapture(video_name)
    c = 1
    
    if vc.isOpened(): #判斷是否開啟影片
        rval, video_frame = vc.read()
    else:
        rval = False

    while rval:   #擷取視頻至結束
        rval, video_frame = vc.read()
        
        if(c % time_F == 0): #每隔幾幀進行擷取
            video_images.append(video_frame)     
        c = c + 1
    vc.release()
    
    return video_images


time_F = 1#time_F越小，取樣張數越多
video_name = 'a.mp4' #影片名稱
print("loading movie.......")
video_images = get_images_from_video(video_name, time_F) #讀取影片並轉成圖片
print("loaded complete!")

#for i in range(0, len(video_images)): #顯示出所有擷取之圖片
#cv2.imshow('windows', video_images[10])
#    cv2.waitKey(1000)
#cv2.imwrite("save.png",video_images[60])
#print(video_images[60].shape[0])

average = 0
for i in range(0,video_images[60].shape[1]):
    average += (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3
average = average / video_images[60].shape[1]-1
print(average)

for i in range(0,video_images[60].shape[1]):
    if average > (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        print("gap")
    elif average < (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        print("key_pixel")
    else:
        print("null")
        
#cv2.destroyAllWindows

#y = 345
