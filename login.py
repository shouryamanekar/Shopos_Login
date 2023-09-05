from tkinter import *
import tkinter.messagebox as box
from selenium import webdriver
import ctypes

def dialog1():
    username2=entry1.get()
    password2= entry2.get()

    

    box.showinfo('info','Login Success')
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\chromedriver.exe')

    def login(url,username, user, password, passw, loginbutton):
        driver.get(url)
        driver.find_element_by_id(username).send_keys(user)
        driver.find_element_by_id(password).send_keys(passw)
        driver.find_element_by_id(loginbutton).click()
        driver.minimize_window()
    login("http://172.16.1.1:8090/httpclient.html?u=http://www.gstatic.com/generate_204", "username", username2 , "password", password2, "loginbutton")

    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

    
    quit()


window = Tk()
window.title('Internet')

frame = Frame(window)

Label1 = Label(window,text = 'Username:')
Label1.pack(padx=15,pady= 5)

entry1 = Entry(window,bd =5)
entry1.pack(padx=15, pady=5)



Label2 = Label(window,text = 'Password: ')
Label2.pack(padx = 15,pady=6)

entry2 = Entry(window, bd=5)
entry2.pack(padx = 15,pady=7)



var1 = IntVar()
Checkbutton(window, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(window, text="female", variable=var2).grid(row=1, sticky=W)

btn = Button(frame, text = 'Connect',command = dialog1)


btn.pack(side = RIGHT , padx =5)
frame.pack(padx=100,pady = 19)
window.mainloop()