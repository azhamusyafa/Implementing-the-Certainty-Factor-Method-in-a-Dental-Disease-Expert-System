from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle


# Data penyakit dan gejala
penyakit = {
    "Periodontal Abscess": ["G01", "G02", "G03"],
    "Periapical Abscess": ["G01", "G04", "G05", "G06"],
    "Dental Abrasion": ["G07", "G08"],
    "Bruxism": ["G09", "G10", "G11"],
    "Gingivitis": ["G05", "G14", "G15"],
    "Caries": ["G13", "G16", "G17"],
    "Tooth Fracture": ["G09", "G10", "G17", "G18"],
    "Periodontitis": ["G02", "G03", "G19", "G20"]
}

gejala = {
    "G01": "Difficult to chew",
    "G02": "Swelling or inflammation of the gums",
    "G03": "Teeth sway",
    "G04": "The jaw becomes swollen",
    "G05": "Swollen lymph nodes around the jaw or neck",
    "G06": "Fever",
    "G07": "Bad breath",
    "G08": "Pain or soreness around the gums",
    "G09": "Teeth feel sore and sensitive",
    "G10": "The shape of the teeth appears eroded",
    "G11": "Insomnia or feeling restless",
    "G12": "Headache",
    "G13": "Cavity",
    "G14": "Gums bleed easily",
    "G15": "The shape of the gums is slightly rounded",
    "G16": "The presence of plaque on the teeth",
    "G17": "Teeth seem to be eroded",
    "G18": "Pain that can appear and disappear suddenly",
    "G19": "Tooth pain when chewing/biting",
    "G20": "Tooth pain when chewing/biting"
}

conditions = {
    "Definitely Yes": 1,
    "Almost Certainly Yes": 0.8,
    "Most likely Yes": 0.6,
    "Maybe yes": 0.4,
    "Don't know": 0
}



def hitung_cf(cf1, cf2):
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    elif cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    else:
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (1250, 710)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        background = Image(source='bg.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
        start_button = Button(
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='1.png',  # Gambar saat normal
            background_down='2.png'  # Gambar saat ditekan
        )
        start_button.bind(on_press=self.goto_diagnosis)

        layout.add_widget(start_button)
        self.add_widget(layout)

    def goto_diagnosis(self, instance):
        self.manager.current = 'diagnosis'

class DiagnosisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_question = 0
        self.selected_gejala = {}

        self.layout = FloatLayout(size_hint=(1, 1))

        with self.layout.canvas.before:
            self.background = Rectangle(source='bg2.png', pos=self.layout.pos, size=Window.size)

        self.layout.bind(size=self.update_background, pos=self.update_background)

#        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
#        background = Image(source='bg2.png', allow_stretch=True, keep_ratio=False)
#        background.size_hint = (1, 1)
#        background.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
#        self.layout.add_widget(background)

        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content_layout.size_hint = (0.9, 0.9)  # Sesuaikan ukuran konten
        content_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.question_label = Label(
            font_size='34sp',
            font_name='Roboto-Bold.ttf',
            color=(0.494, 0.675, 0.710, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5,'center_y':0.85}
        )
        self.question_label.bind(size=self.question_label.setter('text_size'))
        self.layout.add_widget(self.question_label)

        self.options_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        content_layout.add_widget(self.options_layout)

        self.next_button = Button(
            size_hint=(0.13, 0.1),
            pos_hint={'right': 1, 'bottom': 0},
            background_normal='next.png'
        )
        self.next_button.bind(on_press=self.next_question)
        self.layout.add_widget(self.next_button)

        self.layout.add_widget(content_layout)
        self.add_widget(self.layout)

        self.update_question()

    def update_background(self, *args):
        self.background.size = Window.size
        self.background.pos = self.layout.pos

    def update_question(self):
        self.options_layout.clear_widgets()

        gejala_codes = list(gejala.keys())
        if self.current_question < len(gejala_codes):
            kode = gejala_codes[self.current_question]
            self.question_label.text = f"{kode}: {gejala[kode]}"

            for condition, value in conditions.items():
                option_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=100,
                    padding=(450, 0),
                    spacing=300
                )
                checkbox = CheckBox(
                    size_hint=(None, 1), width=40,
                    background_checkbox_normal='uc.png',
                    background_checkbox_down='c.png'
                )
                checkbox.bind(active=self.on_checkbox_active)
                label = Label(
                    text=condition,
                    size_hint=(1, 1),
                    font_name='Roboto-Bold.ttf',
                    font_size='18sp',
                    halign='left',
                    valign='middle'
                )
                label.bind(size=label.setter('text_size'))  # Agar teks rata kiri

                checkbox.gejala_kode = kode
                checkbox.cf_value = value

                option_layout.add_widget(checkbox)
                option_layout.add_widget(label)
                self.options_layout.add_widget(option_layout)
        else:
            self.show_results()

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.selected_gejala[checkbox.gejala_kode] = checkbox.cf_value

            for sibling in self.options_layout.children:
                sibling_checkbox = sibling.children[1]
                if sibling_checkbox != checkbox:
                    sibling_checkbox.active = False

    def next_question(self, instance):
        self.current_question += 1
        self.update_question()

    def show_results(self):
        hasil = {}
        for nama_penyakit, daftar_gejala in penyakit.items():
            cf_total = 0
            for gejala_code in daftar_gejala:
                if gejala_code in self.selected_gejala:
                    cf_total = hitung_cf(cf_total, self.selected_gejala[gejala_code])
            hasil[nama_penyakit] = cf_total

        hasil_terurut = sorted(hasil.items(), key=lambda x: x[1], reverse=True)
        hasil_teks = "\n".join([f"{nama}: {cf * 100:.2f}%" for nama, cf in hasil_terurut])

        popup = Popup(
            title="Hasil Diagnosa",
            content=Label(text=hasil_teks),
            size_hint=(0.8, 0.6)
        )
        popup.open()


class SistemPakar(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(DiagnosisScreen(name='diagnosis'))
        return sm


if __name__ == "__main__":
    SistemPakar().run()
