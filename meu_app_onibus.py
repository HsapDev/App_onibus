import tkinter as tk
from tkinter import messagebox
import json
import os


todos_os_pontos = []

def cadastrar_ponto():
    nome =  entry_nome.get()
    linha= entry_linha.get()
    try:
        pessoas = int(entry_pessoas.get())
    except ValueError:
        messagebox.showerror("Erro","Digite um numero valido de pessoas.")
        return
    
    if not nome or not linha:
        messagebox.showwarning("Aviso","Preencha todos os campos")
        return
    
    ponto = {
        'nome ponto':nome,
        'linha ponto':linha,
        'pessoas_esperando':pessoas
    }

    todos_os_pontos.append(ponto)
    salvar_pontos()

    messagebox.showinfo("sucesso",f"ponto'{nome}'cadastrado com sucesso")
    entry_nome.delete(0,tk.END)
    entry_linha.delete(0,tk.END)
    entry_pessoas.delete(0,tk.END)

def mostrar_mapa():
    texto_mapa.delete('1.0',tk.END)
    if not todos_os_pontos:
        texto_mapa.insert(tk.END,"nenhum ponto cadastrado ainda. \n")
    else:
        for ponto in todos_os_pontos:
            texto_mapa.insert(tk.END,f"📍 ponto {ponto['nome ponto']} | Linha: {ponto['linha ponto']} |Pessoas: {ponto['pessoas_esperando']}\n ")

def otimizar_rotas():
    texto_mapa.delete('1.0',tk.END)
    limite=10
    pontos_cheios = [p for p in todos_os_pontos if p['pessoas_esperando']>limite]
    if pontos_cheios:
        texto_mapa.insert(tk.END,"🚨 Alta demanda detectadanos seguintes pontos:\n\n")
        for ponto in pontos_cheios:
            texto_mapa.insert(tk.END,f"📍 ponto {ponto['nome ponto']} | Linha: {ponto['linha ponto']} |Pessoas: {ponto['pessoas_esperando']}\n ")
    else:
            texto_mapa.insert(tk.END,"✅ Todos os pontos estao com lotacao normal.\n")

def Limpar_tela():
    texto_mapa.delete('1.0',tk.END)

def salvar_pontos():
    with open("pontos_onibus.json", "w", encoding="utf-8") as f:
        json.dump(todos_os_pontos, f, ensure_ascii=False, indent=4)

def carregar_pontos():
    global todos_os_pontos
    if os.path.exists("pontos_onibus.json"):
        with open("pontos_onibus.json", "r", encoding="utf-8") as f:
            todos_os_pontos = json.load(f)

def deletar_todos_os_pontos():
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar TODOS os pontos?"):
        global todos_os_pontos
        todos_os_pontos = []
        salvar_pontos()
        texto_mapa.delete('1.0', tk.END)
        messagebox.showinfo("Sucesso", "Todos os pontos foram apagados.")



#Criando Janela
root= tk.Tk()
root.title("Sistema de ônibus inteligente")
root.geometry("500x500")      

#Labels e entradas
tk.Label(root,text="Nome dos pontos").pack()
entry_nome=tk.Entry(root)
entry_nome.pack()

tk.Label(root,text="Linha de Onibus:").pack()
entry_linha =tk.Entry(root)
entry_linha.pack()

tk.Label(root,text="Pessoas Esperando:").pack()
entry_pessoas = tk.Entry(root)
entry_pessoas.pack()


tk.Button(root,text="Cadastrar ponto",command=cadastrar_ponto).pack(pady=5)
tk.Button(root,text="Mostrar Mapa Virtual",command=mostrar_mapa).pack(pady=5)
tk.Button(root,text="Otimizar Rotas",command=otimizar_rotas).pack(pady=5)
tk.Button(root,text="Limpar Tela", command=Limpar_tela,fg='red').pack(pady=5)
tk.Button(root, text="Deletar Todos os Pontos", command=deletar_todos_os_pontos, bg='red', fg='white').pack(pady=5)

texto_mapa=tk.Text(root,height=15,width=60)
texto_mapa.pack(pady=10)
carregar_pontos()

root.mainloop()