###################################################################################################  Start Threads
def VideoUrl():
    DownloadingBarTextLable.configure(text="")
    DownloadnigLabelResult.configure(text="")
    DownloadnigSizeLabelResult.configure(text="")
    DownloadnigLabelTimeLeft.configure(text="")
    getdetail = threading.Thread(target=getvideo)
    getdetail.start()

def getvideo():
    global streams
    ListBox.delete(0, END)
    url = urltext.get()
    data = pafy.new(url)
    streams = data.allstreams
    index = 0
    for i in streams:
        du = '{:0.1f}'.format(i.get_filesize()//(1024*1024))
        datas = str(index) + '.'.ljust(3, ' ') + str(i.quality).ljust(10, ' ') + str(i.extension).ljust(5, ' ') + str(i.mediatype) + ' ' + du.rjust(10, ' ') + "MB"
        ListBox.insert(END, datas)
        index += 1
def SelectCursor(evt):
    global downloadindex
    listboxdata = ListBox.get(ListBox.curselection())
    print(listboxdata)
    downloadstream = listboxdata[:3]
    downloadindex = int(''.join(x for x in downloadstream if x.isdigit()))


def DownloadVideo():
    getdata = threading.Thread(target=DownloadVideoData)
    getdata.start()

def DownloadVideoData():
    global downloadindex
    fgr = filedialog.askdirectory()
    DownloadingBarTextLable.configure(text="Downloading.....")
    def mycallback(total, recvd, ratio, rate, eta):
        global total12
        total12 = float('{:.5}'.format(total/(1024*1024)))
        DownloadnigProgressBar.configure(maximum=total12)
        recieved1 = '{:.5} mb'.format(recvd / (1024 * 1024))
        eta1 = '{:.2f} sec'.format(eta)
        DownloadnigSizeLabelResult.configure(text=total12)
        DownloadnigLabelResult.configure(text=recieved1)
        DownloadnigLabelTimeLeft.configure(text=eta1)
        DownloadnigProgressBar['value'] = recvd/(1024*1024)

    streams[downloadindex].download(filepath=fgr, quiet=True, callback=mycallback)
    DownloadingBarTextLable.configure(text="Downloaded")


#####################################################################################################

def ChangeIntroLabelColor():
    ss = random.choice(colors)
    IntroLabel.configure(fg=ss)
    IntroLabel.after(20, ChangeIntroLabelColor)

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import random
import threading
import pafy

root = Tk()
root.configure(bg='olivedrab1')
root.geometry('780x500')
root.resizable(False, False)
root.attributes()
root.iconbitmap('YouTube.ico')

downloadindex = 0
total12 = 0
streams = ""
colors = ['red', 'green', 'blue', 'yellow', 'gold', 'pink']
############################################################################################   ScrollBar
scrollbar = Scrollbar(root)
scrollbar.place(x=477, y=230, height=193, width=20)
############################################################################################  Entry
urltext = StringVar()
UrlEntry = Entry(root, textvariable=urltext, font=('arial', 20, 'italic bold'), width=31)
UrlEntry.place(x=20, y=150)

############################################################################################  Labels
IntroLabel = Label(root, text='Welcome to Youtube Video Audio Downloader ', width=36, relief='ridge', bd=4,
                   font=('chiller', 40, 'italic bold'), fg='red')
IntroLabel.place(x=10, y=20)
ChangeIntroLabelColor()

ListBox = Listbox(root, yscrollcommand=scrollbar.set, width=50, height=10, font=('arial', 12, 'italic bold'),
                  relief='ridge', bd=2, highlightcolor="blue", highlightbackground="orange", highlightthickness=2)
ListBox.place(x=20, y=230)
ListBox.bind("<<ListboxSelect>>", SelectCursor)

scrollbar.configure(command=ListBox.yview)

DownloadnigSizeLabel = Label(root, text='Total Size : ', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigSizeLabel.place(x=500, y=240)

DownloadnigLabel = Label(root, text='Recieved Size : ', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigLabel.place(x=500, y=290)

DownloadnigTime = Label(root, text='Time Left  : ', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigTime.place(x=500, y=340)

DownloadnigSizeLabelResult = Label(root, text='', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigSizeLabelResult.place(x=650, y=240)

DownloadnigLabelResult = Label(root, text='', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigLabelResult.place(x=650, y=290)

DownloadnigLabelTimeLeft = Label(root, text='', font=('arial', 15, 'italic bold'), bg='olivedrab1')
DownloadnigLabelTimeLeft.place(x=650, y=340)

DownloadingBarTextLable = Label(root, text='Downloading bar', width=36, font=('chiller', 23, 'italic bold'), fg='red',
                    bg='olivedrab1')
DownloadingBarTextLable.place(x=370, y=445)

DownloadingProgressBarLabel = Label(root, text='', width=36, font=('chiller', 40, 'italic bold'), fg='red', bg='olivedrab1',
                     relief='raised')
DownloadingProgressBarLabel.place(x=20, y=445)


###########################################################################################  Progressbar

DownloadnigProgressBar = Progressbar(DownloadingProgressBarLabel, orient=HORIZONTAL, value=0, length=100, maximum= total12)
DownloadnigProgressBar.grid(row=0, column=0, ipadx=185, ipady=3)

#####################################################################################################  Buttons
ClickButton = Button(root, text='Enter Url And Click', font=('Arial', 10, 'italic bold'), bg='green', fg='red',
                     activebackground='blue', width=23, bd=8, command=VideoUrl)
ClickButton.place(x=530, y=150)

DownloadButton = Button(root, text='Download', font=('Arial', 10, 'italic bold'), bg='red', fg='white',
                        activebackground='blue', width=23, bd=8, command=DownloadVideo)
DownloadButton.place(x=530, y=370)
################################################################################## Create Threads
root.mainloop()