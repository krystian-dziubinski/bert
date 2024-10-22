import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

num = 0

while cap.isOpened():


    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    img2 = cv2.flip(img2, -1)

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('images/stereoLeft/img' + str(num) + '.png', img)
        cv2.imwrite('images/stereoRight/img' + str(num) + '.png', img2)
        print("images saved!")
        num += 1

    cv2.imshow('Img Left',img)
    cv2.imshow('Img Right',img2)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows() 