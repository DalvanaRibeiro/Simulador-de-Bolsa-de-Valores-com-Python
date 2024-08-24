'''

Descrição: Este projeto oferece uma plataforma onde os usuários podem experimentar a compra e venda de ações fictícias, baseando suas decisões em dados reais do mercado de ações. Ideal para entusiastas do mercado financeiro e desenvolvedores interessados em simulações financeiras, este simulador permite uma experiência prática e educativa.

'''

import tkinter as tk  # Biblioteca para criar a interface gráfica
from tkinter import messagebox  # Para exibir mensagens na interface
import matplotlib.pyplot as plt  # Biblioteca para gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integração de gráficos com Tkinter
import random  # Para gerar valores fictícios de ações
import threading  # Para atualizar os gráficos em tempo real
import time  # Para simular a passagem do tempo

class StockSimulator:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Simulador de Bolsa de Valores")
        self.root.geometry("800x600")

        # Inicialização das variáveis
        self.cash = 10000  # Dinheiro disponível
        self.portfolio = {}  # Portfólio de ações
        self.stock_price = 100  # Preço inicial da ação

        # Interface de usuário
        self.cash_label = tk.Label(root, text=f"Dinheiro: ${self.cash}")
        self.cash_label.pack()

        self.stock_label = tk.Label(root, text=f"Preço da Ação: ${self.stock_price}")
        self.stock_label.pack()

        self.buy_button = tk.Button(root, text="Comprar Ação", command=self.buy_stock)
        self.buy_button.pack()

        self.sell_button = tk.Button(root, text="Vender Ação", command=self.sell_stock)
        self.sell_button.pack()

        # Gráfico de desempenho das ações
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Desempenho das Ações")
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("Preço")
        self.line, = self.ax.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.time = 0  # Tempo inicial para o gráfico
        self.prices = []  # Lista de preços das ações

        # Iniciar a atualização dos gráficos em tempo real
        self.update_chart()

    def buy_stock(self):
        # Função para comprar ações
        if self.cash >= self.stock_price:
            self.cash -= self.stock_price
            self.portfolio['Ação'] = self.portfolio.get('Ação', 0) + 1
            self.cash_label.config(text=f"Dinheiro: ${self.cash}")
            messagebox.showinfo("Compra", "Você comprou uma ação!")
        else:
            messagebox.showerror("Erro", "Dinheiro insuficiente para comprar a ação.")

    def sell_stock(self):
        # Função para vender ações
        if self.portfolio.get('Ação', 0) > 0:
            self.portfolio['Ação'] -= 1
            self.cash += self.stock_price
            self.cash_label.config(text=f"Dinheiro: ${self.cash}")
            messagebox.showinfo("Venda", "Você vendeu uma ação!")
        else:
            messagebox.showerror("Erro", "Você não possui ações para vender.")

    def update_chart(self):
        # Função para atualizar o gráfico em tempo real
        def update():
            while True:
                time.sleep(1)  # Espera 1 segundo entre as atualizações
                self.time += 1
                self.stock_price += random.randint(-10, 10)  # Atualiza o preço da ação aleatoriamente
                self.stock_label.config(text=f"Preço da Ação: ${self.stock_price}")
                self.prices.append(self.stock_price)

                # Atualiza o gráfico
                self.line.set_data(range(len(self.prices)), self.prices)
                self.ax.set_xlim(0, len(self.prices))
                self.ax.set_ylim(min(self.prices) - 10, max(self.prices) + 10)
                self.canvas.draw()

        threading.Thread(target=update).start()  # Cria uma nova thread para atualizar o gráfico em segundo plano

# Configuração e inicialização da interface gráfica
root = tk.Tk()
app = StockSimulator(root)
root.mainloop()
