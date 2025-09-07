# base.py
import tkinter as tk
from tkinter import ttk, messagebox
from model_bd import listar_insumos, adicionar_insumo, excluir_insumo, listar_fornecedores, adicionar_compra, listar_cardapio
from datetime import datetime

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque - MySQL")
        self.root.geometry("650x400")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # ===== ABA INSUMOS =====
        self.frame_insumos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_insumos, text="Insumos")

        self.insumos = []
        self._montar_aba_insumos()

        #===== ABA COMPRAS =====
        self.frame_compras = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_compras, text="Compras")
        self._montar_aba_compras()

        # ===== ABA PREPAROS =====
        self.frame_preparos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_preparos, text="Preparos")
        self._montar_aba_preparos()


        # ===== ABA RELATORIOS =====
        self.frame_preparos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_preparos, text="Relatórios")

        #===== ABA Fornecedores =====
        self.frame_fornecedores = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_fornecedores, text="Fornecedores")
        self._montar_aba_fornecedores()

        # ========= Fim das extrutura de Frame =========


    def _montar_aba_compras(self):
        ttk.Label(self.frame_compras, text="Insumo:").grid(row=0, column=0, sticky="w")
        self.insumo_combo = ttk.Combobox(self.frame_compras, width=25, state="readonly")
        self.insumo_combo.grid(row=0, column=1, sticky="w")

        ttk.Label(self.frame_compras, text="Fornecedor:").grid(row=1, column=0, sticky="w")
        self.fornecedor_combo = ttk.Combobox(self.frame_compras, width=25, state="readonly")
        self.fornecedor_combo.grid(row=1, column=1, sticky="w")

        ttk.Label(self.frame_compras, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.qtd_entry = ttk.Entry(self.frame_compras, width=10)
        self.qtd_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(self.frame_compras, text="Unidade:").grid(row=2, column=2, sticky="w")
        self.unidade_combo = ttk.Combobox(self.frame_compras, values=["kg","L","g","ml","unid"], width=8)
        self.unidade_combo.grid(row=2, column=3, sticky="w")

        ttk.Label(self.frame_compras, text="Valor:").grid(row=3, column=0, sticky="w")
        self.valor_entry = ttk.Entry(self.frame_compras, width=10)
        self.valor_entry.grid(row=3, column=1, sticky="w")

        ttk.Label(self.frame_compras, text="Validade:").grid(row=3, column=2, sticky="w")
        self.validade_entry = ttk.Entry(self.frame_compras, width=12)
        self.validade_entry.insert(0, "YYYY-MM-DD")
        self.validade_entry.grid(row=3, column=3, sticky="w")

        tk.Button(self.frame_compras, text="Lançar Compra", command=self.lancar_compra).grid(row=4, column=0, pady=10)

        self.carregar_combos_compras()

    def _montar_aba_preparos(self):
        self.tree = ttk.Treeview(self.frame_preparos,columns=("id","nome","gramatura"), show="headings")
        self.tree.heading("id",text="COD")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("gramatura", text="Gramatura")
        self.tree.grid(row=0, column=0, columnspan=5, pady=5)
        self.carregar_dados_cardapio()

    def carregar_combos_compras(self):
        insumos = listar_insumos()
        self.insumos_dict = {f"{i['nome']} ({i['categoria']})": i['idInsumos'] for i in insumos}
        self.insumo_combo['values'] = list(self.insumos_dict.keys())

        fornecedores = listar_fornecedores()
        self.fornecedores_dict = {f"{f['nome']}": f['idFornecedor'] for f in fornecedores}
        self.fornecedor_combo['values'] = list(self.fornecedores_dict.keys())

    def lancar_compra(self):
        insumo_nome = self.insumo_combo.get()
        fornecedor_nome = self.fornecedor_combo.get()

        if insumo_nome not in self.insumos_dict:
            messagebox.showerror("Erro", "Insumo não cadastrado no sistema!")
            return
        if fornecedor_nome not in self.fornecedores_dict:
            messagebox.showerror("Erro", "Fornecedor não cadastrado no sistema!")
            return

        try:
            id_insumo = self.insumos_dict[insumo_nome]
            fornecedor_id = self.fornecedores_dict[fornecedor_nome]
            quantidade = float(self.qtd_entry.get())
            unidade = self.unidade_combo.get()
            valor = float(self.valor_entry.get())
            validade = self.validade_entry.get()

            menor_parte = quantidade  # Aqui você pode fazer conversão automática
            valor_medio = quantidade / valor if valor != 0 else 0

            adicionar_compra(id_insumo, quantidade, unidade, valor, validade, fornecedor_id, menor_parte, valor_medio)
            messagebox.showinfo("Sucesso", "Compra lançada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao lançar compra: {e}")


        # ==== Montar a Aba de Insumos =====
    def _montar_aba_insumos(self):
        ttk.Label(self.frame_insumos, text="Nome:").grid(row=0, column=0)
        self.nome_entry = ttk.Entry(self.frame_insumos, width=30)
        self.nome_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(self.frame_insumos, text="Categoria:").grid(row=0, column=2, sticky="w")
        self.categoria_combo = ttk.Combobox(self.frame_insumos,
                values=["Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro", 
                        "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"],
                width=15
            )
        self.categoria_combo.set("Cereal")
        self.categoria_combo.grid(row=0, column=3, sticky="w")

        tk.Button(self.frame_insumos, text="Adicionar", command=self.adicionar_item).grid(row=2, column=0, pady=5)
        tk.Button(self.frame_insumos, text="Excluir", command=self.excluir_item).grid(row=2, column=1)
        tk.Button(self.frame_insumos, text="Atualizar Lista", command=self.carregar_dados_insumo).grid(row=2, column=2)

        self.tree = ttk.Treeview(self.frame_insumos, columns=("id", "nome", "categoria"), show="headings")
        self.tree.heading("id", text="COD")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria", text="Categoria")
        self.tree.grid(row=3, column=0, columnspan=8, pady=10)
        self.carregar_dados_insumo()

    
    def carregar_dados_cardapio(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for cardapio in listar_cardapio():
            self.tree.insert("","end", values=(
                cardapio["id_cardapio"], cardapio["Nome"],cardapio["gramatura"]))

    def carregar_dados_insumo(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for insumo in listar_insumos():
            self.tree.insert("", "end", values=(
                insumo["idInsumos"], insumo["nome"], insumo["categoria"]))

    def adicionar_item(self):
        nome = self.nome_entry.get().strip()  
        categoria = self.categoria_combo.get().strip()
       

        if not nome  or not categoria:
            messagebox.showwarning("Aviso", "Preencha pelo menos Nome, Quantidade e Unidade.")
            return

        try:
            adicionar_insumo(nome,categoria)
            self.carregar_dados()
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar: {e}")

    def excluir_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return

        item = self.tree.item(selecionado)
        id_insumo = item["values"][0]

        try:
            excluir_insumo(id_insumo)
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.categoria_combo.delete(0, tk.END)
        
    def _montar_aba_fornecedores(self):

        # Labels e Entrys para Fornecedor
        ttk.Label(self.frame_fornecedores, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = ttk.Entry(self.frame_fornecedores)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_fornecedores, text="CNPJ:").grid(row=1, column=0, padx=5, pady=5)
        cpf_entry = ttk.Entry(self.frame_fornecedores)
        cpf_entry.grid(row=1, column=1, padx=5, pady=5)

        # Endereço
        ttk.Label(self.frame_fornecedores, text="Rua/Av:").grid(row=2, column=0, padx=5, pady=5)
        rua_entry = ttk.Entry(self.frame_fornecedores)
        rua_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame_fornecedores, text="Número:").grid(row=3, column=0, padx=5, pady=5)
        numero_entry = ttk.Entry(self.frame_fornecedores)
        numero_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame_fornecedores, text="Complemento:").grid(row=4, column=0, padx=5, pady=5)
        complemento_entry = ttk.Entry(self.frame_fornecedores)
        complemento_entry.insert(0,'nenhum')
        complemento_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame_fornecedores, text="Tipo:").grid(row=5, column=0, padx=5, pady=5)
        tipo_combo = ttk.Combobox(self.frame_fornecedores, values=["RESIDENCIAL", "COMERCIAL"])
        tipo_combo.grid(row=5, column=1, padx=5, pady=5)

        # Telefone
        ttk.Label(self.frame_fornecedores, text="Telefone:").grid(row=6, column=0, padx=5, pady=5)
        fone_entry = ttk.Entry(self.frame_fornecedores)
        fone_entry.grid(row=6, column=1, padx=5, pady=5)

        # Botão de cadastro
        def cadastrar_fornecedor():
            nome = nome_entry.get()
            CNPJ = cpf_entry.get()
            rua = rua_entry.get()
            numero = numero_entry.get()
            complemento = complemento_entry.get()
            tipo = tipo_combo.get()
            telefone = fone_entry.get()

            from model_bd import inserir_fornecedor
            inserir_fornecedor(nome, CNPJ, rua, numero, complemento, tipo, telefone)

            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")

        ttk.Button(self.frame_fornecedores, text="Cadastrar", command=cadastrar_fornecedor).grid(row=9, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
