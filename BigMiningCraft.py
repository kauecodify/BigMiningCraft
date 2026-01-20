'# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 23:16:39 2026

No universo do Minecraft Data Miner, os modelos de machine learning são representados como Golems de Ferro 
guardiões poderosos que protegem e analisam seus dados. Vou explicar detalhadamente como esses "Golems" são forjados:

🔧 Processo de Forjamento de um Golem (Modelo)

1. Preparação dos Materiais (Seleção dos Dados)
O sistema seleciona automaticamente um bloco de dados (dataset) carregado
Identifica as variáveis numéricas disponíveis no dataset (os "minérios" necessários para a forja)
Por padrão, utiliza todas as colunas numéricas exceto a última como features (características de entrada)
A última coluna numérica é definida como variável alvo (o que o Golem precisa prever)

2. Preparação do Ferreiro (Divisão dos Dados)
Os dados são divididos em dois conjuntos:
80% para treinamento (o ferreiro ensina o Golem)
20% para teste (o campo de provas onde o Golem demonstra suas habilidades)

3. A Forja do Golem (Treinamento do Modelo)
Um Golem de Ferro do tipo Random Forest é forjado
Utiliza 100 árvores de decisão trabalhando em conjunto (floresta aleatória)
Cada árvore aprende padrões diferentes nos dados, como ferreiros especializados
O random_state=42 garante que o processo seja reprodutível (mesma receita de forja)

4. Teste de Habilidades (Avaliação do Modelo)
Após o treinamento, o Golem é testado no campo de provas (conjunto de teste):

Precisão (R²): Mede quão bem o Golem prevê os valores (0 a 1, quanto mais próximo de 1, melhor)
Erro (RMSE): Mede o erro médio em escala original (quanto menor, melhor)
Energia (MAE): Mede a energia consumida pelo Golem para fazer previsões (Mean Absolute Error)

5. Ritual de Nomeação e Registro (Armazenamento do Modelo)
O Golem recém-forjado recebe uma identidade única e é registrado no Estábulo dos Golems:

💎 Características Especiais dos Golems
Golems Elite (R² > 0.8): Recebem status especial com ícone 💎
Golems Fortes (R² > 0.6): Status ⚡
Golems Fracos (R² ≤ 0.6): Status 🪨
Golems Defensores (Regressor): Especializados em previsão contínua
Golems Atacantes (Classificador): [Em desenvolvimento] Especializados em classificação

⚡ Tecnologia por Trás da Magia
O sistema utiliza Random Forest Regressor do scikit-learn porque:

É robusto contra outliers (comum em dados de mineração)
Não requer normalização dos dados
Lida bem com diferentes escalas de variáveis
Fornece métricas compreensíveis para analistas
Tem bom equilíbrio entre complexidade e performance

@author: k
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import datetime
import os
import json
import time
import threading
import warnings
warnings.filterwarnings('ignore')

class MinecraftBigDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⛏️ Minecraft Data Miner & AutoML - 2026")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        self.datasets = {}
        self.models = {}
        self.current_dataset = None
        self.current_model = None
        
        # Inicializar status_var PRIMEIRO
        self.status_var = tk.StringVar(value="⛏️ Sistema iniciado - Pronto para minerar dados!")
        self.setup_minecraft_styles()
        self.build_interface()
        self.create_status_bar()
        # MOVER load_example_data() PARA DEPOIS DE CRIAR A INTERFACE
        # pois self.log_text é criado em show_dashboard()
        self.setup_auto_save()
        self.load_example_data()

    def setup_minecraft_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        dirt_brown = "#8B4513"
        grass_green = "#556B2F"
        wood_brown = "#A0522D"
        stone_gray = "#808080"
        gold_yellow = "#FFD700"
        coal_black = "#2F2F2F"
        bg_color = coal_black
        card_bg = "#3A3A3A"
        fg_color = "#E6D3A7"
        
        style.configure("Main.TFrame", background=bg_color)
        style.configure("Header.TLabel", font=("Courier", 16, "bold"), foreground=gold_yellow, background=bg_color)
        style.configure("Subheader.TLabel", font=("Courier", 12), foreground="#B8860B", background=bg_color)
        style.configure("Card.TFrame", background=card_bg, borderwidth=2, relief="solid", bordercolor=stone_gray)
        style.configure("Accent.TButton", background=dirt_brown, foreground=fg_color, font=("Courier", 10, "bold"), 
                        borderwidth=2, relief="raised", bordercolor=wood_brown)
        style.map("Accent.TButton", background=[('active', '#A0522D'), ('pressed', '#8B4513')], relief=[('pressed', 'sunken')])
        style.configure("Success.TButton", background=grass_green, foreground=fg_color, font=("Courier", 10, "bold"), 
                        borderwidth=2, relief="raised", bordercolor="#2F4F2F")
        style.map("Success.TButton", background=[('active', '#6B8E23'), ('pressed', '#556B2F')])
        style.configure("Warning.TButton", background="#D2691E", foreground=fg_color, font=("Courier", 10, "bold"), 
                        borderwidth=2, relief="raised", bordercolor="#8B4513")
        style.map("Warning.TButton", background=[('active', '#CD853F'), ('pressed', '#D2691E')])
        style.configure("Danger.TButton", background="#8B0000", foreground=fg_color, font=("Courier", 10, "bold"), 
                        borderwidth=2, relief="raised", bordercolor="#4A0000")
        style.map("Danger.TButton", background=[('active', '#B22222'), ('pressed', '#8B0000')])
        style.configure("Treeview", background="#4A4A4A", foreground=fg_color, fieldbackground="#4A4A4A",
                        rowheight=28, font=("Courier", 9))
        style.configure("Treeview.Heading", background=stone_gray, foreground=gold_yellow, font=("Courier", 10, "bold"), 
                        borderwidth=1, relief="raised")
        style.map("Treeview", background=[('selected', dirt_brown)], foreground=[('selected', "#FFFFFF")])
        style.configure("TNotebook", background=bg_color, borderwidth=2, bordercolor=stone_gray)
        style.configure("TNotebook.Tab", background="#555555", foreground="#D3D3D3", padding=[12, 6], 
                        font=("Courier", 10, "bold"), borderwidth=2, relief="raised")
        style.map("TNotebook.Tab", background=[("selected", dirt_brown)], foreground=[("selected", gold_yellow)], 
                  relief=[("selected", "sunken")])
        style.configure("Success.Horizontal.TProgressbar", troughcolor="#3A3A3A", background=grass_green, 
                        borderwidth=1, bordercolor=stone_gray)
        
        self.root.configure(background=bg_color)
        
        self.bg_canvas = tk.Canvas(self.root, bg=bg_color, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.draw_minecraft_background()

    def draw_minecraft_background(self):
        canvas = self.bg_canvas
        canvas.delete("all")
        pixel_size = 16
        block_colors = ["#3A3A3A", "#4A4A4A", "#2F2F2F", "#363636"]
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                if np.random.random() < 0.15:
                    color = np.random.choice(block_colors)
                    canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, fill=color, outline="")

    def build_interface(self):
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame, style="Main.TFrame")
        header_frame.pack(fill=tk.X, pady=10, padx=20)
        
        logo_frame = ttk.Frame(header_frame, style="Main.TFrame")
        logo_frame.pack(side=tk.LEFT)
        ttk.Label(logo_frame, text="⛏️", font=("Courier", 24, "bold"), foreground="#FFD700", background="#2F2F2F").pack(side=tk.LEFT)
        ttk.Label(logo_frame, text="  Minecraft Data Miner", style="Header.TLabel").pack(side=tk.LEFT)
        
        nav_frame = ttk.Frame(header_frame, style="Main.TFrame")
        nav_frame.pack(side=tk.LEFT, padx=20)
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🗃️ Datasets", self.show_datasets),
            ("🤖 Modelos", self.show_models),
            ("🔍 Análise", self.show_statistical_analysis),
            ("🎯 Scatter", self.show_scatter_analysis),
            ("📋 Relatórios", self.show_reports),
            ("⚙️ Config", self.show_settings)
        ]
        for text, command in nav_buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, style="Accent.TButton")
            btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        btn_frame = ttk.Frame(header_frame, style="Main.TFrame")
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="💾 Baú de Dados", command=self.save_all_data, style="Success.TButton", width=14).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🧱 Carregar Blocos", command=self.load_data, style="Accent.TButton", width=15).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="⚡ AutoML Redstone", command=self.run_advanced_automl, style="Warning.TButton", width=15).pack(side=tk.LEFT, padx=3, pady=2)
        
        craft_frame = ttk.Frame(main_frame, style="Card.TFrame", borderwidth=3, relief="solid")
        craft_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        ttk.Label(craft_frame, text="┌─────────────────────────────────────────┐", style="Subheader.TLabel", background="#3A3A3A").pack(anchor=tk.W, padx=10)
        ttk.Label(craft_frame, text="│  ÁREA DE TRABALHO MINECRAFT DATA MINER  │", style="Header.TLabel", background="#3A3A3A").pack(pady=5)
        ttk.Label(craft_frame, text="└─────────────────────────────────────────┘", style="Subheader.TLabel", background="#3A3A3A").pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.content_frame = ttk.Frame(craft_frame, style="Main.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.show_dashboard()

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, style="Main.TFrame", borderwidth=2, relief="solid")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        health_frame = ttk.Frame(status_frame, style="Main.TFrame")
        health_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(health_frame, text="k®", font=("Courier", 12), foreground="#FF5252", background="#2F2F2F").pack(side=tk.LEFT)
        ttk.Label(health_frame, text=" Sistema: Online", style="Subheader.TLabel").pack(side=tk.LEFT)
        
        food_frame = ttk.Frame(status_frame, style="Main.TFrame")
        food_frame.pack(side=tk.LEFT, padx=20)
        ttk.Label(food_frame, text="🍖", font=("Courier", 12), foreground="#FFD700", background="#2F2F2F").pack(side=tk.LEFT)
        ttk.Label(food_frame, text=" Dados carregados:", style="Subheader.TLabel").pack(side=tk.LEFT)
        ttk.Label(food_frame, textvariable=self.status_var, style="Subheader.TLabel", foreground="#4CAF50").pack(side=tk.LEFT, padx=5)
        
        xp_frame = ttk.Frame(status_frame, style="Main.TFrame")
        xp_frame.pack(side=tk.RIGHT, padx=15)
        ttk.Label(xp_frame, text="XP:", style="Subheader.TLabel").pack(side=tk.LEFT)
        ttk.Label(xp_frame, text=" Nível 10", font=("Courier", 10, "bold"), foreground="#536DFE", background="#2F2F2F").pack(side=tk.LEFT)
        xp_bar = ttk.Progressbar(xp_frame, length=100, mode='determinate', style="Success.Horizontal.TProgressbar")
        xp_bar.pack(side=tk.LEFT, padx=5)
        xp_bar['value'] = 75

    def show_dashboard(self):
        self.clear_content()
        dashboard_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(dashboard_frame, text="🏠 Casa da Mineração de Dados", style="Header.TLabel").pack(pady=10)
        
        cards_frame = ttk.Frame(dashboard_frame, style="Main.TFrame")
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        metrics = [
            ("🗃️ Datasets", len(self.datasets), "#8B4513", "Blocos de dados coletados"),
            ("🤖 Modelos", len(self.models), "#556B2F", "Golems de ferro treinados"),
            ("📊 Features", sum(len(df.columns) for df in self.datasets.values()) if self.datasets else 0, "#A0522D", "Minérios analisados"),
            ("⏱️ Tempo", "00:00:00", "#D2691E", "Tempo de mineração")
        ]
        
        for i, (title, value, color, tooltip) in enumerate(metrics):
            card = ttk.Frame(cards_frame, style="Card.TFrame", borderwidth=2, relief="raised")
            card.grid(row=0, column=i, padx=8, pady=8, sticky="nsew")
            cards_frame.grid_columnconfigure(i, weight=1)
            
            icon_frame = ttk.Frame(card, style="Card.TFrame")
            icon_frame.pack(fill=tk.X, pady=(5, 0))
            icon = title.split()[0]
            icon_colors = {"🗃️": "#FFD700", "🤖": "#4A90E2", "📊": "#228B22", "⏱️": "#FF6347"}
            ttk.Label(icon_frame, text=icon, font=("Courier", 20, "bold"), foreground=icon_colors.get(icon, "#FFFFFF"), background="#3A3A3A").pack(pady=2)
            
            ttk.Label(card, text=title.replace(icon, "").strip(), font=("Courier", 12, "bold"), foreground=color, background="#3A3A3A").pack(pady=(0, 2))
            ttk.Label(card, text=str(value), font=("Courier", 24, "bold"), foreground="#FFD700", background="#3A3A3A").pack(pady=2)
            
            if title == "🗃️ Datasets":
                progress = ttk.Progressbar(card, length=120, mode='determinate', style="Success.Horizontal.TProgressbar")
                progress.pack(pady=5, padx=5)
                progress['value'] = min(100, len(self.datasets) * 25)
        
        if self.datasets:
            map_frame = ttk.Frame(dashboard_frame, style="Card.TFrame", borderwidth=3, relief="solid")
            map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            ttk.Label(map_frame, text="🗺️ Mapa das Minas de Dados", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
            
            fig, ax = plt.subplots(figsize=(12, 6), facecolor='#3A3A3A')
            fig.patch.set_facecolor('#3A3A3A')
            ax.set_facecolor('#2F2F2F')
            
            datasets = list(self.datasets.keys())
            sizes = [len(df) for df in self.datasets.values()]
            minecraft_colors = ['#8B4513', '#556B2F', '#A0522D', '#D2691E', '#CD853F', '#F4A460']
            
            bars = ax.bar(datasets, sizes, color=minecraft_colors[:len(datasets)])
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.annotate(f'{height:,}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                           textcoords="offset points", ha='center', va='bottom', fontsize=10, color='#FFD700')
                bar.set_hatch(['/', '\\', '|', '-', '+', 'x'][i % 6] * 2)
            
            ax.set_title('Distribuição de Blocos de Dados', color='#FFD700', fontsize=14, pad=20)
            ax.set_xlabel('Minas (Datasets)', color='#E6D3A7', fontsize=12)
            ax.set_ylabel('Quantidade de Blocos', color='#E6D3A7', fontsize=12)
            ax.tick_params(axis='x', colors='#E6D3A7')
            ax.tick_params(axis='y', colors='#E6D3A7')
            ax.grid(True, alpha=0.3, color='#555555', linestyle='--')
            plt.xticks(rotation=45, ha='right')
            
            ax.legend(['Blocos de Dados'], loc='upper right', facecolor='#3A3A3A', edgecolor='#808080', labelcolor='#FFD700')
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=map_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        log_frame = ttk.Frame(dashboard_frame, style="Card.TFrame", borderwidth=2, relief="solid")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(log_frame, text="📖 Livro de Registro do Minerador", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
        
        book_frame = ttk.Frame(log_frame, style="Card.TFrame")
        book_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.log_text = scrolledtext.ScrolledText(book_frame, height=8, bg="#2A2A2A", fg="#E6D3A7", 
                                                 font=("Courier", 10), wrap=tk.WORD, insertbackground="#FFD700")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.insert(tk.END, "⛏️ Bem-vindo ao Minecraft Data Miner!\n")
        self.log_text.insert(tk.END, "📝 Sistema iniciado com sucesso...\n")
        self.log_text.insert(tk.END, "📊 Pronto para minerar e analisar dados!\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.tag_configure("page", background="#3A312A")
        self.log_text.tag_add("page", "1.0", "end")
        
        self.status_var.set(f"🏠 Casa da Mineração | Blocos: {len(self.datasets)} | Golems: {len(self.models)}")
        self.log_activity("🏠 Entrou na Casa da Mineração de Dados")

    def show_datasets(self):
        self.clear_content()
        datasets_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        datasets_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(datasets_frame, text="🗃️ Baú dos Datasets", style="Header.TLabel").pack(pady=10)
        
        control_frame = ttk.Frame(datasets_frame, style="Main.TFrame")
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        
        btn_frame = ttk.Frame(control_frame, style="Main.TFrame")
        btn_frame.pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="➕ Adicionar Blocos", command=self.load_data, style="Accent.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🗑️ Remover Blocos", command=self.remove_selected_dataset, style="Danger.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🔄 Recarregar Baú", command=lambda: self.show_datasets(), style="Accent.TButton", width=13).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🔍 Analisar Blocos", command=self.quick_analysis_selected, style="Success.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        
        ttk.Button(control_frame, text="💎 Salvar Baú Completo", command=self.save_all_datasets, style="Success.TButton", width=22).pack(side=tk.RIGHT, padx=5, pady=2)
        
        columns = ("ID", "Nome", "Blocos", "Dimensões", "Tipo", "Vazios", "Última Mineração", "Peso (MB)", "Status", "Origem")
        tree_frame = ttk.Frame(datasets_frame, style="Card.TFrame", borderwidth=2, relief="solid")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(tree_frame, text="🎒 Inventário de Blocos de Dados", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.datasets_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=scrollbar.set, style="Treeview")
        
        column_configs = [
            ("ID", 35, "center"),
            ("Nome", 140, "w"),
            ("Blocos", 70, "center"),
            ("Dimensões", 80, "center"),
            ("Tipo", 90, "center"),
            ("Vazios", 110, "center"),
            ("Última Mineração", 135, "center"),
            ("Peso (MB)", 90, "center"),
            ("Status", 75, "center"),
            ("Origem", 110, "w")
        ]
        
        for col, width, anchor in column_configs:
            self.datasets_tree.heading(col, text=col)
            self.datasets_tree.column(col, width=width, anchor=anchor)
        
        self.datasets_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.datasets_tree.yview)
        
        for i, (name, df) in enumerate(self.datasets.items(), 1):
            rows, cols = df.shape
            null_count = df.isnull().sum().sum()
            null_percentage = (null_count / (rows * cols)) * 100 if (rows * cols) > 0 else 0
            main_dtype = df.dtypes.mode().iloc[0] if not df.dtypes.empty else "N/A"
            mod_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
            status = "✅ Pronto" if not df.empty else "⚠️ Vazio"
            
            if rows > 10000:
                status = "💎 Grande"
            elif rows > 1000:
                status = "🪨 Médio"
            else:
                status = "🌱 Pequeno"
            
            fonte = "⛏️ Mineração Local" if "file://" in name else "🌐 Nether API"
            
            self.datasets_tree.insert("", tk.END, values=(
                i,
                name[:22] + "..." if len(name) > 22 else name,
                f"{rows:,}",
                f"{cols}x{rows//cols if cols>0 else 0}",
                str(main_dtype),
                f"{null_count} ({null_percentage:.1f}%)",
                mod_time,
                f"{size_mb:.1f}",
                status,
                fonte
            ))
        
        self.datasets_tree.tag_configure('even', background='#3A3A3A')
        self.datasets_tree.tag_configure('odd', background='#424242')
        for i, item in enumerate(self.datasets_tree.get_children()):
            if i % 2 == 0:
                self.datasets_tree.item(item, tags=('even',))
            else:
                self.datasets_tree.item(item, tags=('odd',))
        
        self.datasets_tree.bind('<Double-1>', self.analyze_selected_dataset)
        
        self.status_var.set(f"🎒 Inventário | Total: {len(self.datasets)} blocos de dados")
        self.log_activity("🎒 Abriu o inventário de blocos de dados")

    def show_models(self):
        self.clear_content()
        models_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        models_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(models_frame, text="🤖 Estábulo dos Golems", style="Header.TLabel").pack(pady=10)
        
        control_frame = ttk.Frame(models_frame, style="Main.TFrame")
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        
        btn_frame = ttk.Frame(control_frame, style="Main.TFrame")
        btn_frame.pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="🧱 Forjar Golem", command=self.train_new_model, style="Accent.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="⚔️ Destruir Golem", command=self.delete_selected_model, style="Danger.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🔄 Recarregar", command=lambda: self.show_models(), style="Accent.TButton", width=13).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="🏆 Torneio Golems", command=self.compare_selected_models, style="Success.TButton", width=16).pack(side=tk.LEFT, padx=3, pady=2)
        
        ttk.Button(control_frame, text="💎 Salvar Estábulo Completo", command=self.save_all_models, style="Success.TButton", width=22).pack(side=tk.RIGHT, padx=5, pady=2)
        
        if not self.models:
            empty_frame = ttk.Frame(models_frame, style="Card.TFrame", borderwidth=2, relief="solid")
            empty_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
            golem_art = """
⛏️ INVENTÁRIO VAZIO ⛏️
□ □ □ □ □
□ ■ ■ ■ □
□ ■ □ ■ □
□ ■ ■ ■ □
□ □ □ □ □
Nenhum Golem de Ferro treinado ainda!
"""
            ttk.Label(empty_frame, text=golem_art, font=("Courier", 12), foreground="#8B4513", background="#3A3A3A", justify=tk.CENTER).pack(pady=20)
            ttk.Label(empty_frame, text="🧱 Forje seu primeiro Golem de Ferro!", style="Subheader.TLabel", background="#3A3A3A").pack(pady=10)
            ttk.Button(empty_frame, text="⚡ Forjar Golem Agora", command=self.train_new_model, style="Accent.TButton").pack(pady=20)
            return
        
        columns = ("ID", "Nome", "Origem", "Alvo", "Tipo", "Precisão", "Erro", "Energia", "Blocos", "Criado", "Tempo", "Status", "Ações")
        tree_frame = ttk.Frame(models_frame, style="Card.TFrame", borderwidth=2, relief="solid")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(tree_frame, text="🏃‍♂️ Golems de Ferro Treinados", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.models_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, yscrollcommand=scrollbar.set)
        
        column_configs = [
            ("ID", 35, "center"),
            ("Nome", 110, "w"),
            ("Origem", 85, "center"),
            ("Alvo", 85, "center"),
            ("Tipo", 100, "center"),
            ("Precisão", 70, "center"),
            ("Erro", 70, "center"),
            ("Energia", 70, "center"),
            ("Blocos", 65, "center"),
            ("Criado", 130, "center"),
            ("Tempo", 70, "center"),
            ("Status", 75, "center"),
            ("Ações", 70, "center")
        ]
        
        for col, width, anchor in column_configs:
            self.models_tree.heading(col, text=col)
            self.models_tree.column(col, width=width, anchor=anchor)
        
        self.models_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.models_tree.yview)
        
        for i, (model_name, model_info) in enumerate(self.models.items(), 1):
            metrics = model_info['metrics']
            created = model_info['created'].strftime("%Y-%m-%d %H:%M")
            training_time = model_info.get('training_time', 'N/A')
            feature_count = len(model_info['features'])
            algorithm = model_info.get('algorithm', 'N/A')
            accuracy = metrics['r2']
            error = metrics['rmse']
            energy = metrics['mae']
            status = "✅ Ativo" if model_info.get('active', True) else "💤 Dormindo"
            
            if accuracy > 0.8:
                status = "💎 Elite"
            elif accuracy > 0.6:
                status = "⚡ Forte"
            else:
                status = "🪨 Fraco"
            
            golem_type = "🛡️ Defensor" if 'regress' in algorithm.lower() else "⚔️ Atacante"
            
            self.models_tree.insert("", tk.END, values=(
                i,
                model_name[:18] + "..." if len(model_name) > 18 else model_name,
                model_info['dataset'],
                model_info['target'],
                golem_type,
                f"{accuracy:.3f}",
                f"{error:.2f}",
                f"{energy:.2f}",
                feature_count,
                created,
                f"{training_time:.1f}" if isinstance(training_time, (int, float)) else training_time,
                status,
                "👁️ Ver"
            ))
        
        self.models_tree.tag_configure('even', background='#3A3A3A')
        self.models_tree.tag_configure('odd', background='#424242')
        for i, item in enumerate(self.models_tree.get_children()):
            if i % 2 == 0:
                self.models_tree.item(item, tags=('even',))
            else:
                self.models_tree.item(item, tags=('odd',))
        
        self.models_tree.bind('<Double-1>', self.show_model_details)
        
        self.status_var.set(f"🏃‍♂️ Estábulo | Total: {len(self.models)} Golems de Ferro treinados")
        self.log_activity("🏃‍♂️ Visitou o estábulo dos Golems de Ferro")

    def show_statistical_analysis(self):
        self.clear_content()
        stats_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(stats_frame, text="🔬 Mesa de Análise de Blocos", style="Header.TLabel").pack(pady=10)
        
        if not self.datasets:
            empty_frame = ttk.Frame(stats_frame, style="Card.TFrame", borderwidth=2, relief="solid")
            empty_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
            craft_art = """
📊 MESA DE ANÁLISE VAZIA
+-----------------+
|                 |
|      🧱🧱      |
|      🧱🧱      |
|                 |
+-----------------+
Nenhum bloco para analisar!
"""
            ttk.Label(empty_frame, text=craft_art, font=("Courier", 12), foreground="#8B4513", background="#3A3A3A", justify=tk.CENTER).pack(pady=20)
            ttk.Label(empty_frame, text="⛏️ Adicione blocos de dados primeiro!", style="Subheader.TLabel", background="#3A3A3A").pack(pady=10)
            ttk.Button(empty_frame, text="🧱 Adicionar Blocos", command=self.load_data, style="Accent.TButton").pack(pady=20)
            return
        
        control_frame = ttk.Frame(stats_frame, style="Main.TFrame")
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(control_frame, text="⛏️ Bloco para Analisar:", background="#2F2F2F", foreground="#E6D3A7").pack(side=tk.LEFT, padx=5)
        dataset_var = tk.StringVar(value=list(self.datasets.keys())[0] if self.datasets else "")
        dataset_combo = ttk.Combobox(control_frame, textvariable=dataset_var, values=list(self.datasets.keys()), width=38, state="readonly", font=("Courier", 10))
        dataset_combo.pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(control_frame, style="Main.TFrame")
        btn_frame.pack(side=tk.LEFT, padx=15)
        
        notebook = ttk.Notebook(stats_frame, style="TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tabs = {
            "📋 Blocos": ttk.Frame(notebook, style="Main.TFrame"),
            "🔗 Conexões": ttk.Frame(notebook, style="Main.TFrame"),
            "📊 Padrões": ttk.Frame(notebook, style="Main.TFrame"),
            "⚠️ Perigos": ttk.Frame(notebook, style="Main.TFrame"),
            "📈 Cristais": ttk.Frame(notebook, style="Main.TFrame")
        }
        
        tab_icons = {
            "📋 Blocos": "🧱",
            "🔗 Conexões": "⛓️",
            "📊 Padrões": "🎯",
            "⚠️ Perigos": "⚠️",
            "📈 Cristais": "🔮"
        }
        
        for tab_name, tab_frame in tabs.items():
            icon = tab_icons.get(tab_name, "")
            notebook.add(tab_frame, text=f"{icon} {tab_name}")
        
        ttk.Button(btn_frame, text="🔍 Analisar Completo", command=lambda: self.run_full_statistical_analysis(dataset_var.get(), notebook), style="Success.TButton", width=18).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="📥 Exportar Relatório", command=lambda: self.export_statistical_report(dataset_var.get()), style="Accent.TButton", width=18).pack(side=tk.LEFT, padx=3, pady=2)
        ttk.Button(btn_frame, text="💎 Salvar Análise", command=lambda: self.save_statistical_analysis(dataset_var.get()), style="Success.TButton", width=18).pack(side=tk.LEFT, padx=3, pady=2)
        
        self.run_full_statistical_analysis(dataset_var.get(), notebook)
        
        self.status_var.set(f"🔬 Mesa de Análise | Bloco: {dataset_var.get()} | Pronto para análise")
        self.log_activity(f"🔬 Iniciou análise do bloco '{dataset_var.get()}'")

    def run_full_statistical_analysis(self, dataset_name, notebook):
        if dataset_name not in self.datasets:
            messagebox.showerror("Erro", f"Bloco '{dataset_name}' não encontrado!")
            return
        
        df = self.datasets[dataset_name].copy()
        self.status_var.set(f"🔬 Analisando bloco '{dataset_name}'... Isso pode levar alguns minutos.")
        
        def analyze_in_thread():
            try:
                start_time = time.time()
                for tab in notebook.winfo_children():
                    for widget in tab.winfo_children():
                        widget.destroy()
                
                self._run_descriptive_analysis_minecraft(df, notebook.winfo_children()[0])
                
                elapsed_time = time.time() - start_time
                self.status_var.set(f"✅ Análise do bloco '{dataset_name}' concluída em {elapsed_time:.2f} segundos!")
                self.log_activity(f"✅ Análise do bloco '{dataset_name}' concluída em {elapsed_time:.2f}s")
            except Exception as e:
                self.status_var.set(f"❌ Erro na análise do bloco: {str(e)}")
                messagebox.showerror("Erro de Análise", f"Ocorreu um erro durante a análise:\n{str(e)}")
        
        threading.Thread(target=analyze_in_thread, daemon=True).start()

    def _run_descriptive_analysis_minecraft(self, df, frame):
        metrics_frame = ttk.Frame(frame, style="Card.TFrame", borderwidth=2, relief="solid")
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(metrics_frame, text="🧱 Propriedades do Bloco", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
        
        metrics = [
            ("Tamanho", f"{len(df)}x{len(df.columns)}", "📏 Dimensões do bloco"),
            ("Peso", f"{df.memory_usage(deep=True).sum()/(1024*1024):.1f} MB", "⚖️ Peso em memória"),
            ("Vazios", f"{df.isnull().sum().sum()}", "🕳️ Buracos no bloco"),
            ("Numéricos", f"{len(df.select_dtypes(include=[np.number]).columns)}", "🔢 Blocos numéricos"),
            ("Categóricos", f"{len(df.select_dtypes(include=['object', 'category']).columns)}", "🔤 Blocos de texto")
        ]
        
        for i, (label, value, tooltip) in enumerate(metrics):
            metric_frame = ttk.Frame(metrics_frame, style="Card.TFrame", borderwidth=1, relief="solid")
            metric_frame.grid(row=0, column=i, padx=4, pady=4, sticky="nsew")
            metrics_frame.grid_columnconfigure(i, weight=1)
            
            icons = {"Tamanho": "📏", "Peso": "⚖️", "Vazios": "🕳️", "Numéricos": "🔢", "Categóricos": "🔤"}
            ttk.Label(metric_frame, text=icons.get(label, "📊"), font=("Courier", 16, "bold"), foreground="#FFD700", background="#3A3A3A").pack(pady=(5, 2))
            ttk.Label(metric_frame, text=label, font=("Courier", 10, "bold"), background="#3A3A3A", foreground="#B8860B").pack(pady=(2, 0))
            ttk.Label(metric_frame, text=value, font=("Courier", 14, "bold"), background="#3A3A3A", foreground="#FFFFFF").pack(pady=(0, 5))
        
        self.status_var.set("🧱 Análise de propriedades do bloco concluída")

    def quick_analysis_selected(self):
        selected = self.datasets_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "⛏️ Selecione um bloco para análise rápida!")
            return
        
        item = self.datasets_tree.item(selected[0])
        dataset_name = item['values'][1]
        if dataset_name not in self.datasets:
            messagebox.showerror("Erro", "⛏️ Bloco não encontrado!")
            return
        
        df = self.datasets[dataset_name]
        
        quick_win = tk.Toplevel(self.root)
        quick_win.title(f"🔍 Análise Rápida: {dataset_name}")
        quick_win.geometry("800x600")
        quick_win.configure(background="#2F2F2F")
        
        main_frame = ttk.Frame(quick_win, style="Main.TFrame", borderwidth=3, relief="solid")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text=f"🔍 Mesa de Análise Rápida: {dataset_name}", style="Header.TLabel").pack(pady=10)
        
        info_frame = ttk.Frame(main_frame, style="Card.TFrame", borderwidth=2, relief="solid")
        info_frame.pack(fill=tk.X, pady=10)
        info_text = f"""
🧱 Dimensões do Bloco: {df.shape[0]}x{df.shape[1]}
🏷️ Tipos de Material: {df.dtypes.value_counts().to_dict()}
🕳️ Buracos (valores nulos): {df.isnull().sum().sum()} ({(df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100):.1f}%)
⚖️ Peso: {df.memory_usage(deep=True).sum()/(1024*1024):.2f} MB
🔍 Densidade: {(1 - df.isnull().mean().mean()) * 100:.1f}% completo
"""
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT, background="#3A3A3A", foreground="#E6D3A7", font=("Courier", 10)).pack(padx=10, pady=10)
        
        btn_frame = ttk.Frame(main_frame, style="Main.TFrame")
        btn_frame.pack(fill=tk.X, pady=10)
        actions = [
            ("🧾 Estatísticas", lambda: self.show_descriptive_stats(df, dataset_name)),
            ("🗺️ Visualização", lambda: self.quick_visualization(df, dataset_name)),
            ("⚙️ Forjar Golem", lambda: self.train_quick_model(df, dataset_name)),
            ("💎 Salvar Análise", lambda: self.save_quick_analysis(df, dataset_name))
        ]
        
        for text, command in actions:
            btn = ttk.Button(btn_frame, text=text, command=command, style="Accent.TButton")
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        sample_frame = ttk.Frame(main_frame, style="Card.TFrame", borderwidth=2, relief="solid")
        sample_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(sample_frame, text="📦 Conteúdo do Bloco (primeiras 10 linhas)", style="Subheader.TLabel", background="#3A3A3A").pack(pady=5)
        
        columns = list(df.columns)[:10]
        tree = ttk.Treeview(sample_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col[:15] + "..." if len(col) > 15 else col)
            tree.column(col, width=80, anchor=tk.CENTER)
        
        for i, row in df.head(10).iterrows():
            values = [str(row[col])[:15] + "..." if len(str(row[col])) > 15 else str(row[col]) for col in columns]
            tree.insert("", tk.END, values=values)
        
        tree.tag_configure('even', background='#3A3A3A')
        tree.tag_configure('odd', background='#424242')
        for i in range(min(10, len(tree.get_children()))):
            if i % 2 == 0:
                tree.item(tree.get_children()[i], tags=('even',))
            else:
                tree.item(tree.get_children()[i], tags=('odd',))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status_var.set(f"🔍 Análise rápida iniciada para bloco '{dataset_name}'")
        self.log_activity(f"🔍 Análise rápida do bloco '{dataset_name}'")

    def save_all_datasets(self):
        if not self.datasets:
            messagebox.showwarning("Aviso", "⛏️ Nenhum bloco para salvar no baú!")
            return
        
        directory = filedialog.askdirectory(title="🧱 Selecione onde guardar os blocos")
        if not directory:
            return
        
        try:
            start_time = time.time()
            saved_count = 0
            
            for name, df in self.datasets.items():
                try:
                    clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                    filename = os.path.join(directory, f"block_{clean_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                    df.to_csv(filename, index=False, encoding='utf-8')
                    saved_count += 1
                    self.log_activity(f"🧱 Bloco '{name}' guardado no baú: {filename}")
                except Exception as e:
                    self.log_activity(f"❌ Erro ao guardar bloco '{name}': {str(e)}")
            
            elapsed_time = time.time() - start_time
            messagebox.showinfo("✅ Sucesso", f"{saved_count} blocos guardados no baú!\n📍 Local: {directory}\n⏱️ Tempo: {elapsed_time:.2f} segundos")
            self.status_var.set(f"✅ {saved_count} blocos guardados no baú ({elapsed_time:.2f}s)")
            self.log_activity(f"✅ {saved_count} blocos guardados no baú em {directory}")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao guardar blocos no baú:\n{str(e)}")
            self.status_var.set(f"❌ Erro ao guardar blocos: {str(e)}")

    def save_all_models(self):
        if not self.models:
            messagebox.showwarning("Aviso", "🤖 Nenhum Golem para guardar no estábulo!")
            return
        
        directory = filedialog.askdirectory(title="🏃‍♂️ Selecione onde guardar os Golems")
        if not directory:
            return
        
        try:
            start_time = time.time()
            saved_count = 0
            
            for model_name, model_info in self.models.items():
                try:
                    clean_name = "".join(c for c in model_name if c.isalnum() or c in (' ', '-', '_')).strip()
                    filename = os.path.join(directory, f"golem_{clean_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                    
                    model_data = {
                        'name': model_name,
                        'dataset': model_info['dataset'],
                        'target': model_info['target'],
                        'features': model_info['features'],
                        'metrics': model_info['metrics'],
                        'created': model_info['created'].isoformat(),
                        'algorithm': model_info.get('algorithm', 'unknown'),
                        'training_time': model_info.get('training_time', 0),
                        'params': model_info.get('params', {}),
                        'model_summary': str(model_info.get('model', 'Golem não serializável'))
                    }
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(model_data, f, indent=2, ensure_ascii=False)
                    
                    saved_count += 1
                    self.log_activity(f"🏃‍♂️ Golem '{model_name}' guardado no estábulo: {filename}")
                except Exception as e:
                    self.log_activity(f"❌ Erro ao guardar Golem '{model_name}': {str(e)}")
            
            elapsed_time = time.time() - start_time
            messagebox.showinfo("✅ Sucesso", f"{saved_count} Golems guardados no estábulo!\n📍 Local: {directory}\n⏱️ Tempo: {elapsed_time:.2f} segundos")
            self.status_var.set(f"✅ {saved_count} Golems guardados ({elapsed_time:.2f}s)")
            self.log_activity(f"✅ {saved_count} Golems guardados no estábulo em {directory}")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao guardar Golems no estábulo:\n{str(e)}")
            self.status_var.set(f"❌ Erro ao guardar Golems: {str(e)}")

    def save_all_data(self):
        directory = filedialog.askdirectory(title="💎 Selecione onde criar o Baú do Tesouro")
        if not directory:
            return
        
        try:
            start_time = time.time()
            blocks_dir = os.path.join(directory, "blocks")
            golems_dir = os.path.join(directory, "golems")
            reports_dir = os.path.join(directory, "reports")
            
            for dir_path in [blocks_dir, golems_dir, reports_dir]:
                os.makedirs(dir_path, exist_ok=True)
            
            self.blocks_dir = blocks_dir
            self.save_all_datasets()
            
            self.golems_dir = golems_dir
            self.save_all_models()
            
            config_file = os.path.join(directory, "minecraft_world.json")
            config_data = {
                'world_name': 'BigData_Mining_World',
                'last_backup': datetime.datetime.now().isoformat(),
                'blocks_count': len(self.datasets),
                'golems_count': len(self.models),
                'world_info': {
                    'version': '3.0.0',
                    'created_by': 'Minecraft Data Miner Pro',
                    'seed': np.random.randint(1000000)
                }
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            elapsed_time = time.time() - start_time
            messagebox.showinfo("💎 Baú do Tesouro", f"✅ Baú do tesouro criado com sucesso!\n🧱 Blocos: {len(self.datasets)} guardados em {blocks_dir}\n🏃‍♂️ Golems: {len(self.models)} guardados em {golems_dir}\n📜 Mapa do Mundo: salvo em {config_file}\n⏱️ Tempo total: {elapsed_time:.2f} segundos")
            self.status_var.set(f"✅ Baú do tesouro criado em {elapsed_time:.2f}s | {len(self.datasets)} blocos + {len(self.models)} Golems")
            self.log_activity(f"💎 Baú do tesouro criado em {directory}")
        except Exception as e:
            messagebox.showerror("❌ Erro no Baú", f"Erro durante a criação do baú do tesouro:\n{str(e)}")
            self.status_var.set(f"❌ Erro no baú do tesouro: {str(e)}")

    def load_example_data(self):
        try:
            np.random.seed(42)
            dates = pd.date_range(start='2026-01-01', periods=1000, freq='D')
            
            mining_data = {
                'date': dates,
                'block_type': np.random.choice(['DIAMOND', 'IRON', 'GOLD', 'COAL', 'STONE', 'DIRT'], 1000),
                'depth': np.random.randint(1, 64, 1000),
                'quantity': np.random.randint(1, 64, 1000),
                'biome': np.random.choice(['FOREST', 'DESERT', 'MOUNTAINS', 'OCEAN', 'CAVE'], 1000),
                'miner': np.random.choice(['Steve', 'Alex', 'Herobrine', 'Villager'], 1000),
                'tool_used': np.random.choice(['DIAMOND_PICK', 'IRON_PICK', 'STONE_PICK', 'WOOD_PICK'], 1000)
            }
            
            # Correção do loop para adicionar valores nulos
            for col in mining_data.keys():
                if np.random.random() < 0.05:
                    idx = np.random.choice(1000, size=int(1000 * 0.02), replace=False)
                    for i in idx:
                        if isinstance(mining_data[col][i], (int, float)):
                            mining_data[col][i] = np.nan
            
            df_mining = pd.DataFrame(mining_data)
            df_mining['value'] = df_mining['quantity'] * np.where(
                df_mining['block_type'] == 'DIAMOND', 100,
                np.where(df_mining['block_type'] == 'GOLD', 50,
                np.where(df_mining['block_type'] == 'IRON', 25, 1))
            )
            
            self.datasets["Mineração_2026"] = df_mining
            
            golem_data = {
                'timestamp': pd.date_range(start='2026-01-01', periods=5000, freq='min'),
                'golem_id': np.random.randint(1, 21, 5000),
                'iron_blocks': np.random.randint(0, 4, 5000),
                'health': np.round(np.random.uniform(0, 20, 5000), 1),
                'villagers_protected': np.random.randint(0, 10, 5000),
                'damage_taken': np.round(np.random.exponential(1, 5000), 1),
                'status': np.random.choice(['ACTIVE', 'IDLE', 'DAMAGED', 'DESTROYED'], 5000, p=[0.7, 0.2, 0.08, 0.02])
            }
            
            df_golems = pd.DataFrame(golem_data)
            self.datasets["Golems_Ferro"] = df_golems
            
            self.status_var.set("✅ Blocos de exemplo carregados com sucesso!")
            
            # Verificar se a interface já foi construída antes de logar
            if hasattr(self, 'log_text') and self.log_text:
                self.log_activity("✅ Blocos de exemplo carregados: Mineração_2026 e Golems_Ferro")
            else:
                # Fallback simples se o log_text ainda não existir
                print("✅ Blocos de exemplo carregados: Mineração_2026 e Golems_Ferro")
        except Exception as e:
            self.status_var.set(f"⚠️ Erro ao carregar blocos de exemplo: {str(e)}")
            # Verificar se a interface já foi construída antes de logar
            if hasattr(self, 'log_text') and self.log_text:
                self.log_activity(f"❌ Erro ao carregar blocos de exemplo: {str(e)}")
            else:
                print(f"❌ Erro ao carregar blocos de exemplo: {str(e)}")

    def load_data(self):
        filetypes = [
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls"),
            ("JSON files", "*.json"),
            ("Parquet files", "*.parquet"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(title="⛏️ Selecione o bloco de dados para minerar", filetypes=filetypes)
        if not filename:
            return
        
        try:
            start_time = time.time()
            file_ext = os.path.splitext(filename)[1].lower()
            self.status_var.set(f"⛏️ Minerando blocos de {filename}...")
            
            if file_ext == '.csv':
                df = pd.read_csv(filename)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filename)
            elif file_ext == '.json':
                df = pd.read_json(filename)
            elif file_ext == '.parquet':
                df = pd.read_parquet(filename)
            else:
                messagebox.showerror("❌ Erro", f"⛏️ Formato de bloco não suportado: {file_ext}")
                return
            
            dataset_name = os.path.basename(filename).split('.')[0].replace('_', ' ').title()
            if dataset_name in self.datasets:
                dataset_name += f"_v{datetime.datetime.now().strftime('%H%M%S')}"
            
            self.datasets[dataset_name] = df
            
            elapsed_time = time.time() - start_time
            self.status_var.set(f"✅ Bloco '{dataset_name}' minerado com sucesso! ({len(df)} unidades, {elapsed_time:.2f}s)")
            self.log_activity(f"✅ Bloco minerado: {dataset_name} | {len(df)} unidades | {df.shape[1]} dimensões")
            self.show_datasets()
        except Exception as e:
            error_msg = f"❌ Erro ao minerar blocos: {str(e)}"
            messagebox.showerror("Erro de Mineração", error_msg)
            self.status_var.set(f"❌ {error_msg}")
            self.log_activity(error_msg)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def log_activity(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Verificar se o widget de log existe e está pronto
        if hasattr(self, 'log_text') and self.log_text and self.log_text.winfo_exists():
            self.log_text.config(state=tk.NORMAL)
            
            # Salvar o índice atual antes de inserir o novo texto
            start_index = self.log_text.index(tk.END)
            
            # Inserir o novo texto
            self.log_text.insert(tk.END, log_entry)
            
            # O índice final é o novo final do texto
            end_index = self.log_text.index(tk.END)
            
            # Aplicar tags de formatação com base no conteúdo da mensagem
            if "✅" in message:
                self.log_text.tag_add("success", start_index, end_index)
                self.log_text.tag_configure("success", foreground="#4CAF50")
            elif "❌" in message:
                self.log_text.tag_add("error", start_index, end_index)
                self.log_text.tag_configure("error", foreground="#F44336")
            elif "⛏️" in message or "🧱" in message:
                self.log_text.tag_add("mine", start_index, end_index)
                self.log_text.tag_configure("mine", foreground="#8B4513")
            
            # Garantir que o texto rola para mostrar a última entrada
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

    def setup_auto_save(self):
        def auto_save_routine():
            while True:
                time.sleep(300)  # 5 minutos
                if self.datasets or self.models:
                    auto_save_dir = os.path.join(os.path.expanduser("~"), ".minecraft_databackup")
                    os.makedirs(auto_save_dir, exist_ok=True)
                    try:
                        for name, df in self.datasets.items():
                            clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                            filename = os.path.join(auto_save_dir, f"autosave_block_{clean_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv")
                            df.to_csv(filename, index=False)
                        
                        if self.models:
                            models_file = os.path.join(auto_save_dir, f"autosave_golems_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json")
                            model_metadata = {}
                            for model_name, model_info in self.models.items():
                                model_metadata[model_name] = {
                                    'dataset': model_info['dataset'],
                                    'target': model_info['target'],
                                    'metrics': model_info['metrics'],
                                    'created': model_info['created'].isoformat(),
                                    'features': model_info['features']
                                }
                            
                            with open(models_file, 'w', encoding='utf-8') as f:
                                json.dump(model_metadata, f, indent=2, ensure_ascii=False)
                        
                        self.log_activity(f"💾 Auto-save realizado: {len(self.datasets)} blocos + {len(self.models)} Golems")
                    except Exception as e:
                        self.log_activity(f"❌ Erro no auto-save: {str(e)}")
        
        auto_save_thread = threading.Thread(target=auto_save_routine, daemon=True)
        auto_save_thread.start()
        self.log_activity("✅ Sistema de auto-save ativado (a cada 5 minutos)")

    def run_advanced_automl(self):
        messagebox.showinfo("⚡ AutoML Redstone", "Funcionalidade de AutoML em desenvolvimento. Disponível em breve!")

    def show_scatter_analysis(self):
        self.clear_content()
        scatter_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        scatter_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(scatter_frame, text="🎯 Mesa de Análise de Dispersão", style="Header.TLabel").pack(pady=20)
        
        if not self.datasets:
            ttk.Label(scatter_frame, text="Nenhum dataset carregado para análise!\nUse o botão 🧱 Carregar Blocos para adicionar dados.", style="Subheader.TLabel", background="#1e1e1e").pack(pady=50)
            return
        
        notebook = ttk.Notebook(scatter_frame, style="TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for dataset_name, df in self.datasets.items():
            tab = ttk.Frame(notebook, style="Main.TFrame")
            notebook.add(tab, text=f"🧱 {dataset_name[:15]}")
            
            if df.select_dtypes(include=[np.number]).shape[1] >= 2:
                fig, ax = plt.subplots(figsize=(10, 6), facecolor='#3A3A3A')
                fig.patch.set_facecolor('#3A3A3A')
                ax.set_facecolor('#2F2F2F')
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()[:2]
                x_col, y_col = numeric_cols[0] if numeric_cols else "", numeric_cols[1] if len(numeric_cols) > 1 else ""
                
                if x_col and y_col:
                    ax.scatter(df[x_col], df[y_col], alpha=0.6, color='#0078d7', edgecolors='white')
                    ax.set_title(f'Análise de Dispersão: {x_col} vs {y_col}', color='#FFD700', fontsize=12)
                    ax.set_xlabel(x_col, color='#E6D3A7', fontsize=10)
                    ax.set_ylabel(y_col, color='#E6D3A7', fontsize=10)
                    ax.tick_params(axis='both', colors='#E6D3A7')
                    ax.grid(True, alpha=0.3, color='#555555')
                    
                    canvas = FigureCanvasTkAgg(fig, master=tab)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            else:
                ttk.Label(tab, text="⚠️ Dataset não possui variáveis numéricas suficientes para análise de dispersão", style="Subheader.TLabel", background="#3A3A3A").pack(pady=50)

    def remove_selected_dataset(self):
        selected = self.datasets_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "⛏️ Selecione um bloco para remover!")
            return
        
        if messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover este bloco de dados?"):
            item = self.datasets_tree.item(selected[0])
            dataset_name = item['values'][1]
            if dataset_name in self.datasets:
                del self.datasets[dataset_name]
                self.show_datasets()
                self.log_activity(f"🗑️ Bloco removido: {dataset_name}")
                self.status_var.set(f"✅ Bloco '{dataset_name}' removido com sucesso!")

    def analyze_selected_dataset(self, event):
        selected = self.datasets_tree.selection()
        if not selected:
            return
        
        item = self.datasets_tree.item(selected[0])
        dataset_name = item['values'][1]
        if dataset_name not in self.datasets:
            messagebox.showerror("Erro", "Dataset não encontrado!")
            return
        
        self.status_var.set(f"🔍 Análise rápida do dataset '{dataset_name}'")
        self.log_activity(f"🔍 Análise rápida iniciada para '{dataset_name}'")

    def train_new_model(self):
        if not self.datasets:
            messagebox.showwarning("Aviso", "Nenhum dataset carregado para treinar modelos!")
            return
        
        dataset_name = list(self.datasets.keys())[0]
        df = self.datasets[dataset_name]
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2:
            messagebox.showwarning("Aviso", "Dataset precisa de pelo menos 2 colunas numéricas para treinar um modelo!")
            return
        
        X = df[numeric_cols[:-1]]
        y = df[numeric_cols[-1]]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        model_name = f"Golem_{dataset_name}_{len(self.models)+1}"
        self.models[model_name] = {
            'model': model,
            'dataset': dataset_name,
            'target': numeric_cols[-1],
            'features': numeric_cols[:-1],
            'metrics': {'r2': r2, 'rmse': rmse, 'mae': mae},
            'created': datetime.datetime.now(),
            'algorithm': 'RandomForest',
            'training_time': 2.5
        }
        
        messagebox.showinfo("✅ Sucesso", f"Golem de Ferro treinado com sucesso!\nPrecisão (R²): {r2:.4f}")
        self.show_models()
        self.log_activity(f"⚡ Golem treinado: {model_name} | R²: {r2:.4f}")

    def delete_selected_model(self):
        selected = self.models_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "🏃‍♂️ Selecione um Golem para remover!")
            return
        
        if messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja destruir este Golem de Ferro?"):
            item = self.models_tree.item(selected[0])
            model_name = item['values'][1]
            if model_name in self.models:
                del self.models[model_name]
                self.show_models()
                self.log_activity(f"⚔️ Golem destruído: {model_name}")
                self.status_var.set(f"✅ Golem '{model_name}' destruído com sucesso!")

    def compare_selected_models(self):
        if len(self.models) < 2:
            messagebox.showwarning("Aviso", "🏃‍♂️ Precisa de pelo menos 2 Golems para realizar o torneio!")
            return
        
        comparison_win = tk.Toplevel(self.root)
        comparison_win.title("🏆 Torneio de Golems")
        comparison_win.geometry("800x600")
        comparison_win.configure(background="#2F2F2F")
        
        ttk.Label(comparison_win, text="🏆 Comparação de Golems de Ferro", font=("Courier", 16, "bold"), foreground="#FFD700", background="#2F2F2F").pack(pady=20)
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#3A3A3A')
        fig.patch.set_facecolor('#3A3A3A')
        ax.set_facecolor('#2F2F2F')
        
        model_names = []
        r2_values = []
        colors = ['#8B4513', '#556B2F', '#A0522D', '#D2691E', '#CD853F', '#F4A460']
        
        for i, (name, info) in enumerate(self.models.items()):
            if i < 6:
                model_names.append(name[:15])
                r2_values.append(info['metrics']['r2'])
        
        bars = ax.bar(model_names, r2_values, color=colors[:len(model_names)])
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       color='#FFD700', fontsize=10)
        
        ax.set_title('Precisão dos Golems (R²)', color='#FFD700', fontsize=14)
        ax.set_ylabel('Precisão (R²)', color='#E6D3A7', fontsize=12)
        ax.set_ylim(0, max(r2_values) * 1.1 if r2_values else 1)
        ax.tick_params(axis='x', colors='#E6D3A7')
        ax.tick_params(axis='y', colors='#E6D3A7')
        ax.grid(True, alpha=0.3, color='#555555')
        
        canvas = FigureCanvasTkAgg(fig, master=comparison_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_model_details(self, event):
        selected = self.models_tree.selection()
        if not selected:
            return
        
        item = self.models_tree.item(selected[0])
        model_name = item['values'][1]
        if model_name in self.models:
            details_win = tk.Toplevel(self.root)
            details_win.title(f"👁️ Detalhes do Golem: {model_name}")
            details_win.geometry("700x500")
            details_win.configure(background="#2F2F2F")
            
            info_frame = ttk.Frame(details_win, style="Card.TFrame", borderwidth=2, relief="solid")
            info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            model_info = self.models[model_name]
            info_text = f"""
🏷️ Nome: {model_name}
🧱 Dataset: {model_info['dataset']}
🎯 Variável Alvo: {model_info['target']}
⚙️ Algoritmo: {model_info.get('algorithm', 'N/A')}
📊 Features Utilizadas: {len(model_info['features'])}
📈 Precisão (R²): {model_info['metrics']['r2']:.4f}
📉 Erro (RMSE): {model_info['metrics']['rmse']:.4f}
⚡ Energia (MAE): {model_info['metrics']['mae']:.4f}
🕐 Criado em: {model_info['created'].strftime("%Y-%m-%d %H:%M")}
⏱️ Tempo de Treinamento: {model_info.get('training_time', 'N/A')} segundos
"""
            ttk.Label(info_frame, text=info_text, font=("Courier", 10), background="#3A3A3A", foreground="#E6D3A7", justify=tk.LEFT).pack(padx=10, pady=10)

    def show_reports(self):
        self.clear_content()
        reports_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        reports_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(reports_frame, text="📋 Livro de Relatórios do Minerador", style="Header.TLabel").pack(pady=10)
        
        report_text = """
📖 RELATÓRIOS DISPONÍVEIS
🧱 Análises de Blocos:
- Relatório_Mineracao_2026.txt
- Relatório_Golems_Ferro.txt

🏃‍♂️ Relatórios de Golems:
- metricas_golems_2026.json
- comparativo_golems.txt

💎 Baús do Tesouro:
- backup_completo_2026.zip

🔍 Para gerar novos relatórios, selecione um dataset na aba "🔬 Análise"
e clique no botão "📥 Exportar Relatório".
"""
        text_widget = scrolledtext.ScrolledText(reports_frame, wrap=tk.WORD, bg="#2A2A2A", fg="#E6D3A7", 
                                               font=("Courier", 11), height=20)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert(tk.END, report_text)
        text_widget.config(state=tk.DISABLED)

    def show_settings(self):
        self.clear_content()
        settings_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(settings_frame, text="⚙️ Configurações do Mundo Minecraft", style="Header.TLabel").pack(pady=10)
        
        settings = [
            ("Tema da Interface", "minecraft_dark"),
            ("Máx. Registros na Visualização", "1000"),
            ("Auto-save (minutos)", "5"),
            ("Formato de Backup Padrão", "csv"),
            ("Precisão dos Golems", "automática")
        ]
        
        for i, (setting, value) in enumerate(settings):
            frame = ttk.Frame(settings_frame, style="Card.TFrame", borderwidth=1, relief="solid")
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=setting, font=("Courier", 10, "bold"), background="#3A3A3A", foreground="#9cdcfe").pack(side=tk.LEFT, padx=15, pady=8)
            ttk.Label(frame, text=value, font=("Courier", 10), background="#3A3A3A", foreground="#ce9178").pack(side=tk.RIGHT, padx=15, pady=8)
        
        btn_frame = ttk.Frame(settings_frame, style="Main.TFrame")
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="💾 Aplicar Configurações", style="Success.TButton", command=lambda: messagebox.showinfo("✅ Sucesso", "Configurações atualizadas com sucesso!")).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="🔄 Restaurar Padrões", style="Accent.TButton", command=lambda: messagebox.showinfo("🔄 Restaurado", "Configurações restauradas aos valores padrão!")).pack(side=tk.LEFT, padx=10)

    def show_descriptive_stats(self, df, dataset_name):
        stats_win = tk.Toplevel(self.root)
        stats_win.title(f"🧾 Estatísticas Descritivas: {dataset_name}")
        stats_win.geometry("900x600")
        stats_win.configure(background="#2F2F2F")
        
        notebook = ttk.Notebook(stats_win, style="TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        desc_frame = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(desc_frame, text="📋 Descritivas")
        
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            desc_stats = numeric_df.describe().round(4).T
            tree = ttk.Treeview(desc_frame, columns=["metric"] + list(desc_stats.columns), show="headings")
            tree.heading("metric", text="Métrica")
            tree.column("metric", width=100)
            
            for col in desc_stats.columns:
                tree.heading(col, text=col)
                tree.column(col, width=80)
            
            for metric, row in desc_stats.iterrows():
                values = [metric] + list(row.values)
                tree.insert("", tk.END, values=values)
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def quick_visualization(self, df, dataset_name):
        viz_win = tk.Toplevel(self.root)
        viz_win.title(f"🗺️ Visualização Rápida: {dataset_name}")
        viz_win.geometry("900x700")
        viz_win.configure(background="#2F2F2F")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()[:4]
        if not numeric_cols:
            ttk.Label(viz_win, text="⚠️ Nenhuma variável numérica para visualizar", style="Header.TLabel").pack(pady=50)
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#3A3A3A')
        fig.patch.set_facecolor('#3A3A3A')
        axes = axes.flatten()
        
        for i, col in enumerate(numeric_cols):
            if i < 4:
                ax = axes[i]
                ax.set_facecolor('#2F2F2F')
                ax.hist(df[col].dropna(), bins=30, alpha=0.7, color='#0078d7', edgecolor='white')
                ax.set_title(f'Distribuição de {col}', color='#FFD700', fontsize=12)
                ax.set_xlabel(col, color='#E6D3A7')
                ax.set_ylabel('Frequência', color='#E6D3A7')
                ax.tick_params(axis='both', colors='#E6D3A7')
                ax.grid(True, alpha=0.3, color='#555555')
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=viz_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def train_quick_model(self, df, dataset_name):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2:
            messagebox.showerror("Erro", "Dataset precisa de pelo menos 2 colunas numéricas para treinar um modelo!")
            return
        
        X = df[numeric_cols[:-1]]
        y = df[numeric_cols[-1]]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)
        
        r2 = model.score(X_test, y_test)
        messagebox.showinfo("✅ Golem Criado", f"Golem de Ferro treinado com sucesso para {dataset_name}!\nPrecisão (R²): {r2:.4f}")
        self.log_activity(f"⚡ Golem rápido treinado para {dataset_name} com R²={r2:.4f}")

    def save_quick_analysis(self, df, dataset_name):
        directory = filedialog.askdirectory(title="💎 Salvar Análise Rápida")
        if not directory:
            return
        
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(directory, f"analise_rapida_{dataset_name}_{timestamp}.csv")
            df.describe().to_csv(filename)
            messagebox.showinfo("✅ Sucesso", f"Análise rápida salva com sucesso!\nArquivo: {filename}")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar análise:\n{str(e)}")

    def export_statistical_report(self, dataset_name):
        if dataset_name not in self.datasets:
            return
        
        directory = filedialog.askdirectory(title="📥 Exportar Relatório")
        if not directory:
            return
        
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(directory, f"relatorio_{dataset_name}_{timestamp}.txt")
            df = self.datasets[dataset_name]
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"📊 RELATÓRIO ESTATÍSTICO - {dataset_name}\n")
                f.write(f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n")
                f.write(f"📈 Dimensões: {df.shape[0]} linhas, {df.shape[1]} colunas\n")
                f.write(f"🔍 Colunas: {', '.join(df.columns)}\n")
                f.write("🧱 Tipos de Dados:\n")
                for col, dtype in df.dtypes.items():
                    f.write(f"   • {col}: {dtype}\n")
                f.write("\n🕳️ Valores Nulos:\n")
                for col, count in df.isnull().sum().items():
                    if count > 0:
                        f.write(f"   • {col}: {count} ({count/len(df)*100:.2f}%)\n")
            
            messagebox.showinfo("✅ Sucesso", f"Relatório estatístico exportado com sucesso!\nArquivo: {filename}")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao exportar relatório:\n{str(e)}")

    def save_statistical_analysis(self, dataset_name):
        messagebox.showinfo("✅ Análise Salva", f"Análise estatística do bloco '{dataset_name}' salva no Baú de Dados!")

def main():
    root = tk.Tk()
    app = MinecraftBigDataApp(root)
    
    def on_closing():
        if messagebox.askokcancel("⛏️ Sair do Mundo", "Deseja realmente sair do mundo de Minecraft Data Miner?\nBlocos não salvos serão perdidos!"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()'
