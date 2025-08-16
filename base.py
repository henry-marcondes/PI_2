import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import os

class InsumoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Insumos de Cozinha")

        self.insumos = []

        # Frame de entrada
        entrada = ttk.Frame(root, padding="10")
        entrada.grid(row=0, column=0, sticky="W")

        # Campos
        ttk.Label(entrada, text="Nome:").grid(row=0, column=0)
        self.nome_entry = ttk.Entry(entrada, width=30)
        self.nome_entry.grid(row=0, column=1)

        ttk.Label(entrada, text="Qtd:").grid(row=1, column=0)
        self.qtd_entry = ttk.Entry(entrada, width=10)
        self.qtd_entry.grid(row=1, column=1)

        ttk.Label(entrada, text="Unidade:").grid(row=2, column=0)
        self.unidade_combo = ttk.Combobox(entrada, values=["kg", "g", "L", "ml", "unid"], width=10)
        self.unidade_combo.grid(row=2, column=1)
        self.unidade_combo.set("kg")

        ttk.Label(entrada, text="Valor: R$").grid(row=3, column=0)
        self.valor_entry = ttk.Entry(entrada, width=15)
        self.valor_entry.grid(row=3, column=1)

        ttk.Label(entrada, text="Validade (dd/mm/aaaa):").grid(row=0, column=2)
        self.validade_entry = ttk.Entry(entrada, width=15)
        self.validade_entry.grid(row=0, column=3)

        ttk.Label(entrada, text="Categoria:").grid(row=1, column=2)
        self.categoria_combo = ttk.Combobox(entrada, values=["Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro", "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"], height=12,width=15)
        self.categoria_combo.grid(row=1, column=3)
        self.categoria_combo.set("Verdura")

        ttk.Label(entrada, text="Fornecedor:").grid(row=2, column=2)
        self.fornecedor_entry = ttk.Entry(entrada, width=30)
        self.fornecedor_entry.grid(row=2, column=3)

        # Botões principais
        botoes = ttk.Frame(root, padding="10")
        botoes.grid(row=1, column=0, sticky="W")

        ttk.Button(botoes, text="Adicionar", command=self.adicionar_insumo).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Editar", command=self.editar_insumo).grid(row=0, column=1, padx=5)
        ttk.Button(botoes, text="Excluir", command=self.excluir_insumo).grid(row=0, column=2, padx=5)
        ttk.Button(botoes, text="Salvar CSV", command=self.salvar_csv).grid(row=0, column=3, padx=5)
        ttk.Button(botoes, text="Abrir CSV", command=self.abrir_csv).grid(row=0, column=4, padx=5)


        # Filtros
        filtros = ttk.Frame(root, padding="10")
        filtros.grid(row=2, column=0, sticky="W")

        ttk.Label(filtros, text="Filtrar por categoria:").grid(row=0, column=0)
        self.filtro_categoria = ttk.Combobox(filtros, values=["Todas","Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro", "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"], height=12,width=15)
        self.filtro_categoria.grid(row=0, column=1)
        self.filtro_categoria.set("Todas")

        ttk.Label(filtros, text="Validade até (dd/mm/aaaa):").grid(row=0, column=2)
        self.filtro_validade = ttk.Entry(filtros, width=15)
        self.filtro_validade.grid(row=0, column=3)

        ttk.Button(filtros, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=0, column=4, padx=10)

        # Tabela
        colunas = ("Nome", "Quantidade", "Unidade", "Valor", "Validade", "Categoria", "Fornecedor")
        self.tree = ttk.Treeview(root, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=3, column=0, padx=10, pady=10)
        self.carregar_csv_automatico()

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
            messagebox.showerror("Erro", "Quantidade inválida ou data em formato errado!")
            return

        insumo = (nome, qtd, unidade, valor, validade, categoria, fornecedor)
        self.tree.insert("", "end", values=insumo)
        self.limpar_campos()

    def editar_insumo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Editar", "Selecione um item para editar.")
            return

        item = self.tree.item(selecionado)
        valores = item["values"]

        # Preenche os campos
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, valores[0])
        self.qtd_entry.delete(0, tk.END)
        self.qtd_entry.insert(0, valores[1])
        self.unidade_combo.set(valores[2])
        self.valor_entry.delete(0, tk.END)
        self.valor_entry.insert(0,valores[3])
        self.validade_entry.delete(0, tk.END)
        self.validade_entry.insert(0, valores[4])
        self.categoria_combo.set(valores[5])
        self.fornecedor_entry.delete(0, tk.END)
        self.fornecedor_entry.insert(0, valores[6])

        # Remove da lista temporariamente
        self.tree.delete(selecionado)

    def excluir_insumo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Excluir", "Selecione um item para excluir.")
            return
        self.tree.delete(selecionado)

    def salvar_caminho_csv(self, caminho):
        try:
            pasta_templates = os.path.join(os.path.dirname(__file__),"templates")
            os.makedirs(pasta_templates, exist_ok=True)
            caminho_arquivo = os.path.join(pasta_templates,"ultimo_arquivo.txt")
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(caminho)
        except Exception as e:
            print("Erro ao salvar caminho do CSV:", e)

    def carregar_csv_automatico(self):
        try:
            pasta_templates = os.path.join(os.path.dirname(__file__),"templates")
            os.makedirs(pasta_templates, exist_ok=True)
            caminho_arquivo = os.path.join(pasta_templates,"ultimo_arquivo.txt")
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                caminho = f.read().strip()
            if caminho and caminho.endswith(".csv"):
                self.abrir_csv_automatico(caminho)
        except FileNotFoundError:
            pass  # Se não existir, ignora

    def abrir_csv_automatico(self, arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor) # pula cabeçalho
                self.tree.delete(*self.tree.get_children())
                self.insumos.clear()

                for linha in leitor:
                    if len(linha) != 7:
                        continue
                    nome, qtd, unidade, valor, validade, categoria, fornecedor = linha
                    try:
                        qtd = float(qtd) # transforma string em float
                        valor =  float(valor)
                    except ValueError:
                        qtd = 0
                        valor = 0
                    item = (nome, qtd, unidade, valor, validade,categoria, fornecedor)
                    self.tree.insert("","end", values=item)
                    self.insumos.append(item)
            print(f"CSV carregado automaticamente: {arquivo}")
        except Exception as e:
            print("Erro ao abrir CSV automático: {e}")

    def salvar_csv(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return

        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Nome", "Quantidade", "Unidade", "Valor", "Validade", "Categoria", "Fornecedor"])
            for row_id in self.tree.get_children():
                valores = self.tree.item(row_id)["values"]
                escritor.writerow(valores)

        messagebox.showinfo("Sucesso", f"Dados salvos em {arquivo}")
        self.salvar_caminho_csv(arquivo)

    def abrir_csv(self):
        arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return

        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor)  # Pular o cabeçalho
                self.tree.delete(*self.tree.get_children())  # Limpa tabela
                self.insumos.clear()

                for linha in leitor:
                    if len(linha) != 7:
                        continue  # ignora linhas com dados incompletos
                    nome, qtd, unidade, valor, validade, categoria, fornecedor = linha
                    try:
                        qtd = float(qtd)
                    except ValueError:
                        qtd = 0
                    item = (nome, qtd, unidade, valor, validade, categoria, fornecedor)
                    self.tree.insert("", "end", values=item)
                    self.insumos.append(item)

            messagebox.showinfo("Sucesso", f"Arquivo carregado: {arquivo}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o arquivo:\n{e}")
        self.salvar_caminho_csv(arquivo)

    def aplicar_filtro(self):
        categoria_filtro = self.filtro_categoria.get()
        validade_filtro = self.filtro_validade.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

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
                    messagebox.showerror("Erro", "Data de validade para filtro inválida.")
                    return

            self.tree.insert("", "end", values=insumo)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.qtd_entry.delete(0, tk.END)
        self.unidade_combo.set("kg")
        self.valor_entry.delete(0, tk.END)
        self.validade_entry.delete(0, tk.END)
        self.categoria_combo.set("Cereal")
        self.fornecedor_entry.delete(0, tk.END)

        # Salva os dados atuais da tabela na lista
        self.insumos = []
        for item_id in self.tree.get_children():
            valores = self.tree.item(item_id)["values"]
            self.insumos.append(valores)

if __name__ == "__main__":
    root = tk.Tk()
    app = InsumoGUI(root)
    root.mainloop()
