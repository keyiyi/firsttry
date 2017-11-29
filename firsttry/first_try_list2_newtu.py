from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import json
import webbrowser
from tunews import get_all_note,get_all_note2



with open('tickets.json','r') as f:   #从json文件中读取3455支股票代码
    tickets = json.load(f)
code_list = list(tickets[i]['code'] for i in range(len(tickets)))

news_titles = []
news_urls = []

def right_code(str):
    #判断是否是股票代码
    if str in code_list:
        return True
    else:
        return False



def get_information(*args):
    global news_titles, news_urls
    text_list_frame.insert('end', '正在查询，请稍候...')
    strings = str(codevar.get())
    if right_code(strings):
        text_list_frame.delete(0, END)
        if keywordsvar.get() != 'is':
            #news_titles, dates, news_urls = get_news(strings)
            news_titles, dates, news_urls = get_all_note(strings)
        elif keywordsvar.get() == 'is':
            #news_titles,dates,news_urls = get_news2(strings)
            news_titles, dates, news_urls = get_all_note2(strings)
        if len(news_titles) > 0:
            new_list = [dates[i] + '>>' + news_titles[i] for i in range(len(news_titles))]
            listvar.set(value=new_list)
            statuvar.set('You got ' + str(len(news_titles)) + ' news.Doulbe click a title to see detail.')
        else:
            text_list_frame.insert('end','没有找到结果。')
    else:
        messagebox.showinfo(message='Please input the right code!\n请输入正确的股票代码。')



def open_url(*args):
    #打开单条新闻网址
    idxs = text_list_frame.curselection()
    if len(idxs) ==1:
        idx = int(idxs[0])
        url = news_urls[idx]
        webbrowser.open_new(url)
    
        
        
def get_name(*args):
    #当选中／输入代码后，显示相应的公司中文简称
    code_str = str(codevar.get())
    name_str = ''
    for i in range(len(tickets)):
        if code_str == tickets[i]['code']:
            name_str = tickets[i]['name']
    namevar.set(name_str)


def clear_text(*args):
    #当按下按键清除各部件的文字显示
    text_list_frame.delete(0, END)
    namevar.set('')
    code.set('')
    statuvar.set('')
    text_list_frame.insert('0', '选择或输入股票代码，按Get News获得新闻，或按Quit退出。')
    text_list_frame.insert('end', '本程序使用过程中会比较慢，请耐心等待^_^')
    text_list_frame.insert('end', '本程序使用过程必须连接互联网（Connect internet to run this App)')
    keywordsvar.set('')
    
    
root = Tk()
root.title('GET NEWS')

mainframe = ttk.Frame(root,padding = '3 3 20 20')
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)
root.resizable(width=False, height=False)
mainframe['borderwidth'] = 2
mainframe['relief'] = 'sunken'

codevar = StringVar() #输入框中的股票代码
namevar = StringVar() #标签公司简称
statuvar = StringVar() #结果列表简况，比如多少条新闻
listvar = StringVar()  #结果列表文字，列表
keywordsvar = StringVar()
# keywordsvar2 = BooleanVar()



label1 = ttk.Label(mainframe,text= "News' table:",)
label2 = ttk.Label(mainframe,text = "Please choice or enter a code:\n请选择或输入股票代码")
label3 = ttk.Label(mainframe,text = "Name:")
label4 = ttk.Label(mainframe,textvariable = namevar,)
label6 = ttk.Label(mainframe,textvariable = statuvar,)
botton1 = ttk.Button(mainframe,text = 'Quit',command = root.destroy)  #退出键
botton2 = ttk.Button(mainframe,text = 'Get News',command = get_information) #获取新闻按键
#botton2 = ttk.Button(mainframe,text = 'Get News',command = get_information) #获取新闻按键
botton3 = ttk.Button(mainframe,text = 'Reset',command = clear_text)    #重置键
code = ttk.Combobox(mainframe,textvariable = codevar,value = code_list,width = 12)  #代码输入框（列表）
checkbotton1 = ttk.Radiobutton(mainframe,text= '质押类公告',variable = keywordsvar,value = 'is')
checkbotton2 = ttk.Radiobutton(mainframe,text= '全部公告',variable = keywordsvar,value = 'not')
#code['value'] = code_list
text_list_frame = Listbox(mainframe, width = 60,height = 10,listvariable = listvar)  #结果列表，即新闻列表
text_list_frame.insert('0','选择或输入股票代码，并按Get News获得新闻，或按Quit退出。')
text_list_frame.insert('end','本程序使用tushare api 获得指定股票的新闻，新闻数量受tushare默认设置限制^_^')
text_list_frame.insert('end','本程序使用过程必须连接互联网（Connect internet to run this App)')

scroll = ttk.Scrollbar(mainframe, orient=VERTICAL, command=text_list_frame.yview)  #滚动条
scroll2 = ttk.Scrollbar(mainframe, orient=HORIZONTAL, command=text_list_frame.xview)

label2.grid(row = 0, column = 0,columnspan =2,sticky = W,padx = 10,pady = 5)
code.grid(row=1,column = 0,sticky = W,padx = 10,pady = 5)
label3.grid(row=2,column =0,sticky = W,padx = 10,pady = 5)
label4.grid(row =2,column =0,sticky = W,padx = 55,pady = 5)
checkbotton1.grid(row = 1,column = 2,sticky = W,padx = 5)
checkbotton2.grid(row = 1,column = 3,sticky = W,padx = 5)
botton3.grid(row =3,column = 0,sticky = W,padx = 10,pady = 5)
botton2.grid(row = 3,column = 2)
botton1.grid(row =3,column = 3)
label1.grid(row = 4,column = 0,sticky = W,padx = 5)
text_list_frame.grid(row = 5,column = 0,columnspan = 4,sticky = W,padx = 1,pady = 5)
scroll.grid(row = 5,column = 4,sticky=(N,S,E))
scroll2.grid(row = 6,column = 0,columnspan = 4,sticky=(W,E,S),padx = 1,pady = 1)
label6.grid(row =7,column = 0,sticky = W,padx = 1,pady = 1)


text_list_frame['yscrollcommand'] = scroll.set
text_list_frame['xscrollcommand'] = scroll2.set
# label1.grid(row =0,column = 0,sticky = W,padx=15,pady = 5)
# label2.grid(row =0,column = 2+1,sticky = W,columnspan = 2,padx=5,pady = 5)
#
#
# text_list_frame.grid(row =2,column = 0,columnspan = 2,rowspan = 4,padx=5,sticky=(W,E))
# scroll.grid(row = 2, column =1,rowspan = 4,sticky=(N,S,E),padx=0,pady = 0)
# scroll2.grid(row = 5, column =0,columnspan = 2,sticky=(W,E,S),pady=0)
# code.grid(row = 2 ,column = 2+1,sticky = W,columnspan = 2,padx=10)
# label3.grid(row=3,column=2+1,sticky =W,pady =5,padx =10)
# label4.grid(row=3,column=2+1,columnspan = 2,sticky = W,pady =5,padx =55)
# label6.grid(row=6,column = 0,sticky =W, padx =9,pady = 5)
# botton3.grid(row = 4, column = 2+1,rowspan =2 ,padx =10,pady = 35,sticky = (E,S))
# botton1.grid(row = 5, column = 3+1,padx=2,pady = 2,sticky = (S,W,))
# botton2.grid(row = 5, column = 2+1,padx =10,pady = 2,sticky = (E,S,))



#text_frame.bind("<KeyPress>",lambda e : "break")
code.bind('<<ComboboxSelected>>', get_name)
code.bind('<Return>',get_name)
text_list_frame.bind('<Double-1>', open_url)
#text1(state = 'disable')
#code.bind('enter',get_info)
#botton2.bind('1',get_info)
#code.bind('<Enter>',get_info)
#code.bind("<KeyPress>",lambda e : "break")
#root.columnconfigure(0, weight=1)
#root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(5, weight=1)
mainframe.rowconfigure(4, weight=1)
mainframe.rowconfigure(2, weight=1)


root.mainloop()

