import tkinter as tk
import random
import string
import requests
import click
import qrcode
from PIL import Image, ImageTk
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.deviceColor = tk.Label(self, text="Device Register", font = (16))
        self.deviceColor.pack(pady=10)
        
        self.deviceColor = tk.Label(self, text="Device Color:")
        self.deviceColor.pack(pady=10)
        
        self.listBox = tk.Listbox(self, width=20, height=3, font = (14))
        self.listBox.insert(1, "Black")
        self.listBox.insert(2, "White")
        self.listBox.pack(pady=10)
        
        self.macAdres = tk.Label(self, text="Device Mac Adres:")
        self.macAdres.pack()
        self.macEntry = tk.Entry(self, bd =5, bg="white", fg="black", font = (14))
        self.macEntry.pack(pady=10)
        
        self.b = tk.Button(self, text="New Device", foreground="white", width=40, height=2, command=lambda: [self.get_random_alphaNumeric_string()])
        self.b.pack(side="bottom", padx=20, pady=10)
        

    def get_random_alphaNumeric_string(self):
        self.lettersAndDigits = string.ascii_letters + string.digits

        self.Code = "Py6u7vW1Po94AzQ"
        self.random1 = ''.join((random.choice(self.lettersAndDigits) for i in range(10)))
        self.random2 = ''.join((random.choice(self.lettersAndDigits) for i in range(10)))

        self.token1 = ''.join((random.choice(self.lettersAndDigits) for i in range(15)))
        self.token2 = ''.join((random.choice(self.lettersAndDigits) for i in range(15)))
        self.token3 = ''.join((random.choice(self.lettersAndDigits) for i in range(15)))

        # get true token
        self.trueToken = self.token1+self.token2+self.token3
        
        # get fake token
        self.fakeToken = self.Code + self.token1 + self.random1 + self.token2 + self.random2 + self.token3
    
        # get device mac address
        self.mac = self.macEntry.get()
        
        # get device color
        self.value = self.listBox.curselection()
        self.color = self.listBox.get(self.value)
    
        # register a device
        if self.color != "" and self.mac !="":
            self.postRequest(self.trueToken, self.fakeToken, self.mac, self.color)
            #self.generateQrCode(self.trueToken, self.fakeToken)
        
        
    def postRequest(self, trueToken, fakeToken, mac, color):
        newHeaders = {'Content-type': 'application/json', 'User-agent': 'xx'}

        body={"token": trueToken, "mac": mac, "color": color}

        response = requests.post('http://55.55.55.55/qrcode/newdevice.php',
                                json=body,
                                headers=newHeaders)

        response_Json = response.json()

        if response_Json['message']=="1":
            self.generateQrCode(trueToken, fakeToken)
        else:
            print("Cihaz eklenirken hata oldu.")
        
        
        
    def generateQrCode(self, trueToken, fakeToken):
        self.face = Image.open('icon.png')
        self.qr_big = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=2
        )

        self.qr_big.add_data(fakeToken)
        self.qr_big.make()
        self.img_qr_big = self.qr_big.make_image(fill_color="#0f3891", back_color="#e8e8e8").convert('RGB')
        self.pos = ((self.img_qr_big.size[0] - self.face.size[0]) // 2, (self.img_qr_big.size[1] - self.face.size[1]) // 2)
        self.img_qr_big.paste(self.face, self.pos)
        self.img_qr_big.save(trueToken+'.png')
        
        self.writeToken(trueToken)
        
        
    def writeToken(self, token):
        self.labelframe = tk.LabelFrame(root, text="New Device Added", width=800, height=50)
        self.labelframe.pack()
        
        self.text = tk.Text(self.labelframe, foreground="white", width=60, height=1, font = (14))
        self.text.insert(tk.END, token)
        self.text.tag_configure("center", justify='center')
        self.text.tag_add("center", 1.0, "end")
        self.text.pack(pady=10)
        
        self.image = ImageTk.PhotoImage(Image.open(token+'.png'))
        self.panel = tk.Label(self.labelframe, image = self.image)
        self.panel.pack(fill = "both", expand = "yes", pady=10)
        
        self.b = tk.Button(self.labelframe, text="OK", foreground="white", command=lambda: [self.text.pack_forget(), self.panel.pack_forget(), self.b.pack_forget(), self.labelframe.pack_forget()])
        self.b.pack(side="right", padx=20, pady=10)

        

root = tk.Tk()
img = tk.PhotoImage(file='icon.png')
root.call('wm', 'iconphoto', root._w, img)
app = Application(master=root)
app.master.title("New Device")
app.master.minsize(1000, 1000)
app.mainloop()
