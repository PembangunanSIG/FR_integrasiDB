import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Image, Text
import cv2
from cv2 import data
import numpy as np
import face_recognition
import os
import asyncio
import imutils
from library import HandTrackingModule as htm
from library import fungsi_fungsi as ff
from library import db
from library import log


waktu   = ff.RealTime()
tanggal = ff.RealDate()


def main():
    path = 'FotoSempel'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    cap = cv2.VideoCapture(1)                            # Setup the OpenCV capture device (webcam)


    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    def GUI_Datang(nama, foto):
        print(type(nama))
        print(type(foto))
        namaFile = ff.RealDate_Nama()+ '_' + nama + '_' + ff.RealTime_Nama() + '_Datang'
        print(namaFile)
        frame = imutils.resize(foto, width=400)    
        cv2.imwrite('library/log/' + namaFile +'.png', frame)
        window["-FOTO-"].update(filename='library/log/' + namaFile + '.png')
        window["-NAMA-"].update(nama)
        window["-STATUS-"].update('Datang')
        window['-WAKTU-'].update ( waktu + '  ||  ' + tanggal )
    def GUI_Pulang(nama, foto):
        print(type(nama))
        print(type(foto))
        namaFile = ff.RealDate_Nama()+ '_' + nama + '_' + ff.RealTime_Nama() + '_Pulang'
        frame = imutils.resize(foto, width=400)
        cv2.imwrite('library/log/' + namaFile +'.png', frame)
        window["-FOTO-"].update(filename='library/log/' + namaFile + '.png')
        window['-NAMA-'].update(nama)
        window['-STATUS-'].update('Pulang')
        window['-WAKTU-'].update ( waktu + '  ||  ' + tanggal )
                        
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def bacaData():
        with open('library/data.csv', 'r') as f:
            data = f.readline()
            return data
    def dataSampelDatang(name):
        with open('library/data.csv', 'w') as f:
            if (name != 'unknown'):
                f.writelines(f'{tanggal + name + "DATANG"}')
    def dataSampelPulang(name):
        with open('library/data.csv', 'w') as f:
            if (name != 'unknown'):
                f.writelines(f'{tanggal + name + "PULANG"}')
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    top_banner = [[sg.Text('Persensi Face Recognition :'+ ' '*64, font='Any 27', background_color='#34495E', text_color='#E5E7E9'),
                sg.Text(tanggal, font='Any 27', background_color='#34495E', text_color='#E5E7E9')]]


    webcam = [[sg.Image(filename='', key='-WEBCAM-' ,tooltip='Right click for exit menu',pad=((7,20),(10.20)) , background_color='#34495E')]]
    foto = [[sg.Image(key='-FOTO-', background_color='#34495E', size=(400, 300), pad=((0,20),(10.10)))]]
    status  = [
                    [sg.Text('Nama :       ', font='Any 15', background_color='#CACFD2', text_color='#34495E')],
                    [sg.Text('   ', background_color='#D5DBDB'),sg.Text(size=(21,1), key='-NAMA-', font='Any 15', background_color='#D5DBDB', text_color='#34495E')],
                    [sg.Text('Waktu :      ', font='Any 15', background_color='#CACFD2', text_color='#34495E')],
                    [sg.Text('   ', background_color='#D5DBDB'),sg.Text(size=(21,1), key='-WAKTU-', font='Any 15', background_color='#D5DBDB', text_color='#34495E')],
                    [sg.Text('Status :      ',font='Any 15', background_color='#CACFD2', text_color='#34495E')],
                    [sg.Text('   ', background_color='#D5DBDB'),sg.Text(size=(21,1), key='-STATUS-', font='Any 15', background_color='#D5DBDB', text_color='#34495E')], 
                ]
    tombol = [[sg.Button('Datang', size=(19, 2), font='Any 13'), sg.Button('Pulang', size=(19, 2), font='Any 13')]]

    layoutKanan = [ [sg.Column(foto, size=(410, 350), background_color='#EAEDED')],
                    [sg.Column(status, size=(410, 210), background_color='#D5DBDB')],
                    [sg.Column(tombol, background_color='#EAEDED')]
                    ]

    layoutFinal = [ [sg.Column(top_banner, size=(1280,60),  background_color='#34495E')],
                    [sg.Column(webcam, background_color='#EAEDED'),
                    sg.VSeparator(),
                    sg.Column(layoutKanan, size=(400, 680), background_color='#EAEDED')
                ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration', layoutFinal, 
                        # location=(800,400),
                        background_color='#EAEDED',
                        no_titlebar=True, grab_anywhere=True,
                        right_click_menu=['&Right', ['E&xit']], ).Finalize()  # if trying Qt, you will need to remove this right click menu
    window.maximize()




    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    async def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = asyncio.run(findEncodings(images))
    print('Encoding Complete')

    detectorTangan = htm.handDetector ( detectionCon=0.75 )
    tipIds = [4, 8, 12, 16, 20]

    while True:
        event, values = window.read(timeout=20)
        if event in ('Exit', None):
            break
            # App.main()

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        #                                         = = = = = = = = = = = = = =   T O M B O L   S P E S I A L    = = = = = = = = = = = = = = = = = = = =
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        def handButton(nama_db,nama_FotoSempel, nama_lengkap, FotoSempel):
            imgH = detectorTangan.findHands ( img )
            lmList = detectorTangan.findPosition ( imgH, draw=False )
            if len ( lmList ) != 0:
                fingers = []

                # Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append ( 1 )
                else:
                    fingers.append ( 0 )

                # 4 Fingers
                for id in range ( 1, 5 ):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append ( 1 )
                    else:
                        fingers.append ( 0 )

                # print(fingers)
                totalFingers = fingers.count ( 1 )
                print ( totalFingers )

                if totalFingers == 5:
                    if bacaData() != tanggal + nama_lengkap + "DATANG":
                        dataSampelDatang(nama_lengkap)
                        print ( 'Datang' )
                        GUI_Datang(nama_lengkap, FotoSempel)
                        db.inputKehadiran(nama_db,nama_FotoSempel, nama_lengkap, tanggal, waktu, "DATANG")
                        
                if totalFingers == 1:
                    if bacaData() != tanggal + nama_lengkap + "PULANG":
                        dataSampelPulang(nama_lengkap)
                        print ( 'Pulang' )
                        GUI_Pulang(nama_lengkap, FotoSempel)
                        db.inputKehadiran(nama_db,nama_FotoSempel, nama_lengkap, tanggal, waktu, "PULANG")
                        # attendance_pulang(nameMentah)

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        ret, frame = cap.read()
        img = imutils.resize(frame, width=800)
        # img = cv2.resize(imgO(00, 150))
        # resize = cv2.resize(image, (176, 144))                  
        imgS = cv2.resize(img, (0,0),None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        def faceRec():
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    nama_FotoSempel = classNames[matchIndex].upper()
                    nama_panggilan = db.ambil_panggilan(nama_FotoSempel)
                    nama_lengkap = db.ambil_nama(nama_FotoSempel)
                    nama_db = db.ambil_db(nama_FotoSempel)
                    
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (94, 73, 52), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (94, 73, 52), cv2.FILLED)
                    cv2.putText(img, nama_panggilan, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (202, 207, 210), 2)
            
                    if event == 'Datang':
                        if bacaData() != tanggal + nama_lengkap + "DATANG":
                            dataSampelDatang(nama_lengkap)
                            GUI_Datang(nama_lengkap, img)
                            db.inputKehadiran(nama_db,nama_FotoSempel, nama_lengkap, tanggal, waktu, "DATANG")
                            print('Datang')
                        
                    elif event == 'Pulang':
                        if bacaData() != tanggal + nama_lengkap + "PULANG":
                            dataSampelPulang(nama_lengkap)
                            GUI_Pulang(nama_lengkap, img)
                            db.inputKehadiran(nama_db,nama_FotoSempel, nama_lengkap, tanggal, waktu, "PULANG")
                            print('Pulang')
                    handButton(nama_db, nama_FotoSempel, nama_lengkap, img)
                    # handButton(nama_lengkap, img)

                    # print (bacaData() + "1")
                    # print (tanggal + nama_FotoSempel + "DATANG" + "2")
                    # handButton(name, nameMentah)
            return img
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        

        # ret, frame = cap.read()                             # Read image from capture device (camera)
        gambar = faceRec()
        imgbytes=cv2.imencode('.png', gambar)[1].tobytes()   # Convert the image to PNG Bytes
        window['-WEBCAM-'].update(data=imgbytes)   # Change the Image Element to show the new image
        
    
    window.close()

main()
