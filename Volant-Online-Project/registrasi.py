import PySimpleGUI as sg
import cv2
import face_recognition
import os
from library import db


def main():
    sg.theme("BluePurple")
    
    

    def foto(nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa, foto):
        FileFoto = 'FotoSempel/' + nis +'.png'
        cv2.imwrite(FileFoto, foto)

        cv2.waitKey(30)
        image = face_recognition.load_image_file(FileFoto)
        face_locations = face_recognition.face_locations(image)
        jumlahWajah = len(face_locations)
        # return jumlahWajah
        if jumlahWajah == 1:
            window['-STATUS-'].update('Wajah '+panggilan+' Terdeteksi', background_color='#3EF56D')
            print('OK')
        elif jumlahWajah > 1:
            window['-STATUS-'].update('Terlalu Banyak '+panggilan, background_color='#F53E3E')
            print('Jangan Berkerumun')
            os.remove(FileFoto)
        elif jumlahWajah == 0:
            window['-STATUS-'].update(panggilan+' Tidak Terdeteksi', background_color='#FC4646')
            print('gaada foto')
            os.remove(FileFoto)

        db.inputDataSiswa(nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa)

        
    # Define the window layout
    layout = [
        [sg.Text("R E G I S T R A S I", font='Any 17 bold bold', text_color='#5990F6')],
        [
        [sg.Image(filename="", key="-IMAGE-")],
        sg.VSeparator(),
        [
            [sg.Text('NIS :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_NIS-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_NIS-')],
            [sg.Text('Nama :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_NAMA-', font='Any 7', text_color='#5990F6'),],
            [sg.Input(key='-IN_NAMA-')],
            [sg.Text('Panggilan :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_PANGGILAN-', font='Any 7', text_color='#5990F6'),],
            [sg.Input(key='-IN_PANGGILAN-')],
            [sg.Text('Angkatan :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_ANGKATAN-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_ANGKATAN-')],
            [sg.Text('Jurusan :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_JURUSAN-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_JURUSAN-')],
            [sg.Text('Kelas :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_KELAS-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_KELAS-')],
            [sg.Text('Email :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_EMAIL-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_EMAIL-')],
            [sg.Text('No WhatsUp :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-OUT_NOWA-', font='Any 7', text_color='#5990F6')],
            [sg.Input(key='-IN_NOWA-')],

            [sg.Text('Status Foto :', font='Any 9 bold', text_color='#5990F6'), sg.Text(size=(15,1), key='-STATUS-', font='Any 7', text_color='#5990F6')],
            [sg.Button('Tambah Data', font='Any 7', button_color='#5990F6')]
        ]
        ]]
    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(800, 400))

    cap = cv2.VideoCapture(1)
    cap.set(3, 300)
    # cap.set(4, 400)

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()
        if event == 'Tambah Data':
            # Update the "output" text element
            # to be the value of "input" element
            window['-OUT_NIS-'].update(values['-IN_NIS-'])
            window['-OUT_NAMA-'].update(values['-IN_NAMA-'])
            window['-OUT_PANGGILAN-'].update(values['-IN_PANGGILAN-'])
            window['-OUT_ANGKATAN-'].update(values['-IN_ANGKATAN-'])
            window['-OUT_JURUSAN-'].update(values['-IN_JURUSAN-'])

            
            window['-OUT_KELAS-'].update(values['-IN_KELAS-'])
            window['-OUT_EMAIL-'].update(values['-IN_EMAIL-'])
            window['-OUT_NOWA-'].update(values['-IN_NOWA-'])
            # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
            nis = values['-IN_NIS-']
            nama = values['-IN_NAMA-']
            panggilan = values['-IN_PANGGILAN-']
            angkatan = values['-IN_ANGKATAN-']
            jurusan = values['-IN_JURUSAN-']
            kelas = values['-IN_KELAS-']
            email = values['-IN_EMAIL-']
            no_wa = values['-IN_NOWA-']
            # query()
            foto(nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa, frame)
        
            # print(nama)
            # # print(nis)
            # print(kelas)
            # # print(jurusan)
            
            

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

main()
