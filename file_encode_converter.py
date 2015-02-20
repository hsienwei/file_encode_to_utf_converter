# coding=utf8
import chardet
import os
from Tkinter import *
import Tkconstants, tkFileDialog

class Application(Frame):
    def ask_dir(self):

        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = '選擇目標文件夾'

        filename = tkFileDialog.askdirectory(**self.dir_opt)
        self.inputField.delete(0, len(self.inputField.get()));
        self.inputField.insert(0, filename)

    def _file_spilt(self, file_path):
        fileName, fileExtension = os.path.splitext(file_path)                
        fileExtension_no_dot  = fileExtension[1:].lower()
        return fileExtension_no_dot in self.process_ext_ary

    def _file_convert(self, file_path):
        print 'convert ' + file_path
        with open(file_path, "r") as f:
            file_data = f.read() 
            det_data = chardet.detect(file_data)  

            if det_data['encoding'] == 'ascii': 
                print 'ascii pass.'
                return

            # 特定狀況: 如果在一個編碼為gb2312的文件中有繁體字, 則用gb2312解碼會有錯(不含繁體字), 需要用gbk解碼
            if det_data['encoding'] == 'GB2312':
                a_unicode = unicode(file_data, 'GBK',"replace")
            else:
                a_unicode = unicode(file_data, det_data['encoding'], "replace")
            a_utf_8 = a_unicode.encode('utf-8')
            f.close();    

            with open(file_path, "w") as f2:
                f2.write(a_utf_8)
                f2.close()

    def encode_convert(self):
        target_path = self.inputField.get()
       
        self.process_ext_ary = self.inputField2.get().split(',')
        for ndx, member in enumerate(self.process_ext_ary):
            self.process_ext_ary[ndx] = member.strip().lower()   

        if self.is_recusive.get() == 1:
            for root, dirs, files in os.walk(target_path):
                for f in files:
                    fullpath = os.path.join(root, f)
                    if os.path.isfile(fullpath):
                        if self._file_spilt(fullpath):
                            self._file_convert(fullpath)
        else:    
            for f in os.listdir(target_path):
                fullpath = os.path.join(target_path, f)
                if os.path.isfile(fullpath):
                    if self._file_spilt(fullpath):
                        self._file_convert(fullpath)
    
    def createWidgets(self):
        self.is_recusive = IntVar()
        self.label_dir_choose = Label(self, text="目標資料夾")
        self.label_dir_choose.pack({"anchor": "w", "padx":10})

        self.inputField = Entry(self, width=50)
        self.inputField.pack({"anchor": "w", "padx":10})

        self.inputButton = Button(self, text="選擇資料夾..", command=self.ask_dir)
        self.inputButton.pack({"anchor": "w", "padx":10})

        self.checkButton2 = Checkbutton(self,text="轉換子資料夾", variable=self.is_recusive)
        self.checkButton2.pack({"anchor": "w", "padx":10})

        self.label_extends_list = Label(self, text="目標副檔名(使用,區隔)")
        self.label_extends_list.pack({"anchor": "w", "padx":10})

        self.inputField2 = Entry(self)
        self.inputField2.insert( 0, "c, cpp, h" )
        self.inputField2.pack({"anchor": "w", "padx":10})

        self.convertButton = Button(self, text="開始轉換", command=self.encode_convert)
        self.convertButton.pack({"anchor": "w", "padx":10, "pady":10})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()


