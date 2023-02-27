from imports import *

print(cv2.__version__)

class CameraApp:
    def __init__(self, vs, output_path):
        self.videostream = vs
        self.output_path = output_path
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tk.Tk()
        self.panel = tk.Label(self.root)
        self.panel.pack(side="top", padx=10, pady=10)

        btn = tk.Button(self.root, text="Snapshot!", command=self.take_screenshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        btn2 = tk.Button(self.root, text="Quit", command=self.on_close)
        btn2.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.name = tk.StringVar()
        self.name.set("")
        self.nameEntry = tk.Entry(self.root, textvariable=self.name)
        self.nameEntry.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

        self.root.wm_title("Getting screenshot data")
        self.root.mainloop()

    def video_loop(self):
        try:
            while not self.stopEvent.is_set():
                ret, self.frame = self.videostream.read()
                if ret:
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    image = PIL.Image.fromarray(self.frame)
                    image = PIL.ImageTk.PhotoImage(image)

                    self.panel.configure(image=image)
                    self.panel.image = image

                    self.root.update()
                else:
                    break
        except Exception as e:
            print(e)

    def take_screenshot(self):
        path = self.create_folder_for_person()
        name = self.name.get()
        now = datetime.datetime.now()
        filename = "{}_{}.png".format(name, now.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.join(path, filename)
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))


    def create_folder_for_person(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        name = self.name.get()
        path = os.path.join(self.output_path, name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path


    def on_close(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.videostream.release()
        self.root.quit()

if __name__ == '__main__':
    vs = cv2.VideoCapture(0)
    p = CameraApp(vs, "screenshots")
    vs.release()