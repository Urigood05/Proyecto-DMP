import tkinter as tk #libreria de la interfaz
from tkinter import ttk  # widgets con estilo moderno (esta importado pero por ahora no se usa)
from tkinter import messagebox  # para mostrar ventanas de aviso y advertencia
import math  # funciones matematicas (seno y coseno) para el modo triangular
import sys #libreria para controlar el apagado del programa
import time   # para medir cuanto tarda el movimiento de los motores
import serial # para hablar con la placa por el puerto serial (se instala con: pip install pyserial)

# ====== AJUSTA ESTOS VALORES ======
PUERTO = "COM6"          # puerto de la placa, el mismo que ves en Arduino IDE > Herramientas > Puerto
BAUDIOS = 9600           # velocidad de comunicacion, debe ser igual que Serial.begin() del .ino
PASOS_POR_REV = 2048     # pasos que da cada motor 28BYJ-48 para dar 1 vuelta completa
VELOCIDAD_RPM = 2        # velocidad de los motores en vueltas por minuto, igual que VELOCIDAD_RPM del .ino
MM_POR_REV = 8.0         # mm que avanza el mecanismo lineal por cada vuelta del motor 1 (valor de ejemplo)
RELACION_ENGRANE = 1.0   # vueltas del motor 2 por cada vuelta del engrane (1.0 = sin engrane, se cambia despues)
GRADOS_POR_MM = 1.0      # grados que gira el motor 2 por cada mm de Y en modo coordenadas (1.0 = 1 mm vale 1 grado, valor temporal que se cambia despues)
# ==================================


class Motor:             # esta clase solo se encarga de hablar con la placa (motores y sensores)
    def __init__(self, puerto, baudios):   # se ejecuta al crear el objeto, recibe el puerto y la velocidad
        self.buffer = ""                   # aqui se guarda el texto que llega de la placa hasta completar una linea
        try:   # intenta abrir el puerto; si algo falla salta a "except"
            self.ser = serial.Serial(puerto, baudios, timeout=0.05)   # abre el puerto serial, espera maximo 50 ms al leer
            time.sleep(2)                  # espera 2 segundos porque la placa se reinicia al abrir el puerto
            self.ser.reset_input_buffer()  # borra lo que la placa mando mientras se reiniciaba
        except serial.SerialException:     # si no se pudo abrir (placa desconectada o puerto ocupado)
            self.ser = None                # sin placa: el programa sigue funcionando en modo simulacion

    def conectado(self):                   # dice si hay una placa conectada
        return self.ser is not None        # True si el puerto se abrio, False si esta en simulacion

    def mover(self, pasos_x, pasos_y):     # manda los pasos de los 2 motores a la placa
        if self.ser:                       # solo si hay placa conectada
            self.buffer = ""               # descarta texto viejo para no mezclarlo con este movimiento
            self.ser.reset_input_buffer()  # descarta lecturas de sensores acumuladas mientras no se leia el puerto
            self.ser.write(f"M,{pasos_x},{pasos_y}\n".encode())   # arma el texto "M,pasosX,pasosY", le agrega salto de linea y lo manda en bytes

    def leer(self):                        # lee lo que mando la placa; devuelve (avance, termino, sensores)
        avance = None                      # ultimo avance recibido como (pasosX, pasosY); None si no llego ninguno
        termino = False                    # pasa a True cuando la placa responde OK
        sensores = None                    # ultima lectura como (dist1, dist2, angulo x10, estado iman); None si no llego ninguna
        if self.ser is None:               # si no hay placa (modo simulacion)
            return None, True, None        # se considera terminado de inmediato y no hay sensores
        self.buffer += self.ser.read(self.ser.in_waiting).decode(errors="ignore")   # lee todo lo que haya llegado y lo agrega al buffer
        *lineas, self.buffer = self.buffer.split("\n")   # separa por lineas; lo ultimo (linea incompleta) se queda en el buffer
        for linea in lineas:               # revisa cada linea completa que llego
            linea = linea.strip()          # quita espacios y saltos de linea
            partes = linea.split(",")      # separa la linea por comas, por ejemplo ["P", "5120", "112"]
            try:                           # intenta convertir los datos a numeros
                if partes[0] == "P" and len(partes) == 3:   # si es un mensaje de avance "P,pasosX,pasosY"
                    avance = (int(partes[1]), int(partes[2]))   # guarda los pasos de cada motor
                elif partes[0] == "S" and len(partes) == 5:   # si es un mensaje de sensores "S,d1,d2,angulo,estado"
                    sensores = tuple(int(dato) for dato in partes[1:])   # guarda los 4 datos como numeros enteros
                elif partes[0] == "OK":    # si la placa dice que ya termino
                    termino = True         # marca el movimiento como terminado
            except ValueError:             # si algun dato no era un numero (linea danada)
                pass                       # ignora esa linea
        return avance, termino, sensores   # devuelve lo ultimo que llego de cada tipo

    def cerrar(self):                      # libera el puerto serial
        if self.ser:                       # solo si hay placa conectada
            self.ser.close()               # cierra el puerto para que otro programa pueda usarlo

class ventana_principal:  # ventana del menu principal
    def __init__(self):   # se ejecuta al crear la ventana
       
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
        
        self.raiz.mainloop()  # mantiene la ventana abierta esperando clics y teclas

    def cerrar_todo(self):  # se ejecuta cuando el usuario cierra la ventana con la X
        motores.cerrar()    # libera el puerto serial
        self.raiz.quit()    # 1. Detiene el mainloop
        self.raiz.destroy() # 2. Destruye la ventana
        sys.exit()          # 3. Apaga Python por completo y libera la terminal

    def abrir_coordenadas(self): #creo la funcion
        self.raiz.withdraw()    # ocultamos la primera ventana
        ventana_coordenadas = tk.Toplevel(self.raiz)  # esta linea del codigo sirve para poder abrir otra ventana y tambien la ventana original
        ventana_modo_coordenadas(ventana_coordenadas, self.raiz)  # se ejecuta la instruccion

    def abrir_triangular(self):  # abre la ventana del modo triangular
        self.raiz.withdraw()    # ocultamos la segunda ventana
        ventana_triangular = tk.Toplevel(self.raiz)  # crea una ventana nueva encima de la principal
        ventana_modo_triangular(ventana_triangular,self.raiz)  # arma el contenido del modo triangular en esa ventana

class ventana_modo_coordenadas:  # ventana donde se escriben X (mm) y Y (mm)
    def __init__(self, ventana_coordenadas, ventana_origen):  # recibe su ventana y la ventana principal

        self.ventana_origen = ventana_origen # Guardamos la ventana principal para usarla luego
        self.raiz = ventana_coordenadas     # se crea la ventana del modo coordenadas
        self.raiz.title("modo coordenadas")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_principal = tk.Label(self.raiz, text="MODO COORDENADAS", font=("Arial 36"), fg="black", bg="sky blue",) #añado un texto principal
       # self.texto_principal.pack(pady=70) #modifico el tamaño del texto
        self.texto_principal.place(x=450 , y=100) # ubico el tamaño del texto

        self.texto_de_x = tk.Label(self.raiz, text= "Ingrese el valor de x en milimetros \n (Maximo 300 milimetros)", font=("Arial 18"), fg="black", bg="sky blue")  # texto que pide el valor de x
      #  self.texto_de_x.pack(pady = 50)  #tamaño del texto
        self.texto_de_x.place(x=510 , y=200) # ubico el tamaño del texto

        self.validar_comando = self.raiz.register(self.solo_numeros) #linea donde se le va a llamar a la funcion solo numeros

        self.ingresar_coordenadas = tk.Entry(self.raiz, font=("Arial 18"),validate= "key", validatecommand=(self.validar_comando, '%P') ) # el key es para evaluar la entrada de texto
       # self.ingresar_coordenadas.pack()
        self.ingresar_coordenadas.place(x = 570 , y = 270)  # posicion del cuadro donde se escribe x

        self.texto_de_y = tk.Label(self.raiz, text= "Ingrese el valor de y en milimetros \n maximo 125mm", font=("Arial 18"), fg="black", bg="sky blue") # se crea el cuadro de texto de y
       # self.texto_de_y.pack(pady = 50) 
        self.texto_de_y.place(x = 510 , y = 320 )  # posicion del texto de y

        self.validar_comando1 = self.raiz.register(self.solo_numeros_coordenada_y)  # registra la funcion que valida lo que se escribe en y

        self.ingresar_coordenadasy = tk.Entry(self.raiz, font=("Arial 18"), validate = "key", validatecommand = (self.validar_comando1, '%P'))  # cuadro donde se escribe y, valida cada tecla
       # self.ingresar_coordenadasy.pack()
        self.ingresar_coordenadasy.place(x = 570 , y = 390)  # posicion del cuadro donde se escribe y

        self.boton_ejecutar = tk.Button(self.raiz, text = "Ejecutar", font = ("Arial 16"), padx = 20, pady= 10, command=self.ejecutar_y_abrir_panel)  # boton que abre el panel y mueve los motores
        self.boton_ejecutar.place(x = 615 , y = 450)  # posicion del boton ejecutar
        self.boton_ejecutar.config(bd = 20)  # grosor del borde del boton
        self.boton_ejecutar.config(relief= "groove")  # estilo del borde del boton
        self.boton_ejecutar.config(bg = "green")  # color de fondo del boton

        self.volver_menu_principal = tk.Button(self.raiz, text = "volver al menu principal",font = ("Arial 16"), padx = 30, pady= 10,  command=self.regresar)  # boton para volver al menu
        self.volver_menu_principal.place(x = 1000 , y = 700)  # posicion del boton volver
        self.volver_menu_principal.config(bd = 20)  # grosor del borde del boton
        self.volver_menu_principal.config(relief = "groove")  # estilo del borde del boton
        self.volver_menu_principal.config(bg = "red")  # color de fondo del boton

   # def verificar_coordenadas(self):
        # Obtenemos el texto escrito en las cajas de X y Y
      #  texto_x = self.ingresar_coordenadas.get()
       # texto_y = self.ingresar_coordenadasy.get()
        
        # Revisamos si alguna de las dos está totalmente vacía
        #if texto_x == "" or texto_y == "":
         #   messagebox.showwarning("Campos vacíos", "Por favor, ingrese los valores de x y y antes de presionar Ejecutar.")
          #  return False
      #  return True

    def regresar(self):  # se ejecuta al presionar "volver al menu principal"
        self.raiz.destroy() # Destruye la ventana de coordenadas
        self.ventana_origen.deiconify() # Vuelve a hacer visible la ventana principal

    def solo_numeros(self, texto_nuevo):  # valida lo que se escribe en x (solo numeros hasta 300)
        if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
            return True  # el cuadro vacio es valido
        
        if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
            
            valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
            
            if valor > 300: # se verifica si se pada el limite
                # se muestra la ventana de advertencia
                messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")  # avisa que el valor no es valido
                return False # Rechazamos el ingreso de ese número
            
            return True # Si es un número y es <= 300, lo permitimos
        
        return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

    def solo_numeros_coordenada_y(self, texto_nuevo):  # valida lo que se escribe en y (solo numeros hasta 125)
            if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                return True  # el cuadro vacio es valido
            
            if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                
                valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                
                if valor > 125: # se verifica si se pada el limite
                    # se muestra la ventana de advertencia
                    messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")  # avisa que el valor no es valido
                    return False # Rechazamos el ingreso de ese número
                
                return True # Si es un número y es <= 300, lo permitimos
            
            return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

   # def ejecutar_y_abrir_panel(self):
      #  if not self.verificar_coordenadas():
       #     return
       # self.raiz.withdraw()
        #ventana_panel = tk.Toplevel(self.raiz)
      #  panel_de_control(ventana_panel, self.raiz)

    def ejecutar_y_abrir_panel(self):  # se ejecuta al presionar "Ejecutar" en modo coordenadas
    #  simplemente comprobamos aquí
        texto_x = self.ingresar_coordenadas.get()  # lee el texto escrito en x (siempre es texto)
        texto_y = self.ingresar_coordenadasy.get()  # lee el texto escrito en y

        if texto_x == "" or texto_y == "":  # si el texto no se ingresa en uno de los 2 cuadros de texto se van a ececutar estas lineas de codigo
        # mostramos la misma advertencia que ya usabas
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese los valores de x y y antes de presionar Ejecutar.")  # avisa que faltan datos
            return  # sale de la funcion sin abrir el panel

        x_mm = int(texto_x)    # texto -> numero entero (mm del motor 1)
        angulo = int(texto_y) * GRADOS_POR_MM   # y en mm -> grados del motor 2, usando la regla temporal GRADOS_POR_MM
        self.raiz.withdraw()  # oculta la ventana de coordenadas
        ventana_panel = tk.Toplevel(self.raiz)  # crea la ventana del panel
        panel_de_control(ventana_panel, self.raiz, x_mm, angulo)   # abre el panel pasandole los mm del motor 1 y los grados del motor 2


    # Si pasa la comprobación, ocultamos esta ventana y abrimos el panel 
    
    # falta que nomas se pongan numeros en la coordenada y pero no conozco hasta cuanto se tiene que poner 
    # tambien me falta hacer una declaracion porque 


class ventana_modo_triangular:  # ventana donde se escribe la hipotenusa y el angulo
    def __init__(self, ventana_triangular, ventana_origen):  # recibe su ventana y la ventana principal
        self.ventana_origen = ventana_origen  # guarda la ventana principal para poder volver a ella
        self.raiz = ventana_triangular  # guarda la ventana propia del modo triangular

        self.valor_hipotenusa = tk.StringVar() # llamamos a la funcion el stringvar porque actua como un espia para el calculo automatico
        self.valor_angulo = tk.StringVar()  # otro espia, este vigila lo que se escribe en el angulo
                
        self.valor_hipotenusa.trace_add("write", self.calcular_automatico) # se le ordena ejecutar la funcion cada que el usuario escriba 
        self.valor_angulo.trace_add("write", self.calcular_automatico) # el trace add son palabras exclusivas

        self.raiz.title("MODO TRIANGULAR")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

        self.texto_triangular = tk.Label(self.raiz, text = "MODO TRIANGULAR",  font=("Arial 24"), fg="black", bg="sky blue")  # titulo de la ventana
        self.texto_triangular.pack(pady = 50)  #tamaño del texto
        self.texto_triangular.place(x=560 , y=50) # ubico el tamaño del texto

        self.texto__hipotenusa = tk.Label(self.raiz, text= "Ingrese el valor de la hipotenusa \n (por lo pronto 100 milimetros max)", font=("Arial 18"), fg="black", bg="sky blue")  # texto que pide la hipotenusa
        self.texto__hipotenusa.pack(pady = 50)  #tamaño del texto
        self.texto__hipotenusa.place(x=300 , y=140) # ubico el tamaño del texto

        self.validar_comando1 = self.raiz.register(self.solo_numeros_hipotenusa)  # registra la funcion que valida la hipotenusa

        self.ingresar_valor_hipotenusa = tk.Entry(self.raiz, font=("Arial 16"), textvariable= self.valor_hipotenusa, validate = "key", validatecommand=(self.validar_comando1, "%P") )  # cuadro de la hipotenusa conectado a su espia
        self.ingresar_valor_hipotenusa.pack()  # lo agrega a la ventana
        self.ingresar_valor_hipotenusa.place(x = 350 , y = 200)  # posicion del cuadro de la hipotenusa

        self.ingresar_angulo = tk.Label(self.raiz, text= "Ingresa el valor del angulo", font = ("Arial 18"), fg="black", bg="sky blue")  # texto que pide el angulo
        self.ingresar_angulo.pack(pady = 50)  # lo agrega a la ventana
        self.ingresar_angulo.place( x= 320 , y = 250)  # posicion del texto del angulo

        self.validar_comando = self.raiz.register(self.solo_numeros)  # registra la funcion que valida el angulo (maximo 360)

        self.ingresar_texto_angulo = tk.Entry(self.raiz, font = ("Arial 16"), textvariable = self.valor_angulo, validate= "key", validatecommand=(self.validar_comando, '%P'))  # cuadro del angulo conectado a su espia
        self.ingresar_texto_angulo.pack()  # lo agrega a la ventana
        self.ingresar_texto_angulo.place(x = 350 , y = 300)  # posicion del cuadro del angulo

        self.texto_del_desplazamientox =tk.Label(self.raiz, text = "El desplazamiento en el eje x sera",  font = ("Arial 18"), fg="black", bg="sky blue")  # texto del resultado en x
        self.texto_del_desplazamientox.pack()  # lo agrega a la ventana
        self.texto_del_desplazamientox.place(x = 800 , y = 140)  # posicion del texto

        self.desplazamiento = tk.Entry(self.raiz, font = ("Arial 18"))  # cuadro donde aparece el desplazamiento en x calculado
        self.desplazamiento.pack()  # lo agrega a la ventana
        self.desplazamiento.place(x = 840 , y = 190)  # posicion del cuadro

        self.texto_desplazamientoy = tk.Label(self.raiz, text ="El desplazamiento en el eje y sera", font= ("Arial 18"), fg="black", bg="sky blue")  # texto del resultado en y
        self.texto_desplazamientoy.pack()  # lo agrega a la ventana
        self.texto_desplazamientoy.place(x = 800, y = 250)  # posicion del texto

        self.desplazamiento_en_y = tk.Entry(self.raiz, font = "Arial 18")  # cuadro donde aparece el desplazamiento en y calculado
        self.desplazamiento_en_y.pack()  # lo agrega a la ventana
        self.desplazamiento_en_y.place(x = 840 , y = 300)  # posicion del cuadro

        self.boton_ejecutar_operacion = tk.Button(self.raiz, text = "Ejecutar", font = ("Arial 16"), padx = 20, pady= 10,command=self.ejecutar_y_abrir_panel)  # boton que abre el panel y mueve los motores
        self.boton_ejecutar_operacion.place(x = 615 , y = 450)  # posicion del boton ejecutar
        self.boton_ejecutar_operacion.config(bd = 20)  # grosor del borde del boton
        self.boton_ejecutar_operacion.config(relief= "groove")  # estilo del borde del boton
        self.boton_ejecutar_operacion.config(bg = "green")  # color de fondo del boton

        self.volver_menu_principal = tk.Button(self.raiz, text = "volver al menu principal",font = ("Arial 16"), padx = 30, pady= 10, command=self.regresar)  # boton para volver al menu
        self.volver_menu_principal.place(x = 1000 , y = 700)  # posicion del boton volver
        self.volver_menu_principal.config(bd = 20)  # grosor del borde del boton
        self.volver_menu_principal.config(relief = "groove")  # estilo del borde del boton
        self.volver_menu_principal.config(bg = "red")  # color de fondo del boton

      # --- FUNCIONES ADICIONALES DE LA VENTANA ---
    def regresar(self):  # se ejecuta al presionar "volver al menu principal"
        self.raiz.destroy() # cierra esta ventana
        self.ventana_origen.deiconify() # muestra la ventana principal

    def calcular_automatico(self, *args):  # calcula x y y cada vez que se escribe algo en hipotenusa o angulo
        try:  # intenta calcular; si algo sale mal salta a "except"
            texto_hip = self.valor_hipotenusa.get()  # lee el texto de la hipotenusa
            texto_ang = self.valor_angulo.get()  # lee el texto del angulo
            
            # Si borran el texto, vaciamos los resultados
            if texto_hip == "" or texto_ang == "":  # si falta alguno de los dos datos
                self.desplazamiento.delete(0, tk.END)  # borra el resultado de x
                self.desplazamiento_en_y.delete(0, tk.END)  # borra el resultado de y
                return  # termina la funcion
            
            # Convertimos el texto a números con decimales
            hip = float(texto_hip)  # hipotenusa como numero con decimales
            ang = float(texto_ang)  # angulo como numero con decimales
            
            # Fórmulas trigonométricas (convertimos a radianes primero)
            ang_rad = math.radians(ang)  # convierte el angulo de grados a radianes
            val_x = hip * math.cos(ang_rad)  # lado adyacente: hipotenusa por coseno del angulo
            val_y = hip * math.sin(ang_rad)  # lado opuesto: hipotenusa por seno del angulo
            
            # Tu regla especial: si termina en <= .5 se queda abajo, si es .6 sube.
            def redondear_especial(valor):  # funcion interna que redondea con la regla especial
                entero = int(valor)  # parte entera del numero
                decimal = abs(valor - entero)  # parte decimal sin signo
                if decimal <= 0.5:  # si el decimal es .5 o menos
                    return entero  # se queda en el entero (baja)
                else:  # si el decimal es mayor a .5
                    return entero + 1 if valor > 0 else entero - 1  # sube si es positivo, baja si es negativo
            
            # Aplicamos tu regla de redondeo
            val_x_redondeado = redondear_especial(val_x)  # redondea el valor de x
            val_y_redondeado = redondear_especial(val_y)  # redondea el valor de y
            
            # Escribimos los resultados en los cuadros de la derecha
            self.desplazamiento.delete(0, tk.END)  # limpia el cuadro de x
            self.desplazamiento.insert(0, str(val_x_redondeado))  # escribe el resultado de x
            
            self.desplazamiento_en_y.delete(0, tk.END)  # limpia el cuadro de y
            self.desplazamiento_en_y.insert(0, str(val_y_redondeado))  # escribe el resultado de y
            
        except ValueError:  # si escriben algo que no se puede convertir a numero
            # Si escriben letras por accidente, ignoramos el error para que no explote
            pass  # no hace nada

    #def verificar_triangulo(self):
      #  # Usamos tus variables espía para leer el contenido actual
       # hip = self.valor_hipotenusa.get()
       # ang = self.valor_angulo.get()
        
       # if hip == "" or ang == "":
          #  messagebox.showwarning("Campos vacíos", "Por favor, ingrese el valor de la hipotenusa y el ángulo antes de presionar Ejecutar.")
      #  else:
            # Como el cálculo ya lo hicimos automático con trace_add, aquí no es necesario hacer matemáticas, 
            # pero el botón cumple la función de validar que no falten datos.
          #  pass


    def solo_numeros(self, texto_nuevo):  # valida lo que se escribe en el angulo (solo numeros hasta 360)
                    if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                        return True  # el cuadro vacio es valido
                    
                    if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                        
                        valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                        
                        if valor > 360: # se verifica si se pada el limite
                            # se muestra la ventana de advertencia
                            messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")  # avisa que el valor no es valido
                            return False # Rechazamos el ingreso de ese número
                        
                        return True # Si es un número y es <= 360, lo permitimos
                    
                    return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

    
    def solo_numeros_hipotenusa(self, texto_nuevo):  # valida lo que se escribe en la hipotenusa (solo numeros hasta 100)
            if texto_nuevo == "":  # si despues de que el usuario cometetiera el error le permitimos que corriga el error
                return True  # el cuadro vacio es valido
            
            if texto_nuevo.isdigit():  # aqui se revisa si lo que se escribio fueron numeros
                
                valor = int(texto_nuevo) #se convierte el texto a un numero entero para que se compare
                
                if valor > 100: # se verifica si se pada el limite
                    # se muestra la ventana de advertencia
                    messagebox.showwarning("Valor inválido", "Los caracteres numericos que se ingresaron no son validos, por favor ingrese de nuevo los caracteres numericos")  # avisa que el valor no es valido
                    return False # Rechazamos el ingreso de ese número
                
                return True # Si es un número y es <= 300, lo permitimos
            
            return False   # Si el usuario intentó escribir letras o símbolos, lo rechazamos

    def ejecutar_y_abrir_panel(self):  # se ejecuta al presionar "Ejecutar" en modo triangular
        # No modificamos verificar_coordenadas() — simplemente comprobamos aquí
            hip = self.valor_hipotenusa.get()  # lee la hipotenusa escrita
            ang = self.valor_angulo.get()  # lee el angulo escrito
    
            if hip == "" or ang == "":  # si falta alguno de los dos datos
            # mostramos la misma advertencia que ya usabas
                messagebox.showwarning("Campos vacíos", "Por favor, ingrese los valores de x y y antes de presionar Ejecutar.")  # avisa que faltan datos
                return  # sale de la funcion sin abrir el panel
            x_mm = int(self.desplazamiento.get() or 0)   # desplazamiento en x ya calculado (mm del motor 1)
            angulo = int(ang)   # angulo escrito, en grados enteros (lo recibe el motor 2)
            self.raiz.withdraw()  # oculta la ventana del modo triangular
            ventana_panel = tk.Toplevel(self.raiz)  # crea la ventana del panel
            panel_de_control(ventana_panel, self.raiz, x_mm, angulo)   # abre el panel pasandole los mm y los grados
    
     # me falta ajustar que nomas se ingresen nuneros en la hipotenusa pero no conosco su valor maximo mejor despues de lo pongo        
        
class panel_de_control:  # ventana del panel: muestra los datos de los 2 motores y los mueve
    def __init__(self, ventana_panel, ventana_origen, x_mm=0, angulo=0):   # recibe los mm del motor 1 y los grados del motor 2

        self.raiz = ventana_panel  # guarda la ventana del panel
        self.ventana_origen = ventana_origen  # guarda la ventana de la que venimos para poder volver
        
        self.raiz.title("panel de control")   #se le pone el nombre a la ventana
        self.raiz.resizable(False,False)  #se bloquea el ajuste de la ventana
        self.raiz.geometry("1400x850")   #tamaño de la ventana
        self.raiz.config(bg="sky blue") # defino el color celeste como fondo de pantalla

       # self.tabla_panel = ttk.Treeview(self.raiz, columns=("col1"))

        #self.tabla_panel.column("#0" , width = 400 , anchor = "center")
        #self.tabla_panel.column("col1", width = 400 , anchor = "center")
        #self.tabla_panel.heading("#0", text= "Motor de desplazamiento lineal", anchor= "center")
        #self.tabla_panel.heading("col1", text = "Motor de desplazamiento angular", anchor = "center")
        #self.tabla_panel.place( x= 100 , y = 150, width= 800 , height= 500)

        # ---------- COLUMNA IZQUIERDA: MOTOR 1 (desplazamiento lineal X) ----------
        self.celda_motor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "desplazamiento lineal"
        self.celda_motor_lineal.place(x=100, y=100, width=400, height=50)  # posicion y tamaño del cuadro
        self.texto_motor_lineal = tk.Label(self.celda_motor_lineal, text=" DESPLAZAMIENTO LINEAL X", font=("Arial", 16, "bold"), fg="blue", bg="white")  # titulo del cuadro
        self.texto_motor_lineal.place(x=30, y=10)  # posicion del titulo dentro del cuadro

        self.valor_motor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor en mm
        self.valor_motor_lineal.place(x = 100, y = 150, width = 400 , height = 152)  # posicion y tamaño del cuadro
        self.texto_valor_motor_lineal = tk.Label(self.valor_motor_lineal,text=" 39 mm", font=("Arial", 50, "bold"), fg="blue", bg="white")  # texto del valor en mm (luego se actualiza)
        self.texto_valor_motor_lineal.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        self.revolucion_motor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "revolucion"
        self.revolucion_motor_lineal.place(x=100, y= 300, width=400, height=50)  # posicion y tamaño del cuadro
        self.texto_valor_revolucion_ml = tk.Label(self.revolucion_motor_lineal, text="REVOLUCION DEL MOTOR EJE X", font=("Arial", 16, "bold"), fg="red", bg="white")  # titulo del cuadro
        self.texto_valor_revolucion_ml.place(x = 20 , y = 10)  # posicion del titulo dentro del cuadro

        self.valor_revolucion_ml = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor de revoluciones
        self.valor_revolucion_ml.place(x = 100, y = 350, width = 400 , height = 100)  # posicion y tamaño del cuadro
        self.texto_valor_revolucion_ml =tk.Label(self.valor_revolucion_ml,text=" 40 rev", font=("Arial", 40, "bold"), fg="red", bg="white")  # texto de revoluciones (luego se actualiza)
        self.texto_valor_revolucion_ml.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        self.pasos_motor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "pasos"
        self.pasos_motor_lineal.place(x = 100 , y = 450, width= 400 , height=50)  # posicion y tamaño del cuadro
        self.texto_pasos_motor_lineal = tk.Label(self.pasos_motor_lineal, text=" PASOS DEL MOTOR EJE X", font=("Arial", 16, "bold"), fg="green", bg="white")  # titulo del cuadro
        self.texto_pasos_motor_lineal.place(x = 30 , y=10)  # posicion del titulo dentro del cuadro

        self.valor_pasos_ml = tk.Frame(self.raiz,  bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor de pasos
        self.valor_pasos_ml.place(x = 100 , y= 500, width= 400 , height= 100 )  # posicion y tamaño del cuadro
        self.texto_valor_pasos_ml = tk.Label(self.valor_pasos_ml,text=" 10 pasos", font=("Arial", 40, "bold"), fg="green", bg="white")  # texto de pasos (luego se actualiza)
        self.texto_valor_pasos_ml.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        # ---------- COLUMNA DERECHA: MOTOR 2 (desplazamiento angular) ----------
        self.celda_motor_angular = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "desplazamiento angular"
        self.celda_motor_angular.place(x = 500, y = 100, width = 400 , height = 50)  # posicion y tamaño del cuadro
        self.texto_motor_angular = tk.Label(self.celda_motor_angular, text=" DESPLAZAMIENTO ANGULAR ", font=("Arial", 16, "bold"), fg="blue", bg="white" )  # titulo del cuadro
        self.texto_motor_angular.place( x= 30 , y=10)  # posicion del titulo dentro del cuadro

        self.valor_motor_angular = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor en grados
        self.valor_motor_angular.place(x = 500, y = 150, width = 400 , height = 152)  # posicion y tamaño del cuadro
        self.texto_valor_motor_angular = tk.Label(self.valor_motor_angular, text=" 50 °", font=("Arial", 50, "bold"), fg="blue", bg="white")  # texto del valor en grados (luego se actualiza)
        self.texto_valor_motor_angular.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        self.revolucion_motor_angular = tk.Frame(self.raiz,  bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "revoluciones"
        self.revolucion_motor_angular.place(x=500, y= 300, width=400, height=50)  # posicion y tamaño del cuadro
        self.texto_revolucion_ma = tk.Label(self.revolucion_motor_angular, text="REVOLUCIONES DEL MOTOR EJE Y ", font=("Arial", 16, "bold"), fg="red", bg="white")  # titulo del cuadro
        self.texto_revolucion_ma.place( x= 20 , y=15)  # posicion del titulo dentro del cuadro

        self.valor_revolucion_ma = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor de revoluciones
        self.valor_revolucion_ma.place(x = 500, y = 350, width = 400 , height = 100)  # posicion y tamaño del cuadro
        self.texto_valor_revolucion_ma =tk.Label(self.valor_revolucion_ma,text=" 20 rev", font=("Arial", 40, "bold"), fg="red", bg="white")  # texto de revoluciones (luego se actualiza)
        self.texto_valor_revolucion_ma.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        self.pasos_motor_y =tk.Frame(self.raiz,  bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "pasos"
        self.pasos_motor_y.place(x = 500, y = 450, width = 400 , height = 50)  # posicion y tamaño del cuadro
        self.texto_pasos_motory = tk.Label(self.pasos_motor_y, text="PASOS DEL MOTOR EJE Y", font=("Arial", 16, "bold"), fg="green", bg="white")  # titulo del cuadro
        self.texto_pasos_motory.place(x = 30, y = 10)  # posicion del titulo dentro del cuadro

        self.valor_pasos_motory = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor de pasos
        self.valor_pasos_motory.place(x = 500, y = 500, width = 400 , height = 100)  # posicion y tamaño del cuadro
        self.texto_pasos_motory = tk.Label(self.valor_pasos_motory, text="20 pasos", font=("Arial", 40, "bold"), fg="green", bg="white")  # texto de pasos (luego se actualiza); reutiliza el nombre del titulo
        self.texto_pasos_motory.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

      #  self.sensor_distancia_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)
      #  self.sensor_distancia_lineal.place(x = 1000, y = 50, width = 300 , height = 75)
      #  self.sensor_lineal = tk.Label(self.sensor_distancia_lineal,  text="SENSOR DE DISTANCIA \n LINEAL ", font=("Arial", 14, "bold"), fg="black", bg="white")
      #  self.sensor_lineal.place(x = 40 , y =10)

      #  self.texto_distancia_lineal =tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)
       # self.texto_distancia_lineal.place(x = 1000 , y = 120, width = 300 , height = 50)
       # self.textdis = tk.Label(self.texto_distancia_lineal, text="DISTANCIA ", font=("Arial", 14, "bold"), fg="black", bg="white")
       # self.textdis.place(x = 100 , y = 10)
       # self.valor_sensor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)
       # self.valor_sensor_lineal.place(x = 1000, y = 170, width=300, height=100)
        #aqui se va a introduccir el valor del sensor lineal en mm

       # self.estado_sensor_lineal = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)
       # self.estado_sensor_lineal.place(x = 1000, y = 250, width=300, height=50)
      #  self.texto_estado_sensor_lineal = tk.Label(self.estado_sensor_lineal, text="ESTADO DEL  SENSOR ", font=("Arial", 14, "bold"), fg="black", bg="white" )
      #  self.texto_estado_sensor_lineal.place(x = 40, y = 10)
      #  self.valor_estado_sensor_lin = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)
      #  self.valor_estado_sensor_lin.place(x = 1000, y = 300, width=300, height=50)
        #aqui se va a introduccir el estado del sensor

        # ---------- SENSOR DE DISTANCIA LINEAL 1 (por ahora con valores de ejemplo) ----------
        self.sensor_distancia_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo del sensor 1
        self.sensor_distancia_lineal.place(x = 950, y = 50, width = 200 , height = 75)  # posicion y tamaño del cuadro
        self.sensor_lineal = tk.Label(self.sensor_distancia_lineal,  text="SENSOR DE DISTANCIA \n LINEAL ", font=("Arial", 10, "bold"), fg="black", bg="white")  # titulo del sensor 1
        self.sensor_lineal.place(x = 20 , y =10)  # posicion del titulo dentro del cuadro

        self.texto_distancia_lineal =tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro de la palabra "distancia"
        self.texto_distancia_lineal.place(x = 950 , y = 120, width = 200 , height = 50)  # posicion y tamaño del cuadro
        self.textdis = tk.Label(self.texto_distancia_lineal, text="DISTANCIA ", font=("Arial", 10, "bold"), fg="black", bg="white")  # palabra "distancia"
        self.textdis.place(x = 50 , y = 10)  # posicion del texto dentro del cuadro
        self.valor_sensor_lineal = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor del sensor 1
        self.valor_sensor_lineal.place(x = 950, y = 170, width=200, height=100)  # posicion y tamaño del cuadro
        self.texto_valor_sensor_lineal = tk.Label(self.valor_sensor_lineal, text="15 mm ", font=("Arial",24 , "bold"), fg="black", bg="white" )  # valor de ejemplo del sensor 1
        self.texto_valor_sensor_lineal.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro
        
        self.estado_sensor_lineal = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "estado del sensor"
        self.estado_sensor_lineal.place(x = 950, y = 250, width=200, height=50)  # posicion y tamaño del cuadro
        self.texto_estado_sensor_lineal = tk.Label(self.estado_sensor_lineal, text="ESTADO DEL  SENSOR ", font=("Arial", 10, "bold"), fg="black", bg="white" )  # titulo del cuadro
        self.texto_estado_sensor_lineal.place(x = 20, y = 10)  # posicion del titulo dentro del cuadro
        self.valor_estado_sensor_lin = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del estado del sensor 1
        self.valor_estado_sensor_lin.place(x = 950, y = 300, width=200, height=50)  # posicion y tamaño del cuadro
        self.texto_valor_estado_sensor_lin =tk.Label(self.valor_estado_sensor_lin, text="BUENO ", font=("Arial", 16, "bold"), fg="black", bg="white")  # estado de ejemplo del sensor 1
        self.texto_valor_estado_sensor_lin.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro
        #################################################################################################################################
        ###################################################################################################################################
        # ---------- SENSOR DE DISTANCIA LINEAL 2 (por ahora con valores de ejemplo) ----------
        self.sensor_distancia_lineal2 = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo del sensor 2
        self.sensor_distancia_lineal2.place(x = 1150, y = 50, width = 200 , height = 75)  # posicion y tamaño del cuadro
        self.sensor_lineal2 = tk.Label(self.sensor_distancia_lineal2,  text="SENSOR DE DISTANCIA \n LINEAL 2 ", font=("Arial", 10, "bold"), fg="black", bg="white")  # titulo del sensor 2
        self.sensor_lineal2.place(x = 20 , y =10)  # posicion del titulo dentro del cuadro
        
        self.texto_distancia_lineal2 =tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro de la palabra "distancia"
        self.texto_distancia_lineal2.place(x = 1150 , y = 120, width = 200 , height = 50)  # posicion y tamaño del cuadro
        self.textdis2 = tk.Label(self.texto_distancia_lineal2, text="DISTANCIA ", font=("Arial", 10, "bold"), fg="black", bg="white")  # palabra "distancia"
        self.textdis2.place(x = 50 , y = 10)  # posicion del texto dentro del cuadro
        self.valor_sensor_lineal2 = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor del sensor 2
        self.valor_sensor_lineal2.place(x = 1150, y = 170, width=200, height=100)  # posicion y tamaño del cuadro
        self.texto_valor_sensor_lineal2 =tk.Label(self.valor_sensor_lineal2,text="10 mm ", font=("Arial",24 , "bold"), fg="black", bg="white")  # valor de ejemplo del sensor 2
        self.texto_valor_sensor_lineal2.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro
                
        self.estado_sensor_lineal2 = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "estado del sensor"
        self.estado_sensor_lineal2.place(x = 1150, y = 250, width=200, height=50)  # posicion y tamaño del cuadro
        self.texto_estado_sensor_lineal2 = tk.Label(self.estado_sensor_lineal2, text="ESTADO DEL  SENSOR ", font=("Arial", 10, "bold"), fg="black", bg="white" )  # titulo del cuadro
        self.texto_estado_sensor_lineal2.place(x = 20, y = 10)  # posicion del titulo dentro del cuadro
        self.valor_estado_sensor_lin2 = tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del estado del sensor 2
        self.valor_estado_sensor_lin2.place(x = 1150, y = 300, width=200, height=50)  # posicion y tamaño del cuadro
        self.texto_valor_estado_sensor_lin2 =tk.Label(self.valor_estado_sensor_lin2,text="BUENO ", font=("Arial", 16, "bold"), fg="black", bg="white")  # estado de ejemplo del sensor 2
        self.texto_valor_estado_sensor_lin2.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        # ---------- SENSOR DE DISTANCIA ANGULAR (por ahora con valores de ejemplo) ----------
        self.sensor_distancia_angular =tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo del sensor angular
        self.sensor_distancia_angular.place(x = 1000, y = 400, width = 300 , height = 75)  # posicion y tamaño del cuadro
        self.sensortexto_distancia_angular = tk.Label(self.sensor_distancia_angular,  text="SENSOR DE DISTANCIA \n ANGULAR ", font=("Arial", 14, "bold"), fg="black", bg="white")  # titulo del sensor angular
        self.sensortexto_distancia_angular.place(x = 40 , y =10)  # posicion del titulo dentro del cuadro

        self.grados_angulares= tk.Frame(self.raiz,bg="white", highlightbackground="black", highlightthickness=2)  # cuadro de la palabra "grados"
        self.grados_angulares.place(x = 1000, y = 470, width = 300 , height = 50)  # posicion y tamaño del cuadro
        self.texto_grados_angulares = tk.Label(self.grados_angulares,text="GRADOS ", font=("Arial", 14, "bold"), fg="black", bg="white")  # palabra "grados"
        self.texto_grados_angulares.place(x=100 , y=10)  # posicion del texto dentro del cuadro

        self.valor_grados_angulares = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del valor en grados del sensor
        self.valor_grados_angulares.place(x = 1000, y = 520, width = 300 , height = 100)  # posicion y tamaño del cuadro
        self.texto_valor_grados_angulares = tk.Label(self.valor_grados_angulares, text="40° ", font=("Arial", 40, "bold"), fg="black", bg="white")  # valor de ejemplo del sensor angular
        self.texto_valor_grados_angulares.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        self.estado_del_sensor_angular = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del titulo "estado del sensor"
        self.estado_del_sensor_angular.place(x = 1000, y = 600, width = 300 , height = 50)  # posicion y tamaño del cuadro
        self.estado_del_sensor_angular = tk.Label(self.estado_del_sensor_angular, text="ESTADO DEL SENSOR ", font=("Arial", 14, "bold"), fg="black", bg="white" )  # titulo del cuadro (reutiliza el nombre del cuadro)
        self.estado_del_sensor_angular.place(x=40, y=10)  # posicion del titulo dentro del cuadro

        self.valor_estado_sensoran = tk.Frame(self.raiz, bg="white", highlightbackground="black", highlightthickness=2)  # cuadro del estado del sensor angular
        self.valor_estado_sensoran.place(x = 1000, y = 650, width=300, height=50)  # posicion y tamaño del cuadro
        self.texto_valor_estado_sensoran = tk.Label(self.valor_estado_sensoran, text="BUENO", font=("Arial", 20, "bold"), fg="black", bg="white" )  # estado de ejemplo del sensor angular
        self.texto_valor_estado_sensoran.place(relx=0.5, rely=0.5, anchor="center")  # lo centra dentro del cuadro

        # ---------- BOTONES ----------
        self.volver_menu_principal = tk.Button(self.raiz, text = "Regresar",font = ("Arial 16"), padx = 30, pady= 10, command= self.regresar)  # boton para salir del panel
        self.volver_menu_principal.place(x = 1000 , y = 740)  # posicion del boton regresar
        self.volver_menu_principal.config(bd = 20)  # grosor del borde del boton
        self.volver_menu_principal.config(relief = "groove")  # estilo del borde del boton
        self.volver_menu_principal.config(bg = "red")  # color de fondo del boton

        self.volver_menu_principal = tk.Button(self.raiz, text = "Regresar a home",font = ("Arial 16"), padx = 30, pady= 10, )  # boton "regresar a home" (todavia no tiene funcion)
        self.volver_menu_principal.place(x = 550 , y = 630)  # posicion del boton
        self.volver_menu_principal.config(bd = 20)  # grosor del borde del boton
        self.volver_menu_principal.config(relief = "groove")  # estilo del borde del boton
        self.volver_menu_principal.config(bg = "yellow")  # color de fondo del boton

        # ---------- CONVERSION A PASOS Y ENVIO A LOS MOTORES ----------
        self.pasos_x = round(x_mm / MM_POR_REV * PASOS_POR_REV)   # motor 1: mm -> vueltas (mm / mm por vuelta) -> pasos (vueltas * pasos por vuelta)
        self.pasos_y = round(angulo / 360 * PASOS_POR_REV * RELACION_ENGRANE)   # motor 2: grados -> fraccion de vuelta (grados / 360) -> pasos (con RELACION_ENGRANE = 1 es directo)

        self.mostrar_valores(0, 0)   # al empezar, los dos motores van en 0 y los valores suben en tiempo real
        self.mostrar_sensores(None, None, None, None)   # los sensores empiezan en "sin datos" hasta que llegue la primera lectura

        self.texto_estado = tk.Label(self.raiz, text=f"Moviendo... (objetivo: {self.pasos_x} y {self.pasos_y} pasos)", font=("Arial", 16, "bold"), bg="sky blue")   # texto de estado con los pasos que debe dar cada motor
        self.texto_estado.place(x=100, y=640)   # posicion del texto de estado

        # tiempo estimado que tarda el motor mas largo + 5 s de margen
        self.limite = max(abs(self.pasos_x), abs(self.pasos_y)) / (PASOS_POR_REV * VELOCIDAD_RPM / 60) + 5   # pasos del motor mas largo / pasos por segundo + 5 s
        self.inicio = time.time()   # guarda la hora a la que empezo el movimiento
        self.moviendo = True   # marca que los motores estan en movimiento
        self.trabajo = None   # aqui se guarda la tarea programada con after

        motores.mover(self.pasos_x, self.pasos_y)   # manda los pasos de los 2 motores a la placa
        self.revisar_motor()   # empieza a leer el avance de la placa

    def mostrar_valores(self, pasos_x, pasos_y):   # actualiza los 6 cuadros a partir de los pasos que lleva cada motor
        rev_x = pasos_x / PASOS_POR_REV   # motor 1: pasos -> revoluciones del motor
        mm = rev_x * MM_POR_REV   # motor 1: revoluciones -> mm recorridos
        rev_y = pasos_y / PASOS_POR_REV   # motor 2: pasos -> revoluciones del motor
        grados = pasos_y * 360 / (PASOS_POR_REV * RELACION_ENGRANE)   # motor 2: pasos -> grados recorridos (es la conversion de envio al reves)

        self.texto_valor_motor_lineal.config(text=f"{mm:.1f} mm")   # muestra el desplazamiento lineal con 1 decimal
        self.texto_valor_revolucion_ml.config(text=f"{rev_x:.3f} rev")   # muestra las revoluciones del motor 1 con 3 decimales
        self.texto_valor_pasos_ml.config(text=f"{pasos_x} pasos")   # muestra los pasos del motor 1

        self.texto_valor_motor_angular.config(text=f"{grados:.1f} °")   # muestra el desplazamiento angular con 1 decimal
        self.texto_valor_revolucion_ma.config(text=f"{rev_y:.3f} rev")   # muestra las revoluciones del motor 2 con 3 decimales
        self.texto_pasos_motory.config(text=f"{pasos_y} pasos")   # muestra los pasos del motor 2

    def mostrar_distancia(self, texto_valor, texto_estado, distancia):   # muestra la lectura de un VL53L0X en sus 2 cuadros
        if distancia is None:   # si todavia no llega ningun dato de la placa
            texto_valor.config(text="---")   # no hay valor que mostrar
            texto_estado.config(text="SIN DATOS")   # avisa que no hay datos
        elif distancia >= 0:   # si es una lectura valida (en mm)
            texto_valor.config(text=f"{distancia} mm")   # muestra la distancia
            texto_estado.config(text="BUENO")   # el sensor funciona bien
        elif distancia == -2:   # si el objeto esta mas lejos de lo que el sensor puede medir
            texto_valor.config(text="---")   # no hay valor que mostrar
            texto_estado.config(text="FUERA RANGO")   # avisa que esta fuera de rango
        else:   # si es -1, el sensor no responde
            texto_valor.config(text="---")   # no hay valor que mostrar
            texto_estado.config(text="ERROR")   # avisa que el sensor falla

    def mostrar_sensores(self, dist1, dist2, angulo10, estado_iman):   # actualiza los 3 sensores del panel
        self.mostrar_distancia(self.texto_valor_sensor_lineal, self.texto_valor_estado_sensor_lin, dist1)   # sensor de distancia 1
        self.mostrar_distancia(self.texto_valor_sensor_lineal2, self.texto_valor_estado_sensor_lin2, dist2)   # sensor de distancia 2
        if angulo10 is None or angulo10 < 0:   # si no hay dato o hubo error en el AS5600
            self.texto_valor_grados_angulares.config(text="---")   # no hay valor que mostrar
        else:   # si hay una lectura valida
            self.texto_valor_grados_angulares.config(text=f"{angulo10 / 10:.1f}°")   # el dato viene en decimas de grado, se divide entre 10
        estados = {0: "BUENO", 1: "SIN IMAN", 2: "IMAN DEBIL", 3: "IMAN FUERTE", 4: "ERROR"}   # texto para cada codigo de estado del AS5600
        self.texto_valor_estado_sensoran.config(text=estados.get(estado_iman, "SIN DATOS"))   # muestra el estado; si no hay dato, "SIN DATOS"

    def revisar_motor(self):      # se ejecuta cada 50 ms mientras el panel este abierto: lee la placa y actualiza la pantalla
        avance, termino, sensores = motores.leer()   # lee lo que mando la placa: avance de motores, si termino y sensores
        if avance:   # si llego un avance nuevo de los motores
            self.mostrar_valores(avance[0], avance[1])   # muestra los pasos que lleva cada motor en este momento
        if sensores:   # si llego una lectura nueva de los sensores
            self.mostrar_sensores(*sensores)   # muestra las distancias y el angulo (el * reparte los 4 datos como argumentos)
        if self.moviendo:   # solo mientras los motores estan en movimiento
            if termino:   # si la placa respondio OK
                self.moviendo = False   # ya no se estan moviendo
                self.mostrar_valores(self.pasos_x, self.pasos_y)   # muestra el valor final exacto
                self.texto_estado.config(text="Listo")   # muestra "Listo" en pantalla
            elif time.time() - self.inicio > self.limite:   # si paso mas tiempo del esperado sin respuesta
                self.moviendo = False   # deja de esperar
                self.texto_estado.config(text="La placa no respondio")   # avisa del problema en pantalla
        self.trabajo = self.raiz.after(50, self.revisar_motor)   # vuelve a revisar dentro de 50 ms (siempre, para que los sensores sigan en vivo)

    def regresar(self):  # se ejecuta al presionar "Regresar"
        if self.moviendo:         # no dejar salir mientras se mueven los motores
            messagebox.showwarning("Motor en movimiento", "Espera a que el motor termine.")   # avisa que hay que esperar
            return   # sale sin cerrar el panel
        self.raiz.destroy() # Destruye la ventana de coordenadas
        self.ventana_origen.deiconify() # Vuelve a hacer visible la ventana principal
        



motores = Motor(PUERTO, BAUDIOS)   # crea el objeto que habla con la placa (tarda 2 s en conectar)
if not motores.conectado():   # si no se encontro la placa
    print("No se encontro la placa, modo simulacion")   # avisa en la terminal

ventana_principal()   # abre la ventana del menu principal; el programa se queda aqui hasta que se cierre
