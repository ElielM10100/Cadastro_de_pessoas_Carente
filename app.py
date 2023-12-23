import csv
import os
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from ttkthemes import ThemedTk

def cadastrar_pessoa():
    nome = simpledialog.askstring("Cadastro", "Digite o nome completo:")
    if nome is None:
        return  # O usuário clicou em Cancelar

    idade = simpledialog.askinteger("Cadastro", "Digite a idade:")
    if idade is None:
        return

    genero = simpledialog.askstring("Cadastro", "Digite o gênero:")
    if genero is None:
        return

    endereco = simpledialog.askstring("Cadastro", "Digite o endereço:")
    if endereco is None:
        return

    dados_pessoa = [nome, idade, genero, endereco]

    with open('dados.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dados_pessoa)

    label_status.config(text="Cadastro realizado com sucesso!", fg="green")
    listar_pessoas()

def listar_pessoas():
    tree.delete(*tree.get_children())  # Limpar a Treeview antes de exibir novamente
    if os.path.exists('dados.csv'):
        with open('dados.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=row)

        label_status.config(text="")
    else:
        label_status.config(text="Nenhuma pessoa cadastrada.", fg="red")

def excluir_pessoa():
    selected_item = tree.selection()
    if not selected_item:
        label_status.config(text="Selecione uma pessoa para excluir.", fg="red")
        return

    confirmed = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta pessoa?")
    if confirmed:
        selected_index = int(selected_item[0][1:]) - 1  # Obter o índice da pessoa na lista

        with open('dados.csv', 'r') as file:
            data = list(csv.reader(file))

        del data[selected_index]

        with open('dados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        label_status.config(text="Pessoa excluída com sucesso!", fg="green")
        listar_pessoas()

def menu():
    root = ThemedTk(theme="arc")  # Escolha um tema, por exemplo, "arc"
    root.title("Cadastro de Pessoas Carentes para Programa Social")

    global tree
    tree = ttk.Treeview(root, columns=(1, 2, 3, 4), show="headings", height="5")
    tree.heading(1, text="Nome")
    tree.heading(2, text="Idade")
    tree.heading(3, text="Gênero")
    tree.heading(4, text="Endereço")
    tree.pack(padx=10, pady=10)

    btn_cadastrar = Button(root, text="Cadastrar Pessoa", command=cadastrar_pessoa)
    btn_cadastrar.pack(pady=5)

    btn_listar = Button(root, text="Listar Pessoas Cadastradas", command=listar_pessoas)
    btn_listar.pack(pady=5)

    btn_excluir = Button(root, text="Excluir Pessoa", command=excluir_pessoa)
    btn_excluir.pack(pady=5)

    global label_status
    label_status = Label(root, text="", fg="green")
    label_status.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    menu()
