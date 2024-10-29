from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout

class Rule:
    def __init__(self, antecedent, consequent, cf):
        self.antecedent = antecedent
        self.consequent = consequent
        self.cf = cf

    def get_antecedent(self):
        return self.antecedent

    def get_consequent(self):
        return self.consequent

    def get_cf(self):
        return self.cf

class ForwardChaining:
    @staticmethod
    def do_forward_chaining(rules, user_facts):
        inferred_facts = {}
        for rule in rules:
            antecedent = rule.get_antecedent()
            cf_pakar = rule.get_cf()

            if all(symptom in user_facts for symptom in antecedent):
                cf_user = min(user_facts[symptom] for symptom in antecedent)
                cf_result = cf_user * cf_pakar

                if rule.get_consequent() in inferred_facts:
                    inferred_facts[rule.get_consequent()] = (
                        inferred_facts[rule.get_consequent()] + cf_result - 
                        (inferred_facts[rule.get_consequent()] * cf_result)
                    )
                else:
                    inferred_facts[rule.get_consequent()] = cf_result
        return inferred_facts

class MainMenu(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        float_layout = FloatLayout()
        layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="YOUR DENTIST",
            md_bg_color='#FF77B7',
            elevation=10,
            left_action_items=[["home", lambda x: x]],
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(toolbar)

        bg = Image(
            source='img/bg.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        float_layout.add_widget(bg)

        button = MDFillRoundFlatButton(
            text='Mulai Diagnosis Gigi Mu',
            font_style='Button',
            md_bg_color="#ffc130",
            text_color="#6851a5",
            pos_hint={"center_x": 0.5, "center_y": 0.13},
            size_hint=(0.8, 0.1),
            on_release=self.go_to_diagnosis
        )
        float_layout.add_widget(button)

        layout.add_widget(float_layout)
        self.add_widget(layout)

    def go_to_diagnosis(self, instance):
        self.manager.current = 'diagnosis'

class Diagnosis(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_question_index = 1
        self.user_facts = {}
        self.rules = self.get_rules()

        self.float_layout = FloatLayout()
        self.layout = MDBoxLayout(orientation='vertical')
        self.checkbox_parent = MDBoxLayout(orientation='vertical', size_hint=(0.1, None), pos_hint={'center_x': 0.43, 'center_y': 0.25})

        self.add_toolbar()
        self.add_background()
        self.add_question()

        self.layout.add_widget(self.float_layout)
        self.add_widget(self.layout)

    def get_rules(self):
        return [
            Rule(['G01'], 'Periodontal Abscess', 0.4),
            Rule(['G02'], 'Periodontal Abscess', 0.4),
            Rule(['G03'], 'Periodontal Abscess', 0.2),
            Rule(['G01'], 'Periapical Abscess', 0.4),
            Rule(['G04'], 'Periapical Abscess', 0.6),
            Rule(['G05'], 'Periapical Abscess', 0.4),
            Rule(['G06'], 'Periapical Abscess', 0.4),
            Rule(['G07'], 'Dental Abrasion', 0.6),
            Rule(['G08'], 'Dental Abrasion', 0.4),
            Rule(['G09'], 'Bruxism', 0.2),
            Rule(['G10'], 'Bruxism', 0.6),
            Rule(['G05'], 'Gingivitis (Gum Inflammation)', 0.8),
            Rule(['G14'], 'Gingivitis (Gum Inflammation)', 0.2),
            Rule(['G15'], 'Gingivitis (Gum Inflammation)', 0.6),
            Rule(['G03'], 'Caries (Cavities)', 0.6),
            Rule(['G07'], 'Caries (Cavities)', 0.2),
            Rule(['G09'], 'Caries (Cavities)', 0.2),
            Rule(['G10'], 'Caries (Cavities)', 0.2),
            Rule(['G13'], 'Caries (Cavities)', 0.8),
            Rule(['G16'], 'Caries (Cavities)', 0.4),
            Rule(['G19'], 'Caries (Cavities)', 0.5),
            Rule(['G09'], 'Tooth Fracture', 0.8),
            Rule(['G10'], 'Tooth Fracture', 0.4),
            Rule(['G15'], 'Tooth Fracture', 0.6),
            Rule(['G17'], 'Tooth Fracture', 0.4),
            Rule(['G18'], 'Tooth Fracture', 0.6),
            Rule(['G19'], 'Tooth Fracture', 0.4),
            Rule(['G02'], 'Periodontitis', 0.8),
            Rule(['G03'], 'Periodontitis', 0.2),
            Rule(['G07'], 'Periodontitis', 0.6),
            Rule(['G14'], 'Periodontitis', 0.6),
            Rule(['G16'], 'Periodontitis', 0.4),
            Rule(['G19'], 'Periodontitis', 0.8),
            Rule(['G20'], 'Periodontitis', 0.4)
        ]

    def get_question(self):
        return {
            'G01': 'Sulit untuk mengunyah',
            'G02': 'Gusi bengkak atau meradang',
            'G03': 'Gigi goyang',
            'G04': 'Rahang menjadi bengkak',
            'G05': 'Pembengkakan kelenjar getah bening di sekitar rahang atau leher',
            'G06': 'Demam',
            'G07': 'Bau mulut',
            'G08': 'Nyeri atau sakit di sekitar gusi',
            'G09': 'Gigi terasa ngilu dan sensitif',
            'G10': 'Bentuk gigi tampak terkikis',
            'G11': 'Insomnia atau merasa gelisah',
            'G12': 'Sakit kepala',
            'G13': 'Rongga',
            'G14': 'Gusi mudah berdarah',
            'G15': 'Bentuk gusi agak membulat',
            'G16': 'Adanya plak pada gigi',
            'G17': 'Gigi tampak terkikis',
            'G18': 'Rasa sakit yang dapat muncul dan hilang secara tiba-tiba',
            'G19': 'Sakit gigi saat mengunyah/menggigit',
            'G20': 'Gusi terasa sakit atau nyeri saat ditekan'
        }

    def add_question(self):
        questions = self.get_question()
        question_key = list(questions.keys())
        question_label = MDLabel(
            text=f'{self.current_question_index}: {questions[question_key[self.current_question_index - 1]]}',
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            adaptive_height=True,
        )
        self.float_layout.add_widget(question_label)
        self.add_checkbox()

        button = MDRectangleFlatIconButton(
            text='Lanjut',
            icon='arrow-right-thin',
            md_bg_color="#ffc130",
            text_color="#6851a5",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            size_hint=(0.1, 0.1),
            on_release=self.next_question
        )
        self.float_layout.add_widget(button)

    def add_checkbox(self):
        option_dict = self.option()
        self.checkbox_parent.clear_widgets()

        for i, (label_text, value) in enumerate(option_dict.items()):
            checkbox = MDCheckbox(group='group', size_hint=(None, 1), size=(40, 40))
            checkbox.bind(active=lambda chk, val, index=i: self.on_checkbox_active(index, val))
            checkbox_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
            checkbox_layout.add_widget(checkbox)
            label = MDLabel(text=label_text, halign='left', valign='middle', size_hint=(None, 1), width=300)
            checkbox_layout.add_widget(label)
            self.checkbox_parent.add_widget(checkbox_layout)

        self.float_layout.add_widget(self.checkbox_parent)

    def option(self):
        return {
            "Pastinya iya": 1.0,
            "Hampir pasti iya": 0.8,
            "Kemungkinan besar iya": 0.6,
            "Mungkin iya": 0.4,
            "Tidak tahu": 0.0
        }

    def on_checkbox_active(self, index, value):
        if value:
            question_key = list(self.get_question().keys())[self.current_question_index - 1]
            self.user_facts[question_key] = list(self.option().values())[index]

    def next_question(self, instance):
        if self.current_question_index < len(self.get_question()):
            self.current_question_index += 1
            self.float_layout.clear_widgets()
            self.add_background()
            self.add_question()
        else:
            self.run_forward_chaining()

    def run_forward_chaining(self):
        inferred_facts = ForwardChaining.do_forward_chaining(self.rules, self.user_facts)
        self.reset()
        self.manager.get_screen('hasil').display_result(inferred_facts)
        self.manager.current = 'hasil'

    def add_background(self):
        bg = Image(source='img/bg2.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.float_layout.add_widget(bg)

    def add_toolbar(self):
        toolbar = MDTopAppBar(
            title="YOUR DENTIST",
            md_bg_color='#FF77B7',
            elevation=10,
            left_action_items=[["home", lambda x: self.go_home(x)]],
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(toolbar)
    
    def reset(self):
        # Resetting the diagnosis screen
        self.current_question_index = 1
        self.user_facts.clear()
        self.float_layout.clear_widgets()  # Clear previous widgets
        self.add_background()  # Optionally re-add background
        self.add_question()  # Re-add question to start over

    def go_home(self, instance):
        self.manager.current = 'main'
        self.reset()

class HasilDiagnosis(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layouts
        self.float_layout = FloatLayout()
        self.float_layout1 = FloatLayout()
        self.layout = MDBoxLayout(orientation='vertical')
        
        # Parent layout for text with padding and center positioning
        self.parent_text = MDBoxLayout(orientation='vertical', padding=(0, 0, 0, 220), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.text_layout = MDBoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Main Cards
        self.card = MDCard(
            orientation='vertical',
            size_hint=(0.5, 0.15),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            md_bg_color=(1, 0.756, 0.188, 1)  # Converted #ffc130 to RGBA
        )

        self.card1 = MDCard(
            orientation='vertical',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(1, 0.756, 0.188, 1)  # Converted #ffc130 to RGBA
        )

        self.add_toolbar()
        
        # Label for highest CF result

        self.highest_cf_label = MDLabel(
            text='CF Tertinggi: -',
            halign='center',
            valign='center',  # Center vertically
            theme_text_color='Primary',
            text_color=(0.41, 0.32, 0.65, 1),  # Converted #6851a5 to RGBA
            font_style='H6'
        )

        center_layout_high = BoxLayout(orientation='vertical', padding=0, spacing=0)
        center_layout_high.add_widget(self.highest_cf_label)
        self.card.add_widget(center_layout_high)

        # Result Label
        self.result_label = MDLabel(
            text='',
            halign='center',
            valign='center',  # Center vertically
            theme_text_color='Secondary',
            text_color=(0.41, 0.32, 0.65, 1),  # Converted #6851a5 to RGBA
            font_style='H6'
        )

        center_layout_result = BoxLayout(orientation='vertical', padding=0, spacing=0)
        center_layout_result.add_widget(self.result_label)
        self.card1.add_widget(center_layout_result)
        
        # Ensure parent_text is only added once
        self.float_layout1.add_widget(self.parent_text)

        self.add_background()

        # Add widgets to layouts
        self.float_layout.add_widget(self.card)
        self.float_layout.add_widget(self.card1)
        self.float_layout.add_widget(self.float_layout1)
        self.layout.add_widget(self.float_layout)
        self.add_widget(self.layout)

    def add_toolbar(self):
        toolbar = MDTopAppBar(
            title="YOUR DENTIST",
            md_bg_color='#FF77B7',
            elevation=0,
            left_action_items=[["home", lambda x: self.go_home(x)]],
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(toolbar)
        

    def go_home(self, instance):
        self.manager.current = 'main'

    def add_background(self):
        bg = Image(source='img/b31.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.float_layout.add_widget(bg)

    def display_result(self, inferred_facts):
        if inferred_facts:
            # Temukan hasil dengan CF tertinggi
            highest_cf_disease = max(inferred_facts, key=inferred_facts.get)
            highest_cf_value = inferred_facts[highest_cf_disease]
            
            # Tampilkan hasil diagnosis
            result_text = "\n".join([f"{disease} ({cf*100:0.2f}%)" for disease, cf in inferred_facts.items() if cf > 0])

            kali = len(inferred_facts)
            self.card1.size_hint = (0.5, 0.0625*kali)
            
            # Cek jika CF tertinggi sama dengan 0
            if highest_cf_value > 0:
                self.highest_cf_label.text = f'Kemungkinan besar Anda menderita:\n {highest_cf_disease} ({highest_cf_value*100:0.2f}%)'
                self.result_label.text = result_text
            else:
                result_text = "Tidak ada penyakit yang teridentifikasi"
                self.highest_cf_label.text = result_text
                self.card1.size_hint = (0, 0)
                self.card.pos_hint={'center_x': 0.5, 'center_y': 0.5}
                self.result_label.text = ''

            if len(inferred_facts) == 0:
                result_text = "Tidak ada penyakit yang teridentifikasi"
                self.highest_cf_label.text = result_text
                self.card1.size_hint = (0, 0)
                self.card.pos_hint={'center_x': 0.5, 'center_y': 0.5}
                self.result_label.text = ''
        else:
            result_text = "Tidak ada penyakit yang teridentifikasi"
            self.highest_cf_label.text = result_text
            self.card1.size_hint = (0, 0)
            self.card.pos_hint={'center_x': 0.5, 'center_y': 0.5}
            self.result_label.text = ''
        
        print(len(inferred_facts))

class UTS(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainMenu(name='main'))
        screen_manager.add_widget(Diagnosis(name='diagnosis'))
        screen_manager.add_widget(HasilDiagnosis(name='hasil'))
        return screen_manager

if __name__ == '__main__':
    UTS().run()