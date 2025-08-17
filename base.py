import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import os

class InsumoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Produtos e Preparos")
        self.root.geometry("800x550")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # ===== ABA INSUMOS =====
        self.frame_insumos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_insumos, text="Insumos")

        self.insumos = []
        self._montar_aba_insumos()

        # ===== ABA PREPAROS =====
        self.frame_preparos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_preparos, text="Preparos")

        self.preparos = []
        self._montar_aba_preparos()

        self.carregar_csv_automatico()

    # ---------- Monta Aba Insumos ----------
    def _montar_aba_insumos(self):
        # Campos de entrada
        ttk.Label(self.frame_insumos, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = ttk.Entry(self.frame_insumos, width=30)
        self.nome_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(self.frame_insumos, text="Qtd:").grid(row=1, column=0, sticky="w")
        self.qtd_entry = ttk.Entry(self.frame_insumos, width=10)
        self.qtd_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(self.frame_insumos, text="Unidade:").grid(row=2, column=0, sticky="w")
        self.unidade_combo = ttk.Combobox(self.frame_insumos, values=["kg", "g", "L", "ml", "unid"], width=10)
        self.unidade_combo.set("kg")
        self.unidade_combo.grid(row=2, column=1, sticky="w")

        ttk.Label(self.frame_insumos, text="Valor R$:").grid(row=3, column=0, sticky="w")
        self.valor_entry = ttk.Entry(self.frame_insumos, width=15)
        self.valor_entry.grid(row=3, column=1, sticky="w")

        ttk.Label(self.frame_insumos, text="Validade (dd/mm/aaaa):").grid(row=0, column=2, sticky="w")
        self.validade_entry = ttk.Entry(self.frame_insumos, width=15)
        self.validade_entry.grid(row=0, column=3, sticky="w")

        ttk.Label(self.frame_insumos, text="Categoria:").grid(row=1, column=2, sticky="w")
        self.categoria_combo = ttk.Combobox(self.frame_insumos,
            values=["Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro", 
                    "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"],
            width=15
        )
        self.categoria_combo.set("Cereal")
        self.categoria_combo.grid(row=1, column=3, sticky="w")

        ttk.Label(self.frame_insumos, text="Fornecedor:").grid(row=2, column=2, sticky="w")
        self.fornecedor_entry = ttk.Entry(self.frame_insumos, width=30)
        self.fornecedor_entry.grid(row=2, column=3, sticky="w")

        # Botões
        botoes = ttk.Frame(self.frame_insumos)
        botoes.grid(row=4, column=0, columnspan=4, pady=5)
        ttk.Button(botoes, text="Adicionar", command=self.adicionar_insumo).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Editar", command=self.editar_insumo).grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="Excluir", command=self.excluir_insumo).grid(row=0, column=2, padx=5)
        ttk.Button(botoes, text="Salvar CSV", command=self.salvar_csv_insumos).grid(row=0, column=3, padx=5)
        ttk.Button(botoes, text="Abrir CSV", command=self.abrir_csv_insumos).grid(row=0, column=4, padx=5)

        # Filtros
        filtros = ttk.Frame(self.frame_insumos)
        filtros.grid(row=5, column=0, columnspan=4, pady=5, sticky="w")
        ttk.Label(filtros, text="Filtrar categoria:").grid(row=0, column=0)
        self.filtro_categoria = ttk.Combobox(filtros, 
            values=["Todas","Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro",
                    "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"], width=15)
        self.filtro_categoria.set("Todas")
        self.filtro_categoria.grid(row=0, column=1)

        ttk.Label(filtros, text="Validade até (dd/mm/aaaa):").grid(row=0, column=2)
        self.filtro_validade = ttk.Entry(filtros, width=15)
        self.filtro_validade.grid(row=0, column=3)
        ttk.Button(filtros, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=0, column=4, padx=10)

        # Tabela
        colunas = ("Nome", "Quantidade", "Unidade", "Valor", "Validade", "Categoria", "Fornecedor")
        self.tree = ttk.Treeview(self.frame_insumos, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=6, column=0, columnspan=4, pady=10)
        self.carregar_csv_automatico()

    # ---------- Monta Aba Preparos ----------
    def _montar_aba_preparos(self):
        filtros_preparos = ttk.Frame(self.frame_preparos, padding="10")
        filtros_preparos.grid(row=0, column=0, sticky="w")

        ttk.Label(filtros_preparos,text="Cardápio:").grid(row=0, column=0)
        self.nome_preparo= ttk.Combobox(filtros_preparos, values=["Escondidinho","Empadão","Lazanha","Bolo de Pote"], width=13)
        self.nome_preparo.grid(row=0, column=1)
        self.nome_preparo.set("Escondidinho")

        ttk.Label(filtros_preparos,text="  Gramatura:").grid(row=0,column=2)
        self.gramatura = ttk.Combobox(filtros_preparos,values=["250","500","1000"],width=5)
        self.gramatura.grid(row=0,column=3)
        self.gramatura.set("250")

        ttk.Label(filtros_preparos, text="  Tempo Preparo(min):").grid(row=0, column=4)
        self.t_preparo = ttk.Entry(filtros_preparos, width=5)
        self.t_preparo.grid(row=0, column=5)

        ttk.Label(filtros_preparos, text="  Tempo Forno(min):").grid(row=0, column=6)
        self.t_forno = ttk.Entry(filtros_preparos, width=5)
        self.t_forno.grid(row=0, column=7)

        ttk.Label(filtros_preparos, text="  Ingredientes :").grid(row=1, column=0, sticky="W",padx=5)

        entrada_ingredientes = ttk.Frame(self.frame_preparos, padding="10")
        entrada_ingredientes.grid(row=1, column=0)

        ttk.Label(entrada_ingredientes, text="Nome:").grid(row=0, column=0)
        self.nome_entry_p = ttk.Entry(entrada_ingredientes, width=20)
        self.nome_entry_p.grid(row=0, column=1)

        ttk.Label(entrada_ingredientes, text=" Qtd:").grid(row=0, column=2)
        self.qtd_entry_p = ttk.Entry(entrada_ingredientes, width=5)
        self.qtd_entry_p.grid(row=0, column=3)

        ttk.Label(entrada_ingredientes, text=" Peso/Unidade:").grid(row=0, column=4)
        self.peso_uni = ttk.Entry(entrada_ingredientes, width=5)
        self.peso_uni.grid(row=0, column=5)

        ttk.Label(entrada_ingredientes, text=":").grid(row=0, column=6)
        self.unidade_combo_p = ttk.Combobox(entrada_ingredientes, values=["kg", "g", "L", "ml", "unid"], width=5)
        self.unidade_combo_p.grid(row=0, column=7)
        self.unidade_combo_p.set("kg")

        colunas = ["Nome", "Quantidade", "Peso por Unidade","Unidade"]
        self.tree_preparos = ttk.Treeview(self.frame_preparos, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tree_preparos.heading(col, text=col)
            self.tree_preparos.column(col, width=100)
        self.tree_preparos.grid(row=2, column=0, columnspan=4, pady=10)

        botoes = ttk.Frame(self.frame_preparos)
        botoes.grid(row=3, column=0, columnspan=4, pady=5)
        ttk.Button(botoes, text="Adicionar", command=self.adicionar_preparo).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Editar", command=self.editar_preparo).grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="Excluir", command=self.excluir_preparo).grid(row=0, column=2, padx=5)
        ttk.Button(botoes, text="Salvar CSV", command=self.salvar_csv_preparos).grid(row=0, column=3, padx=5)
        ttk.Button(botoes, text="Abrir CSV", command=self.abrir_csv_preparos).grid(row=0, column=4, padx=5)

    # ---------- Funções Insumos ----------
    def adicionar_insumo(self):
        nome = self.nome_entry.get().strip()
        qtd = self.qtd_entry.get().strip()
        unidade = self.unidade_combo.get()
        valor = self.valor_entry.get().strip()
        validade = self.validade_entry.get().strip()
        categoria = self.categoria_combo.get()
        fornecedor = self.fornecedor_entry.get().strip()

        if not nome or not qtd or not valor or not validade or not fornecedor:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
            return

        try:
            qtd = float(qtd)
            valor = float(valor)
            datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade/valor inválidos ou data errada!")
            return

        insumo = (nome, qtd, unidade, valor, validade, categoria, fornecedor)
        self.tree.insert("", "end", values=insumo)
        self._atualizar_lista_insumos()

    def editar_insumo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Editar", "Selecione um item para editar.")
            return
        valores = self.tree.item(selecionado)["values"]

        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, valores[0])
        self.qtd_entry.delete(0, tk.END)
        self.qtd_entry.insert(0, valores[1])
        self.unidade_combo.set(valores[2])
        self.valor_entry.delete(0, tk.END)
        self.valor_entry.insert(0, valores[3])
        self.validade_entry.delete(0, tk.END)
        self.validade_entry.insert(0, valores[4])
        self.categoria_combo.set(valores[5])
        self.fornecedor_entry.delete(0, tk.END)
        self.fornecedor_entry.insert(0, valores[6])

        self.tree.delete(selecionado)
        self._atualizar_lista_insumos()

    def excluir_insumo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Excluir", "Selecione um item para excluir.")
            return
        self.tree.delete(selecionado)
        self._atualizar_lista_insumos()

    def salvar_csv_insumos(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Nome", "Quantidade", "Unidade", "Valor", "Validade", "Categoria", "Fornecedor"])
            for row_id in self.tree.get_children():
                escritor.writerow(self.tree.item(row_id)["values"])
        messagebox.showinfo("Sucesso", f"Dados salvos em {arquivo}")
        self._salvar_caminho_csv(arquivo)

    def abrir_csv_insumos(self):
        arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        self._carregar_csv(self.tree, arquivo, 7)
        self._salvar_caminho_csv(arquivo)

    # ---------- Funções Preparos ----------
    def adicionar_preparo(self):
        cardapio = self.nome_preparo.get().strip()
        nome = self.nome_entry_p.get().strip()
        qtd = self.qtd_entry_p.get().strip()
        peso_uni= self.peso_uni.get().strip()
        unidade = self.unidade_combo_p.get().strip()
        gramatura = self.gramatura.get().strip()
        tempo_preparo = self.t_preparo.get().strip()
        tempo_forno = self.t_forno.get().strip()

        if not cardapio or not nome or not qtd or not tempo_preparo or not tempo_forno :
            messagebox.showwarning("Atenção", "Preecha todos os campos obrigatórios")
            return
        try:
            qtd = float(qtd)
            gramatura = int(gramatura)
            tempo_forno = float(tempo_forno)
            tempo_preparo = float(tempo_preparo)
        except ValueError :
            messagebox.showerror("Erro", "Quantidade inválida !")
            return
        cadastro_preparo = (nome, qtd, peso_uni, unidade)
        self.tree_preparos.insert("","end", values=cadastro_preparo)
        self.limpar_campos_preparos()

    def limpar_campos_preparos(self):
        self.nome_entry_p.delete(0, tk.END)
        self.qtd_entry_p.delete(0, tk.END)
        self.unidade_combo_p.set("kg")
        self.t_forno.delete(0, tk.END)
        self.t_preparo.delete(0, tk.END)
        self.peso_uni.delete(0,tk.END)

        # Salva os dados atuais da tabela na lista
        self.cad_preparo = []
        for item_id in self.tree.get_children():
            valores = self.tree.item(item_id)["values"]
            self.cad_preparo.append(valores)


    def editar_preparo(self):
        pass

    def excluir_preparo(self):
        pass

    def salvar_csv_preparos(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Nome do Preparo", "Ingredientes", "Modo de Preparo", "Tempo", "Data", "Observações"])
            for row_id in self.tree_preparos.get_children():
                escritor.writerow(self.tree_preparos.item(row_id)["values"])
        messagebox.showinfo("Sucesso", f"Preparos salvos em {arquivo}")

    def abrir_csv_preparos(self):
        arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        self._carregar_csv(self.tree_preparos, arquivo, 6)

    # ---------- Utilitários ----------
    def _carregar_csv(self, tree, arquivo, num_colunas):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor)
                tree.delete(*tree.get_children())
                for linha in leitor:
                    if len(linha) == num_colunas:
                        tree.insert("", "end", values=linha)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def _salvar_caminho_csv(self, caminho):
        try:
            pasta_templates = os.path.join(os.path.dirname(__file__),"templates")
            os.makedirs(pasta_templates, exist_ok=True)
            caminho_arquivo = os.path.join(pasta_templates,"ultimo_arquivo.txt")
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(caminho)
        except Exception as e:
            print("Erro ao salvar caminho do CSV:", e)

    def carregar_csv_automatico(self):
        pasta_templates = os.path.join(os.path.dirname(__file__),"templates")
        os.makedirs(pasta_templates, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_templates,"ultimo_arquivo.txt")
            
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                caminho = f.read().strip()
                if caminho.endswith(".csv"):
                    self._carregar_csv(self.tree, caminho, 7)

    def _atualizar_lista_insumos(self):
        self.insumos = [self.tree.item(i)["values"] for i in self.tree.get_children()]

    def aplicar_filtro(self):
        categoria_filtro = self.filtro_categoria.get()
        validade_filtro = self.filtro_validade.get().strip()

        self.tree.delete(*self.tree.get_children())
        for insumo in self.insumos:
            nome, qtd, unidade, valor, validade, categoria, fornecedor = insumo
            if categoria_filtro != "Todas" and categoria != categoria_filtro:
                continue
            if validade_filtro:
                try:
                    data_limite = datetime.strptime(validade_filtro, "%d/%m/%Y")
                    data_insumo = datetime.strptime(validade, "%d/%m/%Y")
                    if data_insumo > data_limite:
                        continue
                except ValueError:
                    messagebox.showerror("Erro", "Data de validade inválida para filtro.")
                    return
            self.tree.insert("", "end", values=insumo)

if __name__ == "__main__":
    root = tk.Tk()
    app = InsumoGUI(root)
    root.mainloop()
