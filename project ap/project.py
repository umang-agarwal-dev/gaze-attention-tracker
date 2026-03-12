import cv2 as cv
import mediapipe as mp
import numpy as np
import time

center_start_time=time.time()
lookaway_counter = 0
warning_active = False
prev_gaze="Center"
lookaway_start_time=time.time()
highest_center_time=0

cam=cv.VideoCapture(0)
face_mesh=mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
while True:
  ret, frame=cam.read()
  if not ret:
    print('Ignoring Camera Frame')
    break
  frame=cv.flip(frame,1)
  rgb_frame=cv.cvtColor(frame , cv.COLOR_BGR2RGB)
  output = face_mesh.process(rgb_frame)
  landmarks_points= output.multi_face_landmarks

  frame_h , frame_w, _ = frame.shape
  if landmarks_points:
    landmarks=landmarks_points[0].landmark

    #left iris
    iris_points_left=landmarks[468:473]
    for landmark in iris_points_left:
      x=int(landmark.x*frame_w)
      y=int(landmark.y*frame_h)
      cv.circle(frame,(x,y),3,(0,0,255),-1) 
    iris_center_left_x=int(sum([landmark.x for landmark in iris_points_left])/5*frame_w) 
    iris_center_left_y=int(sum([landmark.y for landmark in iris_points_left])/5*frame_h)
    cv.circle(frame,(iris_center_left_x,iris_center_left_y),5,(255,0,0),-1)

    #right iris
    iris_points_right=landmarks[473:478]
    for landmark in iris_points_right:
      x=int(landmark.x*frame_w)
      y=int(landmark.y*frame_h)
      cv.circle(frame,(x,y),3,(0,0,255),-1)
    iris_center_right_x=int(sum([landmark.x for landmark in iris_points_right])/5*frame_w)
    iris_center_right_y=int(sum([landmark.y for landmark in iris_points_right])/5*frame_h)
  
  
    #left eye corner coord
    left_eye_left_corner_x=int(landmarks[33].x*frame_w)
    left_eye_left_corner_y=int(landmarks[33].y*frame_h)

    left_eye_right_corner_x=int(landmarks[133].x*frame_w)
    left_eye_right_corner_y=int(landmarks[133].y*frame_h)

    #top and down
    #left eye upper and lower
    left_eye_top=landmarks[159]
    left_eye_bottom=landmarks[145]

    #left eye top bottom coord
    left_eye_top_y=int(left_eye_top.y*frame_h)
    left_eye_bottom_y=int(left_eye_bottom.y*frame_h)

    #gaze ratio for left right
    left_ratio = (left_eye_left_corner_x - iris_center_left_x)/(left_eye_left_corner_x-left_eye_right_corner_x)

    #gaze ratio for top bottom
    eye_corner_y = (left_eye_left_corner_y + left_eye_right_corner_y) / 2
    eye_width = abs(left_eye_right_corner_x - left_eye_left_corner_x)
    vertical_ratio = (iris_center_left_y - eye_corner_y) / eye_width

    #result
    if vertical_ratio<-0.1:
     gaze="Looking Top"
    elif vertical_ratio>0.023:
      gaze="Looking Down"
    elif left_ratio<0.38:
      gaze="Looking Left"
    elif left_ratio>0.55 :
      gaze="Looking Right"
    else :
      gaze="Center"

    # detect gaze change
    if gaze == "Center":
        if prev_gaze != "Center":
            center_start_time = time.time()
        center_time = time.time() - center_start_time
        if center_time > highest_center_time:
          highest_center_time = center_time
    else:
        center_time = 0


    # show center timer
    cv.putText(frame, f"Center Time:{center_time:.2f}s", (frame_w-250, frame_h-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv.putText(frame, f"Max Focus:{highest_center_time:.2f}s", (frame_w-250, frame_h-50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)

    # warning logic
    if gaze != "Center":
        if prev_gaze == "Center":
            lookaway_start_time = time.time()
            warning_active = False

        if time.time() - lookaway_start_time > 0.3:
            cv.putText(frame, "Look At The Screen!", (100,100), cv.FONT_HERSHEY_COMPLEX, 1.2, (0,0,255), 3)

            if not warning_active:
                lookaway_counter += 1
                warning_active = True


    # update previous gaze
    prev_gaze = gaze

    #show gaze
    cv.putText(frame,gaze,(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    #show iris center
    cv.circle(frame,(iris_center_right_x,iris_center_right_y),5,(255,0,0),-1)

    #show look away count
    cv.putText(frame,f"Look Away Count: {lookaway_counter}",(20,frame_h-20),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
    
  cv.imshow('webcam' , frame)
  if cv.waitKey(1) & 0xff==ord('q'):
   break

cv.destroyAllWindows()
