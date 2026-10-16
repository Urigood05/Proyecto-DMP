import tkinter as tk #libreria de la interfaz
from tkinter import ttk
from tkinter import messagebox
import math
import sys #libreria para controlar el apagado del programa
class ventana_principal:
    def __init__(self):
       
        self.raiz = tk.Tk()  # se crea la ventana
        self.raiz.title("mi primera ventana")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="ELIGE EL MODO DE ENTRADA", font=("Arial 24"), fg="black", bg="sky blue") #añado un texto principal
       ## self.texto_principal.pack(pady=50) #modifico el tamaño del texto
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

        self.raiz.protocol("WM_DELETE_WINDOW", self.cerrar_todo) ## esta linea de codigo detecta el click de X en la ventana
        
        self.raiz.mainloop() 

    def cerrar_todo(self):
        self.raiz.quit()    # 1. Detiene el mainloop
        self.raiz.destroy() # 2. Destruye la ventana
        sys.exit()          # 3. Apaga Python por completo y libera la terminal

    def abrir_coordenadas(self): #creo la funcion
        self.raiz.withdraw()    # ocultamos la primera ventana
        ventana_coordenadas = tk.Toplevel(self.raiz)  # esta linea del codigo sirve para poder abrir otra ventana y tambien la ventana original
        ventana_modo_coordenadas(ventana_coordenadas, self.raiz)  # se ejecuta la instruccion

    def abrir_triangular(self):
        self.raiz.withdraw()    # ocultamos la segunda ventana
        ventana_triangular = tk.Toplevel(self.raiz)
        ventana_modo_triangular(ventana_triangular,self.raiz)

class ventana_modo_coordenadas:
    def __init__(self, ventana_coordenadas, ventana_origen):

        self.ventana_origen = ventana_origen # Guardamos la ventana principal para usarla luego
        self.raiz = ventana_coordenadas     # se crea la ventana del modo coordenadas
        self.raiz.title("modo coordenadas")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="MODO COORDENADAS", font=("Arial 36"), fg="black", bg="sky blue",) #añado un texto principal
       # self.texto_principal.pack(pady=70) #modifico el tamaño del texto
        self.texto_principal.place(x=450 , y=100) # ubico el tamaño del texto

        self.texto_de_x = tk.Label(self.raiz, text= "Ingrese el valor de x en milimetros \n (Maximo 300 milimetros)", font=("Arial 18"), fg="black", bg="sky blue")
      #  self.texto_de_x.pack(pady = 50)  #tamaño del texto
        self.texto_de_x.place(x=510 , y=200) # ubico el tamaño del texto

        self.validar_comando = self.raiz.register(self.solo_numeros)

        self.ingresar_coordenadas = tk.Entry(self.raiz, font=("Arial 18"),validate= "key", validatecommand=(self.validar_comando, '%P') ) # el key es para evaluar la entrada de texto
       # self.ingresar_coordenadas.pack()
        self.ingresar_coordenadas.place(x = 570 , y = 270)

        self.texto_de_y = tk.Label(self.raiz, text= "Ingrese el valor de y en milimetros \n (por lo pronto le pongo 100 milimetros)", font=("Arial 18"), fg="black", bg="sky blue") # se crea el cuadro de texto de y
       # self.texto_de_y.pack(pady = 50) 
        self.texto_de_y.place(x = 510 , y = 320 )

        self.validar_comando1 = self.raiz.register(self.solo_numeros_coordenada_y)

        self.ingresar_coordenadasy = tk.Entry(self.raiz, font=("Arial 18"), validate = "key", validatecommand = (self.validar_comando1, '%P'))
       # self.ingresar_coordenadasy.pack()
        self.ingresar_coordenadasy.place(x = 570 , y = 390)

        self.boton_ejecutar = tk.Button(self.raiz, text = "Ejecutar", font = ("Arial 16"), padx = 20, pady= 10, command=self.ejecutar_y_abrir_panel)
        self.boton_ejecutar.place(x = 615 , y = 450)
        self.boton_ejecutar.config(bd = 20)
        self.boton_ejecutar.config(relief= "groove")
        self.boton_ejecutar.config(bg = "green")

        self.volver_menu_principal = tk.Button(self.raiz, text = "volver al menu principal",font = ("Arial 16"), padx = 30, pady= 10,  command=self.regresar)
        self.volver_menu_principal.place(x = 1000 , y = 700)
        self.volver_menu_principal.config(bd = 20)
        self.volver_menu_principal.config(relief = "groove")
        self.volver_menu_principal.config(bg = "red")

   # def verificar_coordenadas(self):
        # Obtenemos el texto escrito en las cajas de X y Y
      #  texto_x = self.ingresar_coordenadas.get()
       # texto_y = self.ingresar_coordenadasy.get()
        
        # Revisamos si alguna de las dos está totalmente vacía
        #if texto_x == "" or texto_y == "":
         #   messagebox.showwarning("Campos vacíos", "Por favor, ingrese los valores de x y y antes de presionar Ejecutar.")
          #  return False
      #  return True

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

    def solo_numeros_coordenada_y(self, texto_nuevo):
            if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                return True
            
            if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                
                valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                
                if valor > 100: # se verifica si se pada el limite
                    # se muestra la ventana de advertencia
                    messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")
                    return False # Rechazamos el ingreso de ese número
                
                return True # Si es un número y es <= 300, lo permitimos
            
            return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

   # def ejecutar_y_abrir_panel(self):
      #  if not self.verificar_coordenadas():
       #     return
       # self.raiz.withdraw()
        #ventana_panel = tk.Toplevel(self.raiz)
      #  panel_de_control(ventana_panel, self.raiz)

    def ejecutar_y_abrir_panel(self):
    # No modificamos verificar_coordenadas() — simplemente comprobamos aquí
        texto_x = self.ingresar_coordenadas.get()
        texto_y = self.ingresar_coordenadasy.get()

        if texto_x == "" or texto_y == "":
        # mostramos la misma advertencia que ya usabas
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese los valores de x y y antes de presionar Ejecutar.")
            return
        self.raiz.withdraw()
        ventana_panel = tk.Toplevel(self.raiz)
        panel_de_control(ventana_panel, self.raiz)

    # Si pasa la comprobación, ocultamos esta ventana y abrimos el panel 
    
    # falta que nomas se pongan numeros en la coordenada y pero no conozco hasta cuanto se tiene que poner 
    # tambien me falta hacer una declaracion porque 


class ventana_modo_triangular:
    def __init__(self, ventana_triangular, ventana_origen):
        self.ventana_origen = ventana_origen
        self.raiz = ventana_triangular

        self.valor_hipotenusa = tk.StringVar() # llamamos a la funcion el stringvar porque actua como un espia para el calculo automatico
        self.valor_angulo = tk.StringVar()
                
        self.valor_hipotenusa.trace_add("write", self.calcular_automatico) # se le ordena ejecutar la funcion cada que el usuario escriba 
        self.valor_angulo.trace_add("write", self.calcular_automatico) # el trace add son palabras exclusivas

        self.raiz.title("MODO TRIANGULAR")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_triangular = tk.Label(self.raiz, text = "MODO TRIANGULAR",  font=("Arial 24"), fg="black", bg="sky blue")
        self.texto_triangular.pack(pady = 50)  #tamaño del texto
        self.texto_triangular.place(x=560 , y=50) # ubico el tamaño del texto

        self.texto__hipotenusa = tk.Label(self.raiz, text= "Ingrese el valor de la hipotenusa \n (por lo pronto 100 milimetros max)", font=("Arial 18"), fg="black", bg="sky blue")
        self.texto__hipotenusa.pack(pady = 50)  #tamaño del texto
        self.texto__hipotenusa.place(x=300 , y=140) # ubico el tamaño del texto

        self.validar_comando1 = self.raiz.register(self.solo_numeros_hipotenusa)

        self.ingresar_valor_hipotenusa = tk.Entry(self.raiz, font=("Arial 16"), textvariable= self.valor_hipotenusa, validate = "key", validatecommand=(self.validar_comando1, "%P") )
        self.ingresar_valor_hipotenusa.pack()
        self.ingresar_valor_hipotenusa.place(x = 350 , y = 200)

        self.ingresar_angulo = tk.Label(self.raiz, text= "Ingresa el valor del angulo", font = ("Arial 18"), fg="black", bg="sky blue")
        self.ingresar_angulo.pack(pady = 50)
        self.ingresar_angulo.place( x= 320 , y = 250)

        self.validar_comando = self.raiz.register(self.solo_numeros)

        self.ingresar_texto_angulo = tk.Entry(self.raiz, font = ("Arial 16"), textvariable = self.valor_angulo, validate= "key", validatecommand=(self.validar_comando, '%P'))
        self.ingresar_texto_angulo.pack()
        self.ingresar_texto_angulo.place(x = 350 , y = 300)

        self.texto_del_desplazamientox =tk.Label(self.raiz, text = "El desplazamiento en el eje x sera",  font = ("Arial 18"), fg="black", bg="sky blue")
        self.texto_del_desplazamientox.pack()
        self.texto_del_desplazamientox.place(x = 800 , y = 140)

        self.desplazamiento = tk.Entry(self.raiz, font = ("Arial 18"))
        self.desplazamiento.pack()
        self.desplazamiento.place(x = 840 , y = 190)

        self.texto_desplazamientoy = tk.Label(self.raiz, text ="El desplazamiento en el eje y sera", font= ("Arial 18"), fg="black", bg="sky blue")
        self.texto_desplazamientoy.pack()
        self.texto_desplazamientoy.place(x = 800, y = 250)

        self.desplazamiento_en_y = tk.Entry(self.raiz, font = "Arial 18")
        self.desplazamiento_en_y.pack()
        self.desplazamiento_en_y.place(x = 840 , y = 300)

        self.boton_ejecutar_operacion = tk.Button(self.raiz, text = "Ejecutar", font = ("Arial 16"), padx = 20, pady= 10,command=self.verificar_triangulo)
        self.boton_ejecutar_operacion.place(x = 615 , y = 450)
        self.boton_ejecutar_operacion.config(bd = 20)
        self.boton_ejecutar_operacion.config(relief= "groove")
        self.boton_ejecutar_operacion.config(bg = "green")

        self.volver_menu_principal = tk.Button(self.raiz, text = "volver al menu principal",font = ("Arial 16"), padx = 30, pady= 10, command=self.regresar)
        self.volver_menu_principal.place(x = 1000 , y = 700)
        self.volver_menu_principal.config(bd = 20)
        self.volver_menu_principal.config(relief = "groove")
        self.volver_menu_principal.config(bg = "red")

      # --- FUNCIONES ADICIONALES DE LA VENTANA ---
    def regresar(self):
        self.raiz.destroy() # cierra esta ventana
        self.ventana_origen.deiconify() # muestra la ventana principal

    def calcular_automatico(self, *args):
        try:
            texto_hip = self.valor_hipotenusa.get()
            texto_ang = self.valor_angulo.get()
            
            # Si borran el texto, vaciamos los resultados
            if texto_hip == "" or texto_ang == "":
                self.desplazamiento.delete(0, tk.END)
                self.desplazamiento_en_y.delete(0, tk.END)
                return
            
            # Convertimos el texto a números con decimales
            hip = float(texto_hip)
            ang = float(texto_ang)
            
            # Fórmulas trigonométricas (convertimos a radianes primero)
            ang_rad = math.radians(ang)
            val_x = hip * math.cos(ang_rad)
            val_y = hip * math.sin(ang_rad)
            
            # Tu regla especial: si termina en <= .5 se queda abajo, si es .6 sube.
            def redondear_especial(valor):
                entero = int(valor)
                decimal = abs(valor - entero)
                if decimal <= 0.5:
                    return entero
                else:
                    return entero + 1 if valor > 0 else entero - 1
            
            # Aplicamos tu regla de redondeo
            val_x_redondeado = redondear_especial(val_x)
            val_y_redondeado = redondear_especial(val_y)
            
            # Escribimos los resultados en los cuadros de la derecha
            self.desplazamiento.delete(0, tk.END)
            self.desplazamiento.insert(0, str(val_x_redondeado))
            
            self.desplazamiento_en_y.delete(0, tk.END)
            self.desplazamiento_en_y.insert(0, str(val_y_redondeado))
            
        except ValueError:
            # Si escriben letras por accidente, ignoramos el error para que no explote
            pass

    def verificar_triangulo(self):
        # Usamos tus variables espía para leer el contenido actual
        hip = self.valor_hipotenusa.get()
        ang = self.valor_angulo.get()
        
        if hip == "" or ang == "":
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese el valor de la hipotenusa y el ángulo antes de presionar Ejecutar.")
        else:
            # Como el cálculo ya lo hicimos automático con trace_add, aquí no es necesario hacer matemáticas, 
            # pero el botón cumple la función de validar que no falten datos.
            pass


    def solo_numeros(self, texto_nuevo):
                    if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                        return True
                    
                    if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                        
                        valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                        
                        if valor > 360: # se verifica si se pada el limite
                            # se muestra la ventana de advertencia
                            messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")
                            return False # Rechazamos el ingreso de ese número
                        
                        return True # Si es un número y es <= 360, lo permitimos
                    
                    return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

    
    def solo_numeros_hipotenusa(self, texto_nuevo):
            if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                return True
            
            if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                
                valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                
                if valor > 100: # se verifica si se pada el limite
                    # se muestra la ventana de advertencia
                    messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")
                    return False # Rechazamos el ingreso de ese número
                
                return True # Si es un número y es <= 300, lo permitimos
            
            return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos


     # me falta ajustar que nomas se ingresen nuneros en la hipotenusa pero no conosco su valor maximo mejor despues de lo pongo        
        
class panel_de_control:
     def __init__(self, ventana_panel, ventana_origen):

        self.raiz = ventana_panel
        self.ventana_origen = ventana_origen
        
        self.raiz.title("panel de control")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.tabla_panel = ttk.Treeview(self.raiz, columns=("col1"))

        self.tabla_panel.column("#0" , width = 80 , anchor = "center")
        self.tabla_panel.heading("#0", text= "Motor de desplazamiento lineal", anchor= "center")
                                


ventana_principal()


