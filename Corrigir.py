from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.clock import Clock
from os import system

nota = 0
erradas = []
gabarito_aluno = []
gab_ofc = None

class Notas(Label):
        
    def __init__(self, **kwargs):
        global nota
        global erradas
        super(Notas, self).__init__(**kwargs)
        self.text = 'Nota = {}'.format(nota)

    def update(self, *args):
        global nota
        global erradas
        self.text = 'Nota = {}'.format(nota)

class Erradas(Label):
        
    def __init__(self, **kwargs):
        global nota
        global erradas
        super(Erradas, self).__init__(**kwargs)
        qst = ''
        for item in erradas:
            qst += str(item)
            qst += ', '
        qst = qst[:-2]
        self.text = 'Erradas: '+ qst

    def update(self, *args):
        global nota
        global erradas
        qst = ''
        for item in erradas:
            qst += str(item)
            qst += ', '
        qst = qst[:-2]
        self.text = 'Erradas: '+ qst

class Header(Screen):

    
    def __init__(self,**kwargs):
        global nota
        global erradas
        super(Header, self).__init__(**kwargs)
        #Head
        self.body = BoxLayout(orientation = 'vertical', padding = [10,15,10,15], spacing = 5)
        self.body.add_widget(Label(text='Confira o Gabarito', pos_hint={'center': 1}, font_size = 35))
        self.body.add_widget(Label(text = ' '))
        self.head = GridLayout(cols = 2,spacing = 5)
        self.head.add_widget(Label(text='Ano da Prova', pos_hint={'right':1, 'top': 1}, size_hint=(1, .5), font_size=18))
        self.ano = TextInput(text = '2010', multiline=False,pos_hint={'right':1, 'top': 1}, size_hint=(1, .5), font_size = 29)
        self.ano.bind(on_text_validate = self.enter)
        self.head.add_widget(self.ano)
        self.head.add_widget(Label(text='Colégio',pos_hint={'right':1, 'top': 1}, size_hint=(1, .5), font_size=18))
        self.colegio = TextInput(text = 'cmbh', multiline=False,pos_hint={'right':1, 'top': 1}, size_hint=(1, .5), font_size = 29)
        self.head.add_widget(self.colegio)
        but = Button(text = 'Enviar', size_hint=(1,.4), pos_hint = {'center':1})
        but.bind(on_press=(self.montar))
        self.body.add_widget(self.head)
        self.notas = Notas()
        Clock.schedule_interval(self.notas.update,0.5)
        self.body.add_widget(self.notas)
        self.erradas = Erradas()
        Clock.schedule_interval(self.erradas.update,0.5)
        self.body.add_widget(self.erradas)
        self.body.add_widget(but)
        self.add_widget(self.body)

    def enter(self, obj):

        self.colegio.focus = True
        

    def montar(self, obj):
        global gab_ofc
        global sm
        
        try:
                gab_ofc = open('{}.txt'.format(self.ano.text+'_'+self.colegio.text.upper()))
                sm.switch_to(sm.screen_2)
                loop = False
        except:
                self.notas.text = 'Gabarito indisponível'
        

class Aluno(Screen):
    
    def __init__(self,**kwargs):
        global nota
        global erradas
        global gabarito_aluno
        super(Aluno, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation = 'vertical', spacing = 15, padding = 10)
        self.main_layout.add_widget(Label(text = 'Insira o Gabarito do Aluno', size_hint = (1,.1), pos_hint = {'top':1}, font_size = 20))
        self.gabarit = GridLayout(cols = 4, spacing = 5, size_hint=(1,.6))
        for i in range (0,20):
            gabarito_aluno.append(TextInput(multiline = False, font_size = 15))
            gabarito_aluno[i].bind(on_text_validate = self.enter)
            if i==0:
                gabarito_aluno[i].focus = True
            self.gabarit.add_widget(Label(text = 'Questão {}:'.format(i+1)))
            self.gabarit.add_widget(gabarito_aluno[i])
            #Clock.schedule_interval(self.erradas.update,0.5)
        self.main_layout.add_widget(self.gabarit)
        self.area_but = BoxLayout(orientation = 'vertical', size_hint = (1,.1))
        self.area_but.add_widget(Label(text=' ', size_hint = (1,.2)))
        buton = Button(text = 'Conferir', size_hint = (1,.6))
        buton.bind(on_press = self.conferir)
        self.area_but.add_widget(buton)
        self.area_but.add_widget(Label(text=' ', size_hint = (1,.2)))
        self.main_layout.add_widget(self.area_but)
        self.add_widget(self.main_layout)

    def enter(self, obj):
        global gabarito_aluno

        pos = gabarito_aluno.index(obj)

        if pos == 19:
            pass
        else:
            gabarito_aluno[pos+1].focus = True

    def conferir (self, obj):
        global nota
        global erradas
        global gab_ofc
        global gabarito_aluno
        global sm

        gab = []
        for line in gab_ofc:
            gab.append(line.split()[0][-1])
        gab_ofc.close()
            
        for i in range(0,20):
            if gab[i] == gabarito_aluno[i].text.lower():
                nota +=1
            else:
                erradas.append(i+1)
        gabarito_aluno = []

        sm.switch_to(sm.screen_1)

sm = ScreenManager(transition = FadeTransition())
sm.screen_1 = (Header(name='main'))
sm.screen_2 = Aluno(name='aluno')
sm.add_widget(sm.screen_1)
sm.add_widget(sm.screen_2)
        
            
class Gabarito(App):

    
    def build(self):
        global nota
        global erradas
        page = sm
        return page


if __name__ == '__main__':
    a = Gabarito()
    a.run()
