import tkinter as tk #libreria de la interfaz
class ventana_principal:
    def __init__(self):
       
        self.raiz = tk.Tk()  # se crea la ventana
        self.raiz.title("mi primera ventana")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="ELIGE EL MODO DE ENTRADA", font=("Arial 24"), fg="black", bg="sky blue") #añado un texto principal
        self.texto_principal.pack(pady=50) #modifico el tamaño del texto
        self.texto_principal.place(x=500 , y=250) # ubico el tamaño del texto

        self.boton_modo_coordenadas = tk.Button(self.raiz, text ="MODO COORDENADAS", padx=30, pady= 10,font=("Arial 14"), command = self.abrir_coordenadas) # creo un boton, poniendo el texto, el tamaño del boton, y el tipo de letra y el tamaño de la letra
        self.boton_modo_coordenadas.place(x= 550 , y= 380) # posicion del boton 
        self.boton_modo_coordenadas.config(bd=20) # tamaño del estilo del boton
        self.boton_modo_coordenadas.config(relief= "groove") # estilo del boton
        self.boton_modo_coordenadas.config(bg="yellow")  #fondo del boton

        self.boton_modo_triangular = tk.Button(self.raiz, text ="MODO TRIANGULAR", padx=30, pady= 10,font=("Arial 14")) # creo un boton, poniendo el texto, el tamaño del boton, y el tipo de letra y el tamaño de la letra
        self.boton_modo_triangular.place(x= 560 , y= 550) # posicion del boton 
        self.boton_modo_triangular.config(bd=20) # tamaño del estilo del boton
        self.boton_modo_triangular.config(relief= "groove") # estilo del boton
        self.boton_modo_triangular.config(bg="yellow")  #fondo del boton

        self.raiz.mainloop() 

    def abrir_coordenadas(self):     #creo la funcion
        ventana_coordenadas = tk.Toplevel(self.raiz)  # esta linea del codigo sirve para poder abrir otra ventana 
        ventana_modo_coordenadas(ventana_coordenadas)  # se ejecuta la instruccion

class ventana_modo_coordenadas:
    def __init__(self, ventana_coordenadas):
       
        self.raiz = ventana_coordenadas     # se crea la ventana del modo coordenadas
        self.raiz.title("modo coordenadas")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="MODO COORDENADAS", font=("Arial 24"), fg="black", bg="sky blue",) #añado un texto principal
        self.texto_principal.pack(pady=50) #modifico el tamaño del texto
        self.texto_principal.place(x=100 , y=100) # ubico el tamaño del texto

        self.texto_de_x = tk.Label(self.raiz, text= "Ingrese el valor de x en milimetros \n (Maximo 300 milimetros)", font=("Arial 18"), fg="black", bg="sky blue")
        self.texto_de_x.pack(pady = 50)
        self.texto_de_x.place(x=400 , y=250) # ubico el tamaño del texto
        self.raiz.mainloop()


ventana_principal()


