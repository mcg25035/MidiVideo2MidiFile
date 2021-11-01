import cv2
import time as t
import math
from midiutil.MidiFile import MIDIFile

mf = MIDIFile(1)
mf.addTrackName(0,0, "midi")
mf.addTempo(0,0,320)

def get_images_from_video(video_name, time_F):
    video_images = []
    vc = cv2.VideoCapture(video_name)
    c = 1
    if vc.isOpened():
        rval, video_frame = vc.read()
    else:
        rval = False
    while rval:
        rval, video_frame = vc.read()
        if(c % time_F == 0): 
            video_images.append(video_frame)     
        c = c + 1
    vc.release()
    return video_images

def note_name_convert(key_num):
        key_num=key_num-2
        z = key_num%7
        return [0,2,4,5,7,9,11][z-1]+(math.floor((key_num-1)/7)+2)*12

def black_note_name_convert(key_num):
	    key_num = key_num-1
	    z = key_num%5
	    return [1,3,6,8,10][z-1]+(math.floor((key_num-1)/7)+2)*12

time_F = 1
video_name = 'a.mp4'
print("loading piano roll video")
video_images = get_images_from_video(video_name, time_F)
print("video load complete!")

white_average = 0
for i in range(0,video_images[60].shape[1]):
    white_average += (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3
white_average = white_average / video_images[60].shape[1]-1
white_key_x_s = []
white_key_x_s_color = []
current_status = False
for i in range(0,video_images[60].shape[1]):
    if white_average >= (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        current_status = False
    elif white_average < (int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3:
        if current_status != True:
            white_key_x_s.append(i)
            white_key_x_s_color.append((int(video_images[60][345,i][0])+int(video_images[60][345,i][1])+int(video_images[60][345,i][2]))/3)
        current_status = True


#這ㄍ是求(ㄟ ㄈㄜ 蕊 舉)的
black_average = 0
for i in range(0,video_images[60].shape[1]):
    black_average += ((int(video_images[60][316,i][0])+int(video_images[60][316,i][1])+int(video_images[60][316,i][2]))/3)*0.33
black_average = black_average / video_images[60].shape[1]-1
print(black_average)
black_key_x_s = []
black_key_x_s_color = []
black_readed = False
black_pixel_continous_times = 0
for i in range(0,video_images[60].shape[1]):
    if black_average >= ((int(video_images[60][316,i][0])+int(video_images[60][316,i][1])+int(video_images[60][316,i][2]))/3):
        if black_pixel_continous_times < 3:
            black_pixel_continous_times += 1
            continue
        elif black_readed == False:
            black_pixel_continous_times = 0
            video_images[60][316,i] = [100,100,100]
            black_key_x_s.append(i)
            black_key_x_s_color.append((int(video_images[60][316,i][0])+int(video_images[60][316,i][1])+int(video_images[60][316,i][2]))/3)
            black_readed = True
    elif black_average < ((int(video_images[60][316,i][0])+int(video_images[60][316,i][1])+int(video_images[60][316,i][2]))/3):
        black_readed = False

print("Debug Message : ")
print(black_key_x_s)
cv2.imshow("window",video_images[60])
cv2.waitKey(0)
midi_write = []
midi = {}

print("loading note frame by frame...")
last_note = [False]*52

for i in range(0,len(video_images)-1):
    time = i
    event = []
    key_num = 1
    current_note = []
    current_note_2 = []
    for ii in white_key_x_s:
        if ((int(video_images[i][345,ii][0])+int(video_images[i][345,ii][1])+int(video_images[i][345,ii][2]))/3 -  white_key_x_s_color[key_num-1]) >= 11 :
            current_note.append(True)
            if last_note[key_num-1] == False:
                midi[key_num-1] = {"time" : time , "note" : note_name_convert(key_num)}
        else:
            current_note.append(False)
            if (last_note[key_num-1]):
                midi[key_num-1]["duration"] = time-midi[key_num-1]["time"]
                midi_write.append([midi[key_num-1]["note"] , midi[key_num-1]["time"]*0.14, midi[key_num-1]["duration"]*0.14, 100])
        current_note_2.append((int(video_images[i][345,ii][0])+int(video_images[i][345,ii][1])+int(video_images[i] [345,ii][2]))/3)
        key_num+=1
    last_note = current_note

midi = {}
last_note = [False]*36

for i in range(0,len(video_images)-1):
    time = i
    event = []
    key_num = 1
    current_note = []
    current_note_2 = []
    for ii in black_key_x_s:
        if ((int(video_images[i][316,ii][0])+int(video_images[i][316,ii][1])+int(video_images[i][316,ii][2]))/3)-black_key_x_s_color[key_num-1] >= 11 :
            current_note.append(True)
            event.append("◆")
            if last_note[key_num-1] == False:
                midi[key_num-1] = {"time" : time , "note" : black_note_name_convert(key_num)}
                print(key_num)
                print(black_note_name_convert(key_num))
        else:
            current_note.append(False)
            event.append("◇")
            if (last_note[key_num-1]):
                midi[key_num-1]["duration"] = time-midi[key_num-1]["time"]
                midi_write.append([midi[key_num-1]["note"] , midi[key_num-1]["time"]*0.14, midi[key_num-1]["duration"]*0.14, 100])
        current_note_2.append((int(video_images[i][316,ii][0])+int(video_images[i][316,ii][1])+int(video_images[i][316,ii][2]))/3)
        key_num+=1
    last_note = current_note
    #print(event)
midi_write.sort(key = lambda z: z[1])
for i in midi_write:
    mf.addNote(0,0,i[0],i[1],i[2],100)
    print(i[1])

with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

print("midi file generated!")