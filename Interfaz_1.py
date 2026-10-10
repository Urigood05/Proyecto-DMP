import tkinter as tk #libreria de la interfaz
from tkinter import messagebox
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

        self.boton_modo_triangular = tk.Button(self.raiz, text ="MODO TRIANGULAR", padx=30, pady= 10,font=("Arial 14"), command = self.abrir_triangular) # creo un boton, poniendo el texto, el tamaño del boton, y el tipo de letra y el tamaño de la letra
        self.boton_modo_triangular.place(x= 560 , y= 550) # posicion del boton 
        self.boton_modo_triangular.config(bd=20) # tamaño del estilo del boton
        self.boton_modo_triangular.config(relief= "groove") # estilo del boton
        self.boton_modo_triangular.config(bg="yellow")  #fondo del boton

        self.raiz.mainloop() 

    def abrir_coordenadas(self): #creo la funcion
        self.raiz.withdraw()    # ocultamos la primera ventana
        ventana_coordenadas = tk.Toplevel(self.raiz)  # esta linea del codigo sirve para poder abrir otra ventana y tambien la ventana original
        ventana_modo_coordenadas(ventana_coordenadas, self.raiz)  # se ejecuta la instruccion

    def abrir_triangular(self):
        ventana_triangular = tk.Toplevel(self.raiz)
        ventana_modo_triangular(ventana_triangular, self.raiz)

class ventana_modo_coordenadas:
    def __init__(self, ventana_coordenadas, ventana_origen):

        self.ventana_origen = ventana_origen # Guardamos la ventana principal para usarla luego
        self.raiz = ventana_coordenadas     # se crea la ventana del modo coordenadas
        self.raiz.title("modo coordenadas")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="MODO COORDENADAS", font=("Arial 36"), fg="black", bg="sky blue",) #añado un texto principal
        self.texto_principal.pack(pady=70) #modifico el tamaño del texto
        self.texto_principal.place(x=450 , y=100) # ubico el tamaño del texto

        self.texto_de_x = tk.Label(self.raiz, text= "Ingrese el valor de x en milimetros \n (Maximo 300 milimetros)", font=("Arial 18"), fg="black", bg="sky blue")
        self.texto_de_x.pack(pady = 50)  #tamaño del texto
        self.texto_de_x.place(x=510 , y=200) # ubico el tamaño del texto

        self.validar_comando = self.raiz.register(self.solo_numeros)

        self.ingresar_coordenadas = tk.Entry(self.raiz, font=("Arial 18"),validate= "key", validatecommand=(self.validar_comando, '%P') )
        self.ingresar_coordenadas.pack()
        self.ingresar_coordenadas.place(x = 570 , y = 270)

        self.texto_de_y = tk.Label(self.raiz, text= "Ingrese el valor de y en milimetros", font=("Arial 18"), fg="black", bg="sky blue") # se crea el cuadro de texto de y
        self.texto_de_y.pack(pady = 50) 
        self.texto_de_y.place(x = 510 , y = 320 )

        self.ingresar_coordenadasy = tk.Entry(self.raiz, font=("Arial 18"))
        self.ingresar_coordenadasy.pack()
        self.ingresar_coordenadasy.place(x = 570 , y = 370)

        self.boton_ejecutar = tk.Button(self.raiz, text = "Ejecutar", font = ("Arial 16"), padx = 20, pady= 10)
        self.boton_ejecutar.place(x = 615 , y = 450)
        self.boton_ejecutar.config(bd = 20)
        self.boton_ejecutar.config(relief= "groove")
        self.boton_ejecutar.config(bg = "green")

        self.volver_menu_principal = tk.Button(self.raiz, text = "volver al menu principal",font = ("Arial 16"), padx = 30, pady= 10,  command=self.regresar)
        self.volver_menu_principal.place(x = 1000 , y = 700)
        self.volver_menu_principal.config(bd = 20)
        self.volver_menu_principal.config(relief = "groove")
        self.volver_menu_principal.config(bg = "red")

    def regresar(self):
        self.raiz.destroy() # Destruye la ventana de coordenadas
        self.ventana_origen.deiconify() # Vuelve a hacer visible la ventana principal

    def solo_numeros(self, texto_nuevo):
        if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
            return True
        
        if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
            
            valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
            
            if valor > 300: # se verifica si se pada el limite
                # se muestra la ventana de advertencia
                messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")
                return False # Rechazamos el ingreso de ese número
            
            return True # Si es un número y es <= 300, lo permitimos
        
        return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos


class ventana_modo_triangular:
    def __init__(self, ventana_triangular):
        self.raiz = ventana_triangular
        self.raiz.title("MODO TRIANGULAR")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_de_x = tk.Label(self.raiz, text= "Ingrese el valor de la hipotenusa", font=("Arial 18"), fg="black", bg="sky blue")
        self.texto_de_x.pack(pady = 50)  #tamaño del texto
        self.texto_de_x.place(x=150 , y=200) # ubico el tamaño del texto


        

              
ventana_principal()


