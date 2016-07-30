from tkMessageBox import askokcancel, showerror
import _thread as thread,queue, os
#import os
from pylab import *
from scipy import *
from glob import glob
from tkinter import *
import subprocess
import Tkinter as tk
import Image
textdir = 'C:\Users\RajPratim\Documents\\amazon.in\\amazonin\\amazonin'
textfile = 'reviews.csv'
Textpath =  " "
sun =1
flag = 0
flagQueue = queue.Queue()
childprocess = subprocess
imgpath =  'images.gif'
root = Tk()
i =1
s1= 0
s2 = 0
s3 = 0
s4 = 0
thread_idf = thread
thread_impsent = thread
root.wm_title("SkyGist")
root.geometry("1200x600")

def fetch(entries,ipath,tpath):
    can.delete("all")
    can2.delete("all")
    for entry in entries:
        print 'Input=> "%s"' %entry.get()
        textlen = len(Textpath)
        print textlen
    #img = Image.open(ipath)
    img = PhotoImage(file = ipath)
    #can2.create_text(20,10,text = "Hello World aaaaaaaaaa aaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaa aaaaaaaaaa",width = 180,anchor = NW)
    can2.create_image(20, 70, image=img, anchor=NW)

    can.config(  yscrollcommand=vbar.set)
    can2.pack(side=LEFT, expand=True, fill=BOTH)
    can.pack(side=LEFT, expand=True, fill=BOTH)

    with  open(tpath ,'r') as f:
        i = 60
        for line in f:
            l = len(line)
            l/=11
            if line[0] == '5':
                can.create_text(20,i, text = line,font=("Arial", 12),anchor = NW,fill = '#d90000',width = 400)
            elif line[0] =='4':
                can.create_text(20, i, text=line, anchor=NW,fill = '#0000ff',width = 400,font=("Arial", 12))
            elif line[0] =='3':
                can.create_text(20, i, text=line, anchor=NW,fill = '#00a000',width = 400,font=("Arial", 12))
            elif line[0] == '2':
                can.create_text(20, i, text=line, anchor=NW,fill = '#007070',width = 400,font=("Arial", 12))
            elif line[0] == '1':
                can.create_text(20, i, text=line, anchor=NW,fill = '#ff8f00',width = 400,font=("Arial", 12))
            else:
                can.create_text(20, i, text=line, anchor=NW, width=400, font=("Arial", 12))
            i+=l*5+20
    print "Raj"
    root.mainloop()

def fetch2(entries ):
    can3.delete("all")
    global thread_idf
    #global Textpath
    print "textpath",Textpath

    thread.start_new_thread(NewThreadedProcess_tf_idf,(Textpath,) )

def NewThreadedProcess_tf_idf(command):
    global childprocess
    childprocess = subprocess.Popen(['Python', 'tf_idf_trigram.py',command] )
    childprocess.wait()
    childprocess.terminate()
    global flag
    if flag == 0:
        Writer_tfidf()
    else:
        flag = 0

def Writer_tfidf():

    with  open( 'output_ranking.txt', 'r') as f:
        i = 60
        for line in f:
            can3.create_text(20, i, text=line, anchor=NW, font=("Arial", 12))
            i += 25
    #thread.exit()
    root.mainloop()

def NewThreadedProcess_important_sentences(command):

    global childprocess
    childprocess = subprocess.Popen(['Python', 'text_analysis7.py',command] )
    childprocess.wait()
    childprocess.terminate()
    global flag
    if flag == 0:
        Writer_impsent()
    else:
        flag = 0

def Writer_impsent():
    with  open('summary_output.txt', 'r') as f:
        i = 60
        for line in f:
            l = len(line)
            l /= 20
            print l
            can4.create_text(20, i, text=line, anchor=NW, width=300, font=("Arial", 12))
            i += l * 10 + 30
    #thread.exit()
    root.mainloop()


def fetch3(entries):
    #global Textpath
    can4.delete("all")
    global thread_impsent
    thread_impsent = thread.start_new_thread(NewThreadedProcess_important_sentences,(Textpath,))


def scrap(en,entry,opweb ):

    if en.get().lower()=="iphone 5s" :
        global Textpath
        Textpath = 'reviews_amazoncom.csv'
        fetch(entry,imgpath,'reviews_iphone5s.csv')
        #Textpath = 'reviews_amazoncom.csv'
    elif en.get().lower() == 'revolution 2020':
        Textpath = 'reviews_2020.csv'
        fetch(entry, 'Revolution_2020.gif','reviews_2020.csv')

        t = 2
    elif en.get().lower() == 'motog4':
        Textpath = 'reviews_motog.csv'
        fetch(entry,'Moto.gif','reviews_motog.csv')

    elif en.get().lower() == 'half girl friend':
        Textpath = 'reviews_Half_gf.csv'
        fetch(entry, 'halfgf.gif', 'reviews_motog.csv')

    elif en.get().lower() == 'twitter':
        Textpath = 'tweet.csv'
        fetch(entry, 'twitter-logo.gif', 'tweet.csv')

    else:
        thread.start_new_thread(NewThreadScrap,(en,entry,opweb))
Direct = os.getcwd()
print Direct
    #return textpath
def NewThreadScrap(en, entry,opweb):

    if opweb.get() == 'amazon.in':
        global childprocess
        global Textpath
        childprocess = subprocess.Popen(['scrapy', 'crawl', 'amazonin'],
                             cwd= Direct + "\\amazon.in\\amazonin\\amazonin\spiders"
                             , stdin=subprocess.PIPE)
        Textpath = 'amazon.in\\amazonin\\amazonin\spiders\\reviews.csv'
        childprocess.communicate(en.get())
        childprocess.wait()

    elif opweb.get() == 'amazon.com':
        childprocess = subprocess.Popen(['scrapy', 'crawl', 'amazoncom'],
                                        cwd=Direct + '\\amazoncom\\amazoncom\spiders'
                                        , stdin=subprocess.PIPE)
        Textpath = 'amazoncom\\amazoncom\spiders\\reviews_amazoncom.csv'
        childprocess.communicate(en.get())
        childprocess.wait()

    elif opweb.get() == 'flipkart.com':
        childprocess = subprocess.Popen(['scrapy', 'crawl', 'flipkart'],
                                        cwd= Direct+'\\flipkart\\flipkart\spiders'
                                        , stdin=subprocess.PIPE)
        Textpath = 'flipkart\\flipkart\spiders\\reviews_flipkart12.csv'
        childprocess.communicate(en.get())
        childprocess.wait()
    elif opweb.get() == 'twitter':
        notdone()

    elif opweb.get() == 'RBI bulletin':
        notdone()
    #childprocess.communicate(en.get())
    fetch(entry, "default-img.gif", Textpath)

def makeform(root):
    entries = []
    row = Frame(root)
    lab = Label(row, width =60 , text = 'Search')
    ent = Entry(lab,textvariable =1,width =40)
    row.pack()
    var = StringVar(root)
    var.set("amazon.in")  # initial value
    option = OptionMenu(lab, var, "amazon.com", "amazon.in", "flipkart.com", "twitter","RBI bulletin")
    option.pack(side=RIGHT)
    ent.pack(side = RIGHT)
    entries.append(ent)
    lab.pack()
    return entries,ent,var

def notdone():
    showerror('Not implented', 'Not yet availablle')

def statistics():
    s4 =1

    durl = 'http://datasets.flowingdata.com/crimeRatesByState2005.csv'
    rdata = genfromtxt('output-tfidf21.csv', dtype='S20,f', delimiter=',') #, dtype='S8,f,f,f,f,f,f,f,i'
    #rdata[0] = zeros(8)  # cutting the label's titles
    #rdata[1] = zeros(8)  # cutting the global statistics
    print rdata
    x = []
    y = []
    color = []
    area = []
    cou = 0
    for data in rdata:
       # data = rdata[len(rdata)-1-cou]
        if cou == 20:
            break
        sig = random_integers(-100,100,1)
        k = random_integers(100,800,1)
        l = random_integers(100,800,1)+sig
        c = random_integers(140,300,1)-sig
        x.append(l)  # murder
        y.append(k)  # burglary
        color.append(c)  # larceny_theft
        area.append((data[1]*200))  # population
        # plotting the first eigth letters of the state's name
        #print data[1]
        cou+=1
        text(l, k,
             data[0], size=8, horizontalalignment='center')

    # making the scatter plot
    sct = scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)

    axis([0, 1000, 0, 1000])
    xlabel('Murders per 100,000 population')
    ylabel('Burglaries per 100,000 population')
    show()
def stop_the_process():
    global flag
    flag = 1
    childprocess.terminate()

def makemenu(root,ents):
    top =  Menu(root)
    root.config(menu = top)

    file = Menu(top)
    file.add_command(label = 'Stop the running',command = stop_the_process,underline =0)
    file.add_command(label = 'Statistics',command = statistics,underline =0)
    file.add_command(label = 'Quit',command = lambda:sys.exit(0),underline =0)
    top.add_cascade(label = 'File', menu =  file, underline =0 )

    edit = Menu(top)
    edit.add_command(label='ranking_of_terms', command= lambda:fetch2(ents), underline=0)
    edit.add_command(label='important sentences', command=lambda:fetch3(ents), underline=0)
    top.add_cascade(label='Edit', menu=edit, underline=0)

    Submenu = Menu(edit, tearoff= True)
    Submenu.add_command(label ='Add new',command = root.quit,underline =0)
    Submenu.add_command(label='Add new', command=notdone , underline=0)
    edit.add_cascade(label = 'Stuff', menu = Submenu, underline =0)

if __name__ == '__main__':
    img = PhotoImage(file='partner_skybits.gif')
    panel = Label(root, image=img)
    panel.pack(side="top", fill="both", expand="No")
    ents,Ent,optionweb = makeform(root)
    makemenu(root,ents)
    #root.bind('<Return>',lambda event: fetch(ents))

    #Button(root, text ='Fetch',
     #           command = (lambda: fetch(ents))).pack(side = LEFT)
    lab2 = Label(root, width =160 , text = 'Search')
    butGetReviews =  Button(lab2, text='Get the reviews',
           command=(lambda : scrap(Ent,ents,optionweb)),width = 16)
    butGetReviews.pack(side=LEFT)
    btKeyTerms = Button(lab2, text='Key Phrases',
           command=(lambda : fetch2(ents)),width = 16).pack(side=LEFT)
    butImpSen = Button(lab2, text='Important Sentences',
           command=(lambda: fetch3(ents)),width = 16).pack(side=LEFT)
    btnStat = Button(lab2, text='Get the Statistics',
           command=(lambda: statistics()), width=16).pack(side=LEFT)
    lab2.pack()
    can2 = Canvas(root, width=800, height=600, bg='white', scrollregion=(0, 0, 800, 1000))
    can2.config(width=230, height=300)
    can2.pack(side=LEFT, expand=True, fill=BOTH)
    can2.create_text(80, 20, text="Product Image", anchor=N, width=400)
    can = Canvas(root, width=800, height=600, bg='white', scrollregion=(0, 0, 800, 25000))
    can.config(width=430, height=300)
    can.pack(side=LEFT, expand=True, fill=BOTH)
    can.create_text(190, 20, text="Reviews" , anchor=N, width=400)
    can3 = Canvas(root, width=800, height=600, bg='white', scrollregion=(0, 0, 8000, 15500))
    can3.config(width=230, height=300)
    can3.pack(side=LEFT, expand=True, fill=BOTH)
    can3.create_text(60, 20, text="Key Phrases", anchor=N, width=400)
    can4 = Canvas(root, width=800, height=600, bg='white', scrollregion=(0, 0, 800, 10000))
    can4.config(width=350, height=300)
    can4.pack(side=LEFT, expand=True, fill=BOTH)
    can4.create_text(200, 20, text="Important Sentences", anchor=N, width=300)
    vbar = Scrollbar(root, orient = VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=can.yview)

    vbar = Scrollbar(root, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=can3.yview)

    vbar = Scrollbar(root, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=can4.yview)


    root.mainloop()