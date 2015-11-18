
'''Warning: I wrote this code when I was newbie, so the way of programming might not be the best'''

import calendar
import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import threading


class Calendar_Part(BoxLayout):
    pass

# class for dates.kv file
class Dates(GridLayout):
    now = datetime.datetime.now()
    btn_1 = ObjectProperty(None)
    btn_2 = ObjectProperty(None)
    btn_3 = ObjectProperty(None)
    btn_4 = ObjectProperty(None)
    btn_5 = ObjectProperty(None)
    btn_6 = ObjectProperty(None)
    btn_7 = ObjectProperty(None)
    btn_8 = ObjectProperty(None)
    btn_9 = ObjectProperty(None)
    btn_10 = ObjectProperty(None)
    btn_11 = ObjectProperty(None)
    btn_12 = ObjectProperty(None)
    btn_13 = ObjectProperty(None)
    btn_14 = ObjectProperty(None)
    btn_15 = ObjectProperty(None)
    btn_16 = ObjectProperty(None)
    btn_17 = ObjectProperty(None)
    btn_18 = ObjectProperty(None)
    btn_19 = ObjectProperty(None)
    btn_20 = ObjectProperty(None)
    btn_21 = ObjectProperty(None)
    btn_22 = ObjectProperty(None)
    btn_23 = ObjectProperty(None)
    btn_24 = ObjectProperty(None)
    btn_25 = ObjectProperty(None)
    btn_26 = ObjectProperty(None)
    btn_27 = ObjectProperty(None)
    btn_28 = ObjectProperty(None)
    btn_29 = ObjectProperty(None)
    btn_30 = ObjectProperty(None)
    btn_31 = ObjectProperty(None)
    btn_32 = ObjectProperty(None)
    btn_33 = ObjectProperty(None)
    btn_34 = ObjectProperty(None)
    btn_35 = ObjectProperty(None)
    btn_36 = ObjectProperty(None)
    btn_37 = ObjectProperty(None)
    btn_38 = ObjectProperty(None)
    btn_39 = ObjectProperty(None)
    btn_40 = ObjectProperty(None)
    btn_41 = ObjectProperty(None)
    btn_42 = ObjectProperty(None)
    
    
    def __init__(self,**kwargs):
        super(Dates,self).__init__(**kwargs)
        self.cols = 7
        threading.Thread(target=self.seventh_thread).start()
    
    def seventh_thread(self):
        self.btn_1 = "a"
        self.btn_2 = "b"
        self.btn_3 = "c"

# class for select.kv file
class Select(BoxLayout):
    
    month = ObjectProperty()
    y1 = ListProperty()
    y2 = ListProperty()
    year_1 = ObjectProperty(None)
    year_2 = ObjectProperty(None)
    lbl_ = ObjectProperty(None)
    btn = ObjectProperty(None)
    c  = calendar.monthcalendar(2015,5)
    
    def __init__(self,**kwargs):
        super(Select,self).__init__(**kwargs)
        self.count = 0 
        self.month = 1
        
    def get_years(self):
        if self.count == 0:
            for i in range(0,100):
                if i<10:
                    self.y1.append('0'+str(i))
                    if i == 0:
                        pass
                    else:
                        self.y2.append('0'+str(i))
                else:
                    self.y1.append(str(i))
                    self.y2.append(str(i))
        self.count = 1
        self.year_1.values = self.y1
        self.year_2.values = self.y2
        
    def on_release(self):
        self.a = int(self.year_1.text)
        self.b = int(self.year_2.text)
        self.parent.parent.ids.dates.btn_37.text = ''
        self.parent.parent.ids.dates.btn_36.text = ''
        self.final = int(str("%02d" % (self.a,))+str("%02d" % (self.b,)))
        self.survive = []
        self.c = calendar.monthcalendar(self.final,self.parent.parent.ids.months.decide)
        for i in self.c:
            for j in i:
                if j == 0:
                    self.survive.append(' ')
                else:
                    self.survive.append(j)
        try:
            self.parent.parent.ids.dates.btn_1.text = str(self.survive[0])
            self.parent.parent.ids.dates.btn_2.text = str(self.survive[1])
            self.parent.parent.ids.dates.btn_3.text = str(self.survive[2])
            self.parent.parent.ids.dates.btn_4.text = str(self.survive[3])
            self.parent.parent.ids.dates.btn_5.text = str(self.survive[4])
            self.parent.parent.ids.dates.btn_6.text = str(self.survive[5])
            self.parent.parent.ids.dates.btn_7.text = str(self.survive[6])
            self.parent.parent.ids.dates.btn_8.text = str(self.survive[7])
            self.parent.parent.ids.dates.btn_9.text = str(self.survive[8])
            self.parent.parent.ids.dates.btn_10.text = str(self.survive[9])
            self.parent.parent.ids.dates.btn_11.text = str(self.survive[10])
            self.parent.parent.ids.dates.btn_12.text = str(self.survive[11])
            self.parent.parent.ids.dates.btn_13.text = str(self.survive[12])
            self.parent.parent.ids.dates.btn_14.text = str(self.survive[13])
            self.parent.parent.ids.dates.btn_15.text = str(self.survive[14])
            self.parent.parent.ids.dates.btn_16.text = str(self.survive[15])
            self.parent.parent.ids.dates.btn_17.text = str(self.survive[16])
            self.parent.parent.ids.dates.btn_18.text = str(self.survive[17])
            self.parent.parent.ids.dates.btn_19.text = str(self.survive[18])
            self.parent.parent.ids.dates.btn_20.text = str(self.survive[19])
            self.parent.parent.ids.dates.btn_21.text = str(self.survive[20])
            self.parent.parent.ids.dates.btn_22.text = str(self.survive[21])
            self.parent.parent.ids.dates.btn_23.text = str(self.survive[22])
            self.parent.parent.ids.dates.btn_24.text = str(self.survive[23])
            self.parent.parent.ids.dates.btn_25.text = str(self.survive[24])
            self.parent.parent.ids.dates.btn_26.text = str(self.survive[25])
            self.parent.parent.ids.dates.btn_27.text = str(self.survive[26])
            self.parent.parent.ids.dates.btn_28.text = str(self.survive[27])
            self.parent.parent.ids.dates.btn_29.text = str(self.survive[28])
            self.parent.parent.ids.dates.btn_30.text = str(self.survive[29])
            self.parent.parent.ids.dates.btn_31.text = str(self.survive[30])
            self.parent.parent.ids.dates.btn_32.text = str(self.survive[31])
            self.parent.parent.ids.dates.btn_33.text = str(self.survive[32])
            self.parent.parent.ids.dates.btn_34.text = str(self.survive[33])
            self.parent.parent.ids.dates.btn_35.text = str(self.survive[34])
        except:
            pass
        try:
            self.parent.parent.ids.dates.btn_36.text = str(self.survive[35])
        except:
            pass
        try:
            self.parent.parent.ids.dates.btn_37.text = str(self.survive[36])
        except:
            pass

# ------------------------------------------------------------------------------------------------#

# class for months.kv file
class Months(BoxLayout):
    decide = ObjectProperty(None)
    btn_jan = ObjectProperty(None)
    btn_feb = ObjectProperty(None)
    btn_mar = ObjectProperty(None)
    btn_april = ObjectProperty(None)
    btn_may = ObjectProperty(None)
    btn_june = ObjectProperty(None)
    btn_july = ObjectProperty(None)
    btn_aug = ObjectProperty(None)
    btn_sept = ObjectProperty(None)
    btn_oct = ObjectProperty(None)
    btn_nov = ObjectProperty(None)
    btn_dec = ObjectProperty(None)
    
    def __init__(self,**kwargs):
        super(Months,self).__init__(**kwargs)
        self.decide = 1
        
    def on_release(self,event):
        self.previous = event.name
        if event.text == 'Jan':
            self.decide = 1
            self.parent.parent.ids.select.month = 1
        elif event.text == 'Feb':
            self.decide = 2
            self.parent.parent.ids.select.month = 2
        elif event.text == 'Mar':
            self.decide = 3
            self.parent.parent.ids.select.month = 3
        elif event.text == 'April':
            self.decide = 4
            self.parent.parent.ids.select.month = 4
        elif event.text == 'May':
            self.decide = 5
            self.parent.parent.ids.select.month = 5
        elif event.text == 'June':
            self.decide = 6
            self.parent.parent.ids.select.month = 6
        elif event.text == 'July':
            self.decide = 7
            self.parent.parent.ids.select.month = 7
        elif event.text == 'Aug':
            self.decide = 8
            self.parent.parent.ids.select.month = 8
        elif event.text == 'Sept':
            self.decide = 9
            self.parent.parent.ids.select.month = 9
        elif event.text == 'Oct':
            self.decide = 10
            self.parent.parent.ids.select.month = 10
        elif event.text == 'Nov':
            self.decide = 11
            self.parent.parent.ids.select.month = 11
        elif event.text == 'Dec':
            self.decide = 12
            self.parent.parent.ids.select.month = 12
### --------------------- EOF ------------------------------EOF---------------------------###
