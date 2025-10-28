import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from playsound import playsound 
from PIL import Image, ImageTk
import threading
import os
import time

# ======== FUNÇÃO SEGURA PARA TOCAR SOM ========
def tocar_som(caminho):
    def run():
        try:
            playsound(caminho)
        except Exception as e:
            if tk.Toplevel().winfo_exists():
                 tk.Toplevel().after(0, lambda: messagebox.showerror("Erro de Som", f"Não foi possível tocar o som:\n{e}"))
            print(f"Erro ao tocar som '{caminho}': {e}")
            
    # Inicia a thread para não travar a interface gráfica (GUI)
    threading.Thread(target=run, daemon=True).start()

# ======== CLASSE BASE ========
class Animal:
    """
    Classe Base para todos os animais do Zoológico.
    Gerencia energia, status de vida, e a perda de energia em background.
    """
    def __init__(self, nome, idade, imagem_awake, som, imagem_sleep=None):
        self.__nome = nome
        self.__idade = idade
        self.__energia = 100
        self.imagem_awake = imagem_awake
        self.imagem_sleep = imagem_sleep
        self.som = som
        self.vivo = True
        self._iniciar_perda_energia() # Inicia a thread de perda de energia

    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade

    @property
    def energia(self):
        return self.__energia

    def alimentar(self):
        """Aumenta a energia do animal em 20 pontos, até o máximo de 100."""
        if not self.vivo:
            return f"{self.nome} está muito cansado e não pode se alimentar."
        self.__energia = min(100, self.__energia + 20)
        return f"{self.nome} foi alimentado! 🍖 Energia atual: {self.__energia}%"

    def _iniciar_perda_energia(self):
        """Inicia uma thread separada para a perda contínua de energia."""
        def perder():
            while True:
                if not self.vivo:
                    break
                time.sleep(5) # Perde 5% a cada 5 segundos
                if self.__energia > 0:
                    self.__energia -= 5
                    if self.__energia <= 0:
                        self.__energia = 0
                        self.vivo = False
                        print(f"💀 {self.nome} ficou exausto!")
                    elif self.__energia <= 20:
                        print(f"⚠️ {self.nome} está com pouca energia ({self.__energia}%)!")
        threading.Thread(target=perder, daemon=True).start()

    def falar(self):
        """Faz o animal emitir o som, consome 10 de energia e mostra o estado."""
        if not self.vivo:
            self._mostrar_imagem(sleep_forced=True) # Exausto
            return f"{self.nome} está sem energia e não consegue fazer som..."
        
        # Consome energia antes de qualquer verificação de status
        self.__energia = max(0, self.__energia - 10)

        if self.__energia <= 20 and self.vivo:
            self._mostrar_imagem() # Fraco/Dormindo
            return f"{self.nome} está com pouca energia ({self.__energia}%) — precisa se alimentar!"
        elif not self.vivo:
            self._mostrar_imagem(sleep_forced=True) # Se a energia foi para 0 com essa ação
            return f"{self.nome} ficou exausto e não conseguiu fazer o som!"
        
        # Toca o som usando a função segura
        if os.path.exists(self.som):
            tocar_som(self.som)
        else:
            print(f"Som não encontrado: {self.som}")
            messagebox.showwarning("Aviso de Som", f"Arquivo de som '{self.som}' não encontrado.")

        self._mostrar_imagem() # Ativo
        return f"{self.nome} fez seu som! Energia atual: {self.__energia}%"

    def _mostrar_imagem(self, sleep_forced=False):
        """Decide qual imagem mostrar (ativo ou dormindo/exausto) e chama a função Toplevel."""
        # Se for forçado (e.g., está exausto) OU energia <= 20 e imagem de sono existe
        if (self.__energia <= 20 or sleep_forced) and self.imagem_sleep:
            caminho = self.imagem_sleep
        else:
            caminho = self.imagem_awake
        mostrar_imagem(caminho, f"{self.nome} - Energia: {self.__energia}%")

# ======== SUBCLASSES SIMPLIFICADAS (Herança) ========
class Onca(Animal): pass
class Macaco(Animal): pass
class Papagaio(Animal): pass
class Elefante(Animal): pass
class Cobra(Animal): pass

# ======== FUNÇÃO PARA EXIBIR IMAGEM POP-UP ========
def mostrar_imagem(caminho, titulo):
    """Cria uma janela Toplevel para exibir uma imagem por 10 segundos."""
    if not caminho or not os.path.exists(caminho):
        messagebox.showerror("Erro de Arquivo", f"Imagem '{caminho}' não encontrada!")
        return

    janela_img = Toplevel()
    janela_img.title(titulo)

    try:
        imagem = Image.open(caminho)
        imagem.thumbnail((500, 400)) # Redimensiona para caber na tela
        img_tk = ImageTk.PhotoImage(imagem)
    except Exception as e:
        messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem: {e}")
        janela_img.destroy()
        return

    lbl = tk.Label(janela_img, image=img_tk)
    lbl.image = img_tk # Referência para evitar o garbage collector
    lbl.pack(padx=10, pady=10)

    # Fecha a janela automaticamente após 10000ms (10 segundos)
    janela_img.after(10000, janela_img.destroy)

# ======== CLASSE PRINCIPAL DO ZOOLÓGICO (TKINTER) ========
class ZoologicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Zoológico Interativo - Charles Darwin 🐾")
        self.root.geometry("600x500")
        self.animais = []

        tk.Label(root, text="🐒 Zoológico Interativo - Charles Darwin 🐘", font=("Arial", 16, "bold")).pack(pady=10)

        # Botões Principais
        tk.Button(root, text="➕ Adicionar Animal", command=self.adicionar_animal, width=30).pack(pady=6)
        tk.Button(root, text="🔊 Fazer Animal Falar", command=self.falar_animal, width=30).pack(pady=6)
        tk.Button(root, text="🍖 Alimentar Animal", command=self.alimentar_animal, width=30).pack(pady=6)
        tk.Button(root, text="🚪 Sair", command=root.quit, width=30).pack(pady=12)

        # Frame para listar os animais e suas barras de energia
        self.frame_animais = tk.Frame(root)
        self.frame_animais.pack(pady=10, fill="both", expand=True)

        # Inicia a atualização periódica da lista
        self.atualizar_lista_periodicamente()

    def adicionar_animal(self):
        """Pede dados ao usuário e cria uma instância do animal, adicionando-a à lista."""
        nome = simpledialog.askstring("Novo Animal", "Digite o nome do animal:")
        if not nome: return
        idade = simpledialog.askinteger("Idade", "Digite a idade do animal:")
        if idade is None: return
        tipo = simpledialog.askstring("Tipo", "Digite o tipo (onca, macaco, papagaio, elefante, cobra):")
        if not tipo: return
        tipo = tipo.lower().strip()

        classes = {
            "onca": (Onca, "onca.png", "onca.mp3", "onca_dormindo.png"),
            "macaco": (Macaco, "macaco.png", "macaco.mp3", "macaco_dormindo.png"),
            "papagaio": (Papagaio, "papagaio.png", "papagaio.mp3", "papagaio_dormindo.png"),
            "elefante": (Elefante, "elefante.png", "elefante.mp3", "elefante_dormindo.png"), 
            "cobra": (Cobra, "cobra.png", "cobra.mp3", "cobra_dormindo.png"), 
        }

        if tipo in classes:
            classe, img_awake, som, img_sleep = classes[tipo]
            animal = classe(nome, idade, img_awake, som, imagem_sleep=img_sleep)
            self.animais.append(animal)
            messagebox.showinfo("Sucesso", f"{classe.__name__} '{nome}' adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Tipo de animal inválido!")

    def alimentar_animal(self):
        """Chama o método alimentar() no animal selecionado."""
        if not self.animais:
            messagebox.showwarning("Aviso", "Nenhum animal cadastrado.")
            return
        nomes = [a.nome for a in self.animais]
        nome = simpledialog.askstring("Alimentar", f"Escolha um animal: {', '.join(nomes)}")
        if not nome: return
        
        for a in self.animais:
            if a.nome == nome:
                msg = a.alimentar()
                messagebox.showinfo("Alimentar", msg)
                return
        messagebox.showerror("Erro", "Animal não encontrado.")

    def falar_animal(self):
        """Chama o método falar() no animal selecionado, disparando som e imagem."""
        if not self.animais:
            messagebox.showwarning("Aviso", "Nenhum animal cadastrado.")
            return
        nomes = [a.nome for a in self.animais]
        nome = simpledialog.askstring("Falar", f"Escolha um animal: {', '.join(nomes)}")
        if not nome: return
        
        for a in self.animais:
            if a.nome == nome:
                msg = a.falar()
                # Exibe a mensagem de acordo com o estado do animal
                if not a.vivo:
                    messagebox.showwarning("Exaustão", msg)
                elif a.energia <= 20:
                    messagebox.showwarning("Pouca Energia", msg)
                else:
                    messagebox.showinfo("Som e Energia", msg)
                return
        messagebox.showerror("Erro", "Animal não encontrado.")

    def atualizar_lista_periodicamente(self):
        """
        Limpa e redesenha a lista de animais com suas barras de energia
        a cada intervalo de tempo (2 segundos).
        """
        # Limpa o frame
        for widget in self.frame_animais.winfo_children():
            widget.destroy()

        if not self.animais:
            tk.Label(self.frame_animais, text="Nenhum animal cadastrado ainda.").pack(pady=20)
        else:
            for a in self.animais:
                frame = tk.Frame(self.frame_animais)
                frame.pack(fill="x", pady=5, padx=10)

                # Determina o estado de exibição
                estado = "Ativo"
                if not a.vivo:
                    estado = "EXAUSTO 💀"
                elif a.energia <= 20:
                    estado = "Fraco ⚠️"

                tk.Label(frame, text=f"{a.nome} ({a.__class__.__name__}) - {estado}", width=40, anchor="w", font=("Arial", 10)).pack(side="left", padx=5)

                # Criação da barra de energia (Canvas)
                barra = tk.Canvas(frame, width=120, height=15, bg="#E0E0E0", highlightthickness=0)
                barra.pack(side="left", padx=10)

                # Define a cor da barra
                cor = "green"
                if not a.vivo: # Se exausto, fica cinza/escuro
                    cor = "gray" 
                elif a.energia <= 20:
                    cor = "red"
                elif a.energia <= 50:
                    cor = "yellow"

                # Desenha o preenchimento da barra
                largura_preenchimento = a.energia * 1.2
                barra.create_rectangle(0, 0, largura_preenchimento, 15, fill=cor, outline="")
                
                # Exibe o texto da porcentagem
                barra.create_text(60, 7, text=f"{a.energia}%", fill="black", font=("Arial", 8, "bold"))


        # Agenda a próxima atualização após 2000ms (2 segundos)
        self.root.after(2000, self.atualizar_lista_periodicamente)

# ======== EXECUÇÃO ========
if __name__ == "__main__":
    root = tk.Tk()
    app = ZoologicoApp(root)
    root.mainloop()