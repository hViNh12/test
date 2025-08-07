# Đây là phiên bản Kivy được viết lại từ mã Tkinter của bạn để có thể build APK trên Android
# Lưu ý: Cần chỉnh sửa thêm UI/UX nếu muốn hoàn chỉnh

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime
from gtts import gTTS
import pandas as pd
import os
import threading
from kivy.core.audio import SoundLoader

RESULT_FILE = "ketqua.xlsx"

class CarBox(BoxLayout):
    def __init__(self, car_name, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=5, **kwargs)
        self.car_name = car_name
        self.score = 100

        self.name_input = TextInput(hint_text="Tên thí sinh")
        self.result_label = Label(text="Điểm: 100", bold=True)

        self.add_widget(Label(text=f"Xe {car_name}", bold=True))
        self.add_widget(self.name_input)

        self.add_widget(self._create_button("🚦 Bắt đầu thi", self.bat_dau))
        self.add_widget(self._create_button("❌ Chạm vạch (-5đ)", self.cham_vach))
        self.add_widget(self._create_button("🦶 Chống chân (-5đ)", self.chong_chan))
        self.add_widget(self._create_button("⚠ Sai quy trình (Rớt)", self.sai_quy_trinh))
        self.add_widget(self._create_button("✅ Hoàn thành bài thi", self.hoan_thanh))
        self.add_widget(self._create_button("📊 Kết quả", self.ket_qua))
        self.add_widget(self._create_button("🔁 Reset", self.reset))

        self.add_widget(self.result_label)

    def _create_button(self, text, func):
        btn = Button(text=text, size_hint_y=None, height=40)
        btn.bind(on_release=lambda x: func())
        return btn

    def speak(self, text):
        def play():
            try:
                tts = gTTS(text=text, lang='vi')
                filename = f"temp_{threading.get_ident()}.mp3"
                tts.save(filename)
                sound = SoundLoader.load(filename)
                if sound:
                    sound.play()
                    threading.Timer(5, lambda: os.remove(filename) if os.path.exists(filename) else None).start()
            except Exception as e:
                self.show_popup("Lỗi", f"Không thể đọc: {e}")

        threading.Thread(target=play, daemon=True).start()

    def bat_dau(self):
        self.speak(f"Xe {self.car_name} bắt đầu thi")

    def cham_vach(self):
        if self.score > 0:
            self.score -= 5
            self.update_score()
            self.speak(f"Xe {self.car_name}, chạm vạch, trừ 5 điểm")

    def chong_chan(self):
        if self.score > 0:
            self.score -= 5
            self.update_score()
            self.speak(f"Xe {self.car_name}, chống chân, trừ 5 điểm")

    def sai_quy_trinh(self):
        self.score = 0
        self.update_score()
        self.speak(f"Xe {self.car_name}, bạn đã đi sai quy trình, rớt")

    def hoan_thanh(self):
        self.speak(f"Xe {self.car_name}, hoàn thành bài thi")

    def ket_qua(self):
        ketqua = "Đậu" if self.score >= 80 else "Rớt"
        text = f"Điểm: {self.score} - {ketqua}"
        self.result_label.text = text
        self.speak(f"Xe {self.car_name}, {self.score} điểm, {ketqua}")
        self.save_result()

    def reset(self):
        self.score = 100
        self.update_score()

    def update_score(self):
        ketqua = "Đậu" if self.score >= 80 else "Rớt"
        self.result_label.text = f"Điểm: {self.score}"

    def save_result(self):
        name = self.name_input.text.strip() or "Thí sinh"
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ketqua = "Đậu" if self.score >= 80 else "Rớt"

        try:
            old_df = pd.read_excel(RESULT_FILE)
        except:
            old_df = pd.DataFrame(columns=["Tên thí sinh", "Điểm", "Kết quả", "Thời gian"])

        new_row = pd.DataFrame([{
            "Tên thí sinh": name,
            "Điểm": self.score,
            "Kết quả": ketqua,
            "Thời gian": time_now
        }])

        new_df = pd.concat([old_df, new_row], ignore_index=True)
        new_df.to_excel(RESULT_FILE, index=False)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class MainApp(App):
    def build(self):
        self.init_excel()
        layout = GridLayout(cols=4, spacing=10, padding=10)
        car_list = ["4", "7", "8", "9", "10", "11", "12", "T"]
        for car in car_list:
            layout.add_widget(CarBox(car))
        return layout

    def init_excel(self):
        if not os.path.exists(RESULT_FILE):
            df = pd.DataFrame(columns=["Tên thí sinh", "Điểm", "Kết quả", "Thời gian"])
            df.to_excel(RESULT_FILE, index=False)

if __name__ == '__main__':
    MainApp().run()
