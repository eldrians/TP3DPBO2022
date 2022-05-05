from ast import Lambda
from cProfile import label
from ctypes.wintypes import PINT
from tkinter import *
from PIL import ImageTk, Image
from pydoc import TextDoc
import tkinter as tk
from tkinter import ttk
import mysql.connector
import sqlite3

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tp3dpbo2022"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


def getJenisKelamin():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT jenis_kelamin FROM mahasiswa")
    result = dbcursor.fetchall()

    return result

# Window Input Data


def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(
        row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # =====================================================================================
    # Input 3
    gender = StringVar()
    gender.set('Pria')
    label3 = Label(dframe, text="Jenis Kelamin").grid(
        row=2, column=0, sticky="w")
    Radiobutton(dframe, text="Pria", variable=gender, value="Pria").grid(
        row=2, column=1, padx=20, pady=10, sticky="w")
    Radiobutton(dframe, text="Wanita", variable=gender, value="Wanita").grid(
        row=3, column=1, padx=20, pady=0, sticky="w")
    gander_value = gender.get()
    # =====================================================================================

    # Input 4
    options = ["Filsafat Meme", "Sastra Mesin",
               "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=4, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=4, column=1, padx=20, pady=10, sticky='w')

    # =====================================================================================
    # Input 5
    label5 = Label(dframe, text="hobi").grid(row=5, column=0, sticky="w")
    hobi = StringVar()
    pilihanHobi = ttk.Combobox(dframe, width=27, textvariable=hobi)

    # Adding combobox drop down list
    pilihanHobi['values'] = ('bernyanyi',
                             ' bermain games',
                             ' bermain musik',
                             ' begadang',
                             ' coding',
                             ' baca Alquran')

    pilihanHobi.current(2)
    pilihanHobi.grid(column=1, row=5, padx=20, pady=10, sticky='w')

    # =====================================================================================
    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit", anchor="s", command=lambda: [insertData(
        top, input_nama, input_nim, input_jurusan, gender.get(), pilihanHobi.get()), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Back", anchor="s", command=lambda: [
                        top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

    btn_submit2 = Button(frame2, text="Hapus", anchor="s",
                         command=lambda: clear())
    btn_submit2.grid(row=3, column=2, padx=10)
    # clear sumbit

    def clear():

        # clear the content of text entry box
        input_nama.delete(0, END)
        input_nim.delete(0, END)
        gender.delete(0, END)
        input4.delete(0, END)
        pilihanHobi.delete("", END)


# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, gender, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    gender = gender
    hobi = hobi
    if(nama == "" or nim == "" or jurusan == "" or gender == "" or hobi == ""):
        btn_ok = Button(top, text="isi semua form!!", anchor="s",
                        command=lambda: [top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
        # Input data disini
    else:
        dbcursor = mydb.cursor()
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan, jenis_kelamin, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, gender, hobi)
        dbcursor.execute(sql, val)
        mydb.commit()
        print(dbcursor.rowcount, "data berhasil di masukkan")
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda: [
                        top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)

# Window Semua Mahasiswa


def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column=0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1,
                   relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1,
                   relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1,
                       relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid",
                       height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data


def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green",
                     fg="white", command=lambda: [top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red",
                    fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI


def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white",
                     command=lambda: [top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white",
                    command=lambda: [top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)


def delAll():
    top = Toplevel()
    # Delete data disini
    dbsql = mydb.cursor()
    sql = "TRUNCATE mahasiswa"
    dbsql.execute(sql)
    mydb.commit()
    print(dbsql, "Table has been reset")
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)


def fasilitasKampus():
    global root
    global nextButton
    global backButton
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas")
    dframe = LabelFrame(top, text="Daftar Fasilitas", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    A = ImageTk.PhotoImage(Image.open('python-db/gambar/gambarD.jpg'))
    B = ImageTk.PhotoImage(Image.open('python-db/gambar/gambarB.jpg'))
    C = ImageTk.PhotoImage(Image.open('python-db/gambar/gambarC.jpg'))
    D = ImageTk.PhotoImage(Image.open('python-db/gambar/gambarD.jpg'))
    E = ImageTk.PhotoImage(Image.open('python-db/gambar/gambarE.jpg'))

    image_list = [A, B, C, D, E]

    my_label = Label(dframe, image=A)
    my_label.grid(row=0, column=0, columnspan=3)
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    def buttonNextBack(nomorImage, my_label):
        my_label.grid_forget()
        my_label = Label(dframe, image=image_list[nomorImage - 1])
        nextButton = Button(dframe, text="-->", command=lambda: buttonNextBack(nomorImage + 1, my_label))
        backButton = Button(dframe, text="<--", command=lambda: buttonNextBack(nomorImage - 1, my_label))
        my_label.grid(row=0, column=0, columnspan=3)
        backButton.grid(row=1, column=0)
        nextButton.grid(row=1, column=2)

    backButton = Button(
        dframe, text="<--", command=lambda: buttonNextBack(), state=DISABLED)
    btn_cancel = Button(dframe, text="Kembali", anchor="w",
                        command=lambda: [top.destroy(), root.deiconify()])
    nextButton = Button(
        dframe, text="-->", command=lambda: buttonNextBack(2, my_label))

    backButton.grid(row=1, column=0)
    btn_cancel.grid(row=1, column=1)
    nextButton.grid(row=1, column=2)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa",
               command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa",
               command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa",
                 command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Facilities btn
b_fasilitas = Button(buttonGroup, text="Fasilitas Kampus",
                     command=fasilitasKampus, width=30)
b_fasilitas.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()
