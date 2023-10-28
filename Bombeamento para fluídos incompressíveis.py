import PySimpleGUI as sg
import math

def area_secao(d):
    return (3.14 * (d**2)) / 4

def calculo_velocidade(q, a):
    return q / a

def bernoulli(P, p, v1, v2, h1, h2):
    gravidade = 9.81
    return P + (p * (v2**2 - v1**2) / 2) + (p * gravidade * (h2 - h1))

def viscosidade(u, l, q, d1, d2):
    pi = 3.14
    d = (d1 + d2) / 2
    return (128 * u * l * q) / (pi * d**4)

def potencia(q, p1, p2, n):
    return (q * (p2 - p1)) / (n * 0.01)
    

class Interface:
    def __init__(self):
        # Layout
        sg.theme('BluePurple')

        layout = [
            [sg.Text('Vazão (m³/s)', size=(20,0)), sg.Input(size=(15,0), key='vazao')],
            [sg.Text('Comprimento (m)', size=(20,0)), sg.Input(size=(15,0), key='comprimento')],
            [sg.Text('Diámetro Entrada (m)', size=(20,0)), sg.Input(size=(15,0), key='diametroEntrada')],
            [sg.Text('Diámetro Saída (m)', size=(20,0)), sg.Input(size=(15,0), key='diametroSaida')],
            [sg.Text('Altura Entrada (m)', size=(20,0)), sg.Input(size=(15,0), key='alturaEntrada')],
            [sg.Text('Altura Saída (m)', size=(20,0)), sg.Input(size=(15,0), key='alturaSaida')],
            [sg.Text('Pressão (Pa)', size=(20,0)), sg.Input(size=(15,0), key='pressão')],
            [sg.Text('A pressão será de entrado ou de saida?')],
            [sg.Radio('Entrada', 'pressoes', key='pDeEntrada'), sg.Radio('Saida', 'pressoes', key='pDeSaida')],
            [sg.Text('Selecione o tipo de fluido a ser medido:')],
            [sg.Radio('Água', 'fluidos', key='agua'), sg.Radio('Petróleo', 'fluidos', key='petroleo'), sg.Radio('Gasolina', 'fluidos',key='gasolina'), sg.Radio('Óleo de Arroz', 'fluidos',key='oleo')],
            [sg.Text('Coeficiente de eficiencia do sistema (%):',size=(30,0)), sg.Input(size=(10,0), key="eficiencia")],
            [sg.Button('Calcular')],
            [sg.Output(size=(40, 5), key='output')]
        ]
        # Janela
        self.janela = sg.Window("Dados do Usuario", layout=layout)

    def Iniciar(self):
        while True:
            self.button, self.values = self.janela.read()
            
            if self.button is None:
                break
            
            vazao = float(self.values['vazao'])
            comprimento = float(self.values['comprimento'])
            diametroEntrada = float(self.values['diametroEntrada'])
            diametroSaida = float(self.values['diametroSaida'])
            alturaEntrada = float(self.values['alturaEntrada'])
            alturaSaida = float(self.values['alturaSaida'])
            pressao = float(self.values['pressão'])
            pressao_entrada = self.values['pDeEntrada']
            pressao_saida = self.values['pDeSaida']
            fluido_agua = self.values['agua']
            fluido_petroleo = self.values['petroleo']
            fluido_gasolina = self.values['gasolina']
            fluido_oleoArroz = self.values['oleo']
            eficiencia = float(self.values['eficiencia'])

            a1 = area_secao(diametroEntrada)
            a2 = area_secao(diametroSaida)
            v1 = calculo_velocidade(vazao, a1)
            v2 = calculo_velocidade(vazao, a2)

            if fluido_agua == True:
                densidade = 997
                viscosidade_fluido = 0.001
                potencia_vis = viscosidade(viscosidade_fluido, comprimento, vazao, diametroEntrada, diametroSaida)
            if fluido_petroleo == True:
                densidade = 826.5
                viscosidade_fluido = 0.8
                potencia_vis = viscosidade(viscosidade_fluido, comprimento, vazao, diametroEntrada, diametroSaida)
            if fluido_gasolina == True:
                densidade = 715
                viscosidade_fluido = 1.41
                potencia_vis = viscosidade(viscosidade_fluido, comprimento, vazao, diametroEntrada, diametroSaida)
            if fluido_oleoArroz == True:
                densidade = 920
                viscosidade_fluido = 0.0738
                potencia_vis = viscosidade(viscosidade_fluido, comprimento, vazao, diametroEntrada, diametroSaida)

            
            if pressao_entrada == True:
                P1 = pressao
                P2 = bernoulli(P1, densidade, v1, v2, alturaEntrada, alturaSaida)
            if pressao_saida == True:
                P2 = pressao
                P1 = bernoulli(P2, densidade, v1, v2, alturaEntrada, alturaSaida)
            



            pot = potencia(vazao, P1, P2, eficiencia)
            potencia_total = potencia_vis + pot
            potencia_formatada = f"{potencia_total:.2f}"
            
            print(f'Potência Total: {potencia_formatada} Watts')

          

tela = Interface()
tela.Iniciar()
