"""IMPORTACIONES"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, UnidentifiedImageError
import creapdf
import tkinter as tk
from tkinter import Toplevel
import os

"""INICIALIZACION DE VARIABLES, LISTAS, BANDERAS, CONFIGURACION DEL ROOT"""

# listas con las peliculas, salas, horarios
peliculas = ["Godzilla", "Scarface", "Titanic", "Venom"]
descripciones = [
    "Monstruo gigante ataca la ciudad",
    "Historia de un mafioso",
    "Romance en el mar",
    "Simbionte alienígena"
]
horarios = ["9:00", "15:00", "21:00"]
salas = ["Sala 1", "Sala 2", "Sala 3"]

peliculas_imagenes = [
    ("Godzilla", r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto\imagenes\logo_godzilla.png"),
    ("Scarface", r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto \imagenes\logo_scarface.png"),
    ("Titanic", r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto \imagenes\logo_titanic.png"),
    ("Venom", r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto \imagenes\MV5BNTFkZjdjN2QtOGE5MS00ZTgzLTgxZjAtYzkyZWQ5MjEzYmZjXkEyXkFqcGdeQXVyMTM0NTUzNDIy._V1_.png")
]

peliculas_repositorio = [
    ("Star Wars", r"C:\Users\ASUS I5\Downloads\starwars.jpg", "Batalla espacial épica"),
    ("Spiderman", r"C:\Users\ASUS I5\Downloads\spiderman.jpg", "Héroe arácnido"),
    ("Harry Potter", r"C:\Users\ASUS I5\Downloads\harry poter.jpg", "El niño que vivió"),
    ("Cars", r"C:\Users\ASUS I5\Downloads\cars.jpg", "Carrera de autos")
]

# Crear la estructura de datos para almacenar los horarios y las salas con asientos para el pdf
cine = {}
datos = {}
asientoslist = []
info = {}
asientoslist = []

# Ruta del html
ruta_template = r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto\codigo\proyecto\template.html"

# Definimos la función para inicializar una matriz de asientos
def inicializar_asientos(filas, columnas):
    return [["Libre" for _ in range(columnas)] for _ in range(filas)]

# Asignamos cada película con sus respectivos horarios, salas y asientos
for pelicula in peliculas:
    cine[pelicula] = {}
    for horario in horarios:
        cine[pelicula][horario] = {}
        for sala in salas:
            cine[pelicula][horario][sala] = inicializar_asientos(5, 5)  # 5x5 es el tamaño definido

# Configuración inicial de selección
pelicula_seleccionada = None
horario_seleccionado = None
sala_seleccionada = None
es_admin = False  # Variable para controlar el estado de la cuenta

# Configuración de apariencia de la aplicación
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Inicialización de la ventana principal
root = ctk.CTk()
root.title("Cine sin base de datos")
root.geometry("800x650")
root.resizable(False, False)


"""FUNCIONES QUE CONTROLAN EL PROGRAMA"""

# VALIDACION Y LOGIN 
def iniciar_login():
    limpiar_ventana()
    root.geometry("550x650")
    logo_claro_path = r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto\imagenes\logo_claro.png"
    logo_oscuro_path = r"C:\Users\ASUS I5\OneDrive\Desktop\proyecto\proyecto\proyecto\imagenes\logo_oscuro.png"
    
    try:
        logo = ctk.CTkImage(
            light_image=Image.open(logo_claro_path),
            dark_image=Image.open(logo_oscuro_path),
            size=(250, 250)
        )
        logo_widget = ctk.CTkLabel(root, image=logo, text="")
        logo_widget.pack(pady=15)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de logo.")
    except UnidentifiedImageError:
        messagebox.showerror("Error", "El archivo de logo no es una imagen válida.")
    
    # Entrada de usuario
    ctk.CTkLabel(root, text="Usuario").pack()
    usuario_entry = ctk.CTkEntry(root)
    usuario_entry.insert(0, "Ej. Laura")
    usuario_entry.bind("<Button-1>", lambda e: usuario_entry.delete(0, "end"))
    usuario_entry.pack()
    
    # Entrada de contraseña
    ctk.CTkLabel(root, text="Contraseña").pack()
    contraseña_entry = ctk.CTkEntry(root)
    contraseña_entry.insert(0, "")
    contraseña_entry.bind("<Button-1>", lambda e: contraseña_entry.delete(0, "end"))
    contraseña_entry.pack()
    
    # Botón de entrar
    ctk.CTkButton(root, text="Entrar", command=lambda: validar_credenciales(usuario_entry.get(), contraseña_entry.get())).pack(pady=10)

def validar_credenciales(usuario, contraseña):
    global es_admin
    if usuario == "user" and contraseña == "user":
        es_admin = False
        iniciar_programa()
    elif usuario == "admin" and contraseña == "admin":
        es_admin = True
        iniciar_programa()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# INICIO DEL PROGRAMA
def iniciar_programa():
    limpiar_ventana()
    mostrar_peliculas_principales()


# REGRESO AL LOGIN
def irlogin():
    limpiar_ventana()
    iniciar_login()


# PAGINA PRINCIPAL(MENU)

def mostrar_peliculas_principales():
    movie_frame = ctk.CTkFrame(master=root)
    movie_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.geometry("750x600")

    canvas = tk.Canvas(movie_frame)
    scrollbar = tk.Scrollbar(movie_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(master=canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for idx, (titulo, imagen) in enumerate(peliculas_imagenes):
        row, column = divmod(idx, 2)
        try:
            movie_image = ctk.CTkImage(light_image=Image.open(imagen), size=(150, 375))
            movie_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="gray20", width=300, height=500)
            movie_frame.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")

            movie_widget = ctk.CTkLabel(movie_frame, image=movie_image, text="")
            movie_widget.image = movie_image  # Prevent garbage collection
            movie_widget.pack(padx=10, pady=10)

            seleccionar_label = ctk.CTkLabel(movie_frame, text=f"{titulo}\n{descripciones[idx]}", font=("Arial", 16))
            seleccionar_label.pack(padx=10, pady=10)

            seleccionar_button = ctk.CTkButton(movie_frame, text="Seleccionar horario", command=lambda t=titulo, i=imagen: seleccionar_horario(t, i))
            seleccionar_button.pack(padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo de imagen: {imagen}")
        except UnidentifiedImageError:
            messagebox.showerror("Error", f"El archivo no es una imagen válida: {imagen}")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    cerrar_sesion_frame = ctk.CTkFrame(master=root)
    cerrar_sesion_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    cerrar_sesion = ctk.CTkButton(cerrar_sesion_frame, text="Cerrar sesión", command=irlogin)
    cerrar_sesion.grid(pady=10)

    if es_admin:
        agregar_peliculas = ctk.CTkButton(cerrar_sesion_frame, text="Agregar Películas", command=abrir_repositorio)
        agregar_peliculas.grid(pady=10)

        eliminar_peliculas = ctk.CTkButton(cerrar_sesion_frame, text="Eliminar Película", command=eliminar_pelicula)
        eliminar_peliculas.grid(pady=10)

# FUNCIONES DE CREACION DE VENTANAS PARA REPOSITORIO Y AGG

def abrir_repositorio():
    global repo_window
    repo_window = Toplevel(root)
    repo_window.title("Repositorio de Películas")
    repo_window.geometry("500x500")
    repo_window.configure(bg='black')  # Cambia el color de fondo de la ventana

    canvas = tk.Canvas(repo_window, bg='black')  # Cambia el color de fondo del canvas
    scrollbar = tk.Scrollbar(repo_window, orient="vertical", command=canvas.yview, bg='black')  # Cambia el color de fondo de la scrollbar
    scrollable_frame = ctk.CTkFrame(master=canvas, fg_color='black')  # Cambia el color de fondo del frame

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for idx, (titulo, imagen, descripcion) in enumerate(peliculas_repositorio):
        try:
            movie_image = ctk.CTkImage(light_image=Image.open(imagen), size=(100, 250))
            movie_widget = ctk.CTkLabel(scrollable_frame, image=movie_image, text=f"{titulo}\n{descripcion}", fg_color='black')
            movie_widget.image = movie_image  # Prevent garbage collection
            movie_widget.grid(row=idx, column=0, padx=10, pady=10)

            seleccionar_button = ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda t=titulo, i=imagen, d=descripcion: seleccionar_pelicula(t, i, d))
            seleccionar_button.grid(row=idx, column=1, padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo de imagen: {imagen}")
        except UnidentifiedImageError:
            messagebox.showerror("Error", f"El archivo no es una imagen válida: {imagen}")

    botton_elementos = ctk.CTkButton(scrollable_frame, text="Agregar más", command=aggelements_list_repowindows)
    botton_elementos.grid(row=len(peliculas_repositorio), column=0, columnspan=2, pady=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def aggelements_list_repowindows():
    limpiar_ventana_secundaria()
    ctk.CTkLabel(repo_window, text="Nombre de la pelicula", fg_color='black').pack()
    titulosx = ctk.CTkEntry(repo_window)
    titulosx.insert(0, "Ej. Los Increíbles")
    titulosx.bind("<Button-1>", lambda e: titulosx.delete(0, "end"))
    titulosx.pack()

    ctk.CTkLabel(repo_window, text="Ruta de acceso de la pelicula", fg_color='black').pack()
    ruta = ctk.CTkEntry(repo_window)
    ruta.insert(0, "C:\\path\\to\\image.png")
    ruta.bind("<Button-1>", lambda e: ruta.delete(0, "end"))
    ruta.pack()

    ctk.CTkLabel(repo_window, text="Descripción de la película", fg_color='black').pack()
    descripcion = ctk.CTkEntry(repo_window)
    descripcion.insert(0, "Descripción breve de la película")
    descripcion.bind("<Button-1>", lambda e: descripcion.delete(0, "end"))
    descripcion.pack()

    ctk.CTkButton(repo_window, text="Guardar", command=lambda: guardar_pelicula(titulosx.get(), ruta.get(), descripcion.get())).pack(pady=10)

# FUNCIONES DE SELECCION USER

def seleccionar_horario(pelicula, i):
    global pelicula_seleccionada
    pelicula_seleccionada = pelicula
    limpiar_ventana()
    imagen_roots_secundarios(i)
    ctk.CTkLabel(root, text=f"Película seleccionada: {pelicula}", font=("Arial", 18)).pack(pady=10)
    ctk.CTkLabel(root, text="Seleccione un horario:", font=("Arial", 18)).pack(pady=10)
    for horario in horarios:
        ctk.CTkButton(root, text=horario, command=lambda h=horario, i=i: seleccionar_sala(h, i), font=("Arial", 14)).pack(pady=5)
    ctk.CTkButton(root, text="Regresar", command=iniciar_programa).pack(pady=10)

def seleccionar_sala(horario, i):
    global horario_seleccionado
    horario_seleccionado = horario
    limpiar_ventana()
    imagen_roots_secundarios(i)
    ctk.CTkLabel(root, text=f"Película seleccionada: {pelicula_seleccionada}", font=("Arial", 18)).pack(pady=10)
    ctk.CTkLabel(root, text=f"Horario seleccionado: {horario}", font=("Arial", 18)).pack(pady=10)
    ctk.CTkLabel(root, text="Seleccione una sala:", font=("Arial", 18)).pack(pady=10)
    for sala in salas:
        ctk.CTkButton(root, text=sala, command=lambda s=sala: seleccionar_asiento(s), font=("Arial", 14)).pack(pady=5)
    ctk.CTkButton(root, text="Regresar", command=lambda: seleccionar_horario(pelicula_seleccionada,i)).pack(pady=10)

def seleccionar_asiento(sala):
    global sala_seleccionada
    sala_seleccionada = sala
    limpiar_ventana()
    ctk.CTkLabel(root, text=f"Película seleccionada: {pelicula_seleccionada}", anchor="w").pack(pady=(20, 5))
    ctk.CTkLabel(root, text=f"Horario seleccionado: {horario_seleccionado}", anchor="w").pack(pady=(20, 5))
    ctk.CTkLabel(root, text=f"Sala seleccionada: {sala}", anchor="w").pack(pady=(20, 5))
    ctk.CTkLabel(root, text="Seleccione un asiento:").pack(pady=(20, 5))

    frame_asientos = ctk.CTkFrame(root)
    frame_asientos.pack(pady=20)

    text = "XABCDEFGH"
    textnum = "112345678"
    fila_recomendada = recomendar_fila()
    
    for i in range(5):
        for j in range(5):
            if i == 0:
                cora = text[j]
                label = ctk.CTkLabel(frame_asientos, text=cora)
                label.grid(row=i, column=j, padx=5, pady=5)
            elif j == 0:
                xd = textnum[i]
                label = ctk.CTkLabel(frame_asientos, text=xd)
                label.grid(row=i, column=j, padx=5, pady=5)
            else:
                if cine[pelicula_seleccionada][horario_seleccionado][sala][i][j] == "Libre":
                    if i == fila_recomendada:
                        btn = ctk.CTkButton(frame_asientos, text="Recomendado", fg_color="green", width=3, command=lambda i=i, j=j: ocupar_asiento(i, j, text, textnum))
                    else:
                        btn = ctk.CTkButton(frame_asientos, text="Libre", fg_color="blue", width=3, command=lambda i=i, j=j: ocupar_asiento(i, j, text, textnum))
                else:
                    btn = ctk.CTkButton(frame_asientos, text="Ocupado", height=3, width=5, fg_color="red", state=ctk.DISABLED)
                btn.grid(row=i, column=j, padx=5, pady=5)

    ctk.CTkButton(root, text="Regresar", command=confirmacion_boletos).pack(pady=10)

# FUNCIONALIDADES ADICIONALES DE USER

def confirmacion_boletos():
    if x == 0:
        if messagebox.askyesno('Confirmar', '¿Desea regresar a la página principal e imprimir boletos?'):
            creapdf.crea_pdf(ruta_template, info, rutacss="")
            iniciar_programa()
    elif x == 1:
        if messagebox.askyesno('Validación', 'No tienes ningún asiento seleccionado. ¿Quieres regresar al menú principal?'):
            iniciar_programa()

def recomendar_fila():
    global sala_seleccionada
    for fila in range(1, 5):  
        if any(asiento == "Libre" for asiento in cine[pelicula_seleccionada][horario_seleccionado][sala_seleccionada][fila][1:]):
            return fila
    return -1

def ocupar_asiento(i, j, text, textnum):
    global asientoslist
    global datos
    global info
    global x
    if cine[pelicula_seleccionada][horario_seleccionado][sala_seleccionada][i][j] == "Libre":
        cine[pelicula_seleccionada][horario_seleccionado][sala_seleccionada][i][j] = "Ocupado"
        messagebox.showinfo("Éxito", "Asiento reservado con éxito")

        asientos = f"{text[j]}{textnum[i]}"
        horario = f"{horario_seleccionado}"
        peli = f"{pelicula_seleccionada}"
        sal_a = f"{sala_seleccionada}"
        asientoslist.append(asientos)
        info = {
            'pelicula': peli,
            'horario': horario,
            'sala': sal_a,
            'asientoslist': asientoslist
        }

        if not asientoslist:  # Verifica si la lista está vacía
            x = 1
        else:
            x = 0
    else:
        messagebox.showwarning("Advertencia", "El asiento ya está ocupado")
    actualizar_matriz()

def actualizar_matriz():
    seleccionar_asiento(sala_seleccionada)

def imagen_roots_secundarios(pelicula):
    try:
        movie_image = ctk.CTkImage(dark_image=Image.open(pelicula), size=(100, 250))
        movie_widget = ctk.CTkLabel(root, image=movie_image)
        movie_widget.pack(pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo de imagen: {pelicula}")
    except UnidentifiedImageError:
        messagebox.showerror("Error", f"El archivo no es una imagen válida: {pelicula}")

# FUNCIONALIDADES DE ADMIN

def guardar_pelicula(titulo, ruta, descripcion):
    global peliculas_repositorio
    global peliculas
    global descripciones
    global cine

    # Verificar si el título está vacío
    if not titulo.strip():
        messagebox.showerror("Error", "El título no puede estar vacío.")
        return

    # Verificar si la ruta del archivo es válida
    if not os.path.isfile(ruta):
        messagebox.showerror("Error", "La ruta de la imagen no es válida.")
        return

    if titulo and ruta and descripcion:
        peliculas_repositorio.append((titulo, ruta, descripcion))
        peliculas.append(titulo)
        descripciones.append(descripcion)
        peliculas_imagenes.append((titulo, ruta))
        cine[titulo] = {}
        for horario in horarios:
            cine[titulo][horario] = {}
            for sala in salas:
                cine[titulo][horario][sala] = inicializar_asientos(5, 5)
        print(f"{peliculas}")
        print(f"Película guardada: {titulo}, Ruta: {ruta}, Descripción: {descripcion}")  # Debug print
        limpiar_ventana_secundaria()
        abrir_repositorio()
    else:
        if messagebox.askyesno("No has guardado nada", "¿Quieres regresar al repositorio?"):
            abrir_repositorio()
        else:
            aggelements_list_repowindows()

def seleccionar_pelicula(titulo, imagen, descripcion):
    global peliculas_imagenes
    global peliculas
    global descripciones
    if (titulo, imagen) not in peliculas_imagenes:
        peliculas_imagenes.append((titulo, imagen))
        peliculas.append(titulo)
        descripciones.append(descripcion)
    print(f"Película seleccionada: {titulo}, Ruta: {imagen}, Descripción: {descripcion}")  # Debug print
    mostrar_peliculas_principales()

def eliminar_pelicula():
    def eliminar():
        titulo = entry_titulo.get()
        if titulo in peliculas:
            idx = peliculas.index(titulo)
            peliculas.pop(idx)
            descripciones.pop(idx)
            peliculas_imagenes.pop(idx)
            del cine[titulo]
            messagebox.showinfo("Éxito", f"Película '{titulo}' eliminada correctamente.")
        else:
            messagebox.showerror("Error", f"Película '{titulo}' no encontrada.")
        ventana_eliminar.destroy()
        mostrar_peliculas_principales()

    ventana_eliminar = Toplevel(root)
    ventana_eliminar.title("Eliminar Película")
    ventana_eliminar.geometry("300x150")
    ventana_eliminar.configure(bg='black')  

    label_titulo = tk.Label(ventana_eliminar, text="Título de la película a eliminar:", bg='black', fg='white')
    label_titulo.pack(pady=10)

    entry_titulo = tk.Entry(ventana_eliminar)
    entry_titulo.pack(pady=5)

    btn_eliminar = tk.Button(ventana_eliminar, text="Eliminar", command=eliminar)
    btn_eliminar.pack(pady=10)

# lIMPIAR VENTANA PRINCIPAL Y SECUNDARIA
def limpiar_ventana():
    for widget in root.winfo_children():
        widget.destroy()

def limpiar_ventana_secundaria():
    for widget in repo_window.winfo_children():
        widget.destroy()

# INICIAR APLICACION
iniciar_login()
root.mainloop()
