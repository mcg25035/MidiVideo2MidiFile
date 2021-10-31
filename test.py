import cv2
import time
import math
from midiutil.MidiFile import MIDIFile

mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 1240)

channel = 0
volume = 100

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

def  note_name_convert(key_num):
        key_num=key_num-2
        z = key_num%7
        return [0,2,4,5,7,9,11][z-1]+(math.floor((key_num-1)/7)+2)*12

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

key_x_s = []
key_x_s_color = []
current_status = ""

for i in range(0,video_images[60].shape[1]):
    if average >= (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        current_status = "gap"
    elif average < (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        if current_status != "key":
            key_x_s.append(i)
            key_x_s_color.append((int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3)
        current_status = "key"
midi = {}
print("playing")
last_note = [False]*52
for i in range(0,len(video_images)-1):
    time = i
    event = []
    key_num = 1
    current_note = []
    current_note_2 = []
    for ii in key_x_s:
        if ((int(video_images[i][345,ii][0])+int(video_images[i][345,ii][1])+int(video_images[i][345,ii][2]))/3) - key_x_s_color[key_num-1] >= 5 :
            current_note.append(True)
            if last_note[key_num-1] == False:
                midi[key_num-1] = {"time" : time , "note" : note_name_convert(key_num)}
                #event.append(str(note_name_convert(key_num))+" Pressed")
        else:
            current_note.append(False)
            if (last_note[key_num-1]):
                midi[key_num-1]["duration"] = time-midi[key_num-1]["time"]
                mf.addNote(track, channel, midi[key_num-1]["note"] , midi[key_num-1]["time"]*0.14, midi[key_num-1]["duration"]*0.14, volume)
                #event.append(str(note_name_convert(key_num))+" Released")
        current_note_2.append((int(video_images[i][345,ii][0])+int(video_images[i][345,ii][1])+int(video_images[i][345,ii][2]))/3)
        key_num+=1
    #print(event)
    last_note = current_note
    #print("--")
    #print(key_x_s_color)
    #print(current_note_2)
    #print("--")

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

        
#cv2.destroyAllWindows

#y = 345
