import mysql.connector

# host = "localhost:3306"
host = "137.59.126.35"
user = "presensi_tedk"
passwd = "presensi_tedk123"
db   = "tedk"

mydb =  mysql.connector.connect(host=host, user=user, password=passwd, database=db)
print("Koneksi Berhasil")

# all data
def semua():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM data_siswa")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

# Mengambil data
# 1. mengambil nama
def ambil_panggilan(n):
    cursor = mydb.cursor()
    data = "SELECT panggilan FROM data_siswa WHERE nis=%s"
    cursor.execute(data, (n,))
    hasil = cursor.fetchone()
    hasil = "".join(str(e) for e in hasil) # Menhapus tanda kutip DB
    return hasil

def ambil_nama(n):
    cursor = mydb.cursor()
    data = "SELECT nama FROM data_siswa WHERE nis=%s"
    cursor.execute(data, (n,))
    hasil = cursor.fetchone()
    hasil = "".join(str(e) for e in hasil) # Menhapus tanda kutip DB
    return hasil

# b. mengambil db
def ambil_db(n):
    cursor = mydb.cursor()
    data = "SELECT angkatan, jurusan, kelas FROM data_siswa WHERE nis=%s"
    cursor.execute(data, (n,))
    hasil = cursor.fetchone()
    hasil = "".join(str(e) for e in hasil) # Menhapus tanda kutip DB
    return hasil


# menginpt data
def inputKehadiran(tabel, nis, nama, tanggal, waktu, status):
    mycursor = mydb.cursor()
    sql = "INSERT INTO "+ tabel +" (nis, nama, tanggal, waktu, status) VALUES (%s, %s, %s, %s, %s)"
    val = (nis, nama, tanggal, waktu, status)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def inputDataSiswa(nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa):
    mycursor = mydb.cursor()
    sql = "INSERT INTO data_siswa (nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (nis, nama, panggilan, angkatan, jurusan, kelas, email, no_wa)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record data_siswa inserted.")

# nis = 171113124
# tabel = ambil_db(nis)
# nama = ambil_nama(nis)
# tanggal = "23-12-09"
# waktu = "12:45"
# status = "datang"
# inputData(tabel, nis, nama, tanggal, waktu, "datang")

# print(type(ambil_panggilan(123123)))