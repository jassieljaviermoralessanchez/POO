import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


config = {
    'host': 'localhost',
    'user': 'root',          
    'password': '1234',    
    'database': 'gestion_tareas'
}

def conectar():
    return mysql.connector.connect(**config)

def agregar_tarea(materia, descripcion, fecha):
    conn = conectar()
    cursor = conn.cursor()

    
    cursor.execute("SELECT id FROM materias WHERE nombre = %s", (materia,))
    resultado = cursor.fetchone()

    if resultado:
        materia_id = resultado[0]
    else:
        cursor.execute("INSERT INTO materias (nombre) VALUES (%s)", (materia,))
        materia_id = cursor.lastrowid

    
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, fecha_entrega, estado, materia_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (materia, descripcion, fecha, 'pendiente', materia_id))

    conn.commit()
    conn.close()

def listar_tareas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, m.nombre, t.descripcion, t.fecha_entrega, t.estado
        FROM tareas t
        JOIN materias m ON t.materia_id = m.id
    """)
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def eliminar_tarea(tarea_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
    conn.commit()
    conn.close()

def actualizar_tarea(tarea_id, nuevo_estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET estado = %s WHERE id = %s", (nuevo_estado, tarea_id))
    conn.commit()
    conn.close()



def actualizar_lista():
    lista_tareas.delete(*lista_tareas.get_children())
    tareas = listar_tareas()
    for tarea in tareas:
        lista_tareas.insert("", "end", values=tarea)

def agregar():
    materia = entrada_materia.get()
    descripcion = entrada_descripcion.get()
    fecha = entrada_fecha.get()

    if materia and descripcion and fecha:
        try:
            agregar_tarea(materia, descripcion, fecha)
            messagebox.showinfo("Éxito", "Tarea agregada correctamente.")
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")

def eliminar():
    seleccionado = lista_tareas.selection()
    if seleccionado:
        tarea_id = lista_tareas.item(seleccionado)["values"][0]
        try:
            eliminar_tarea(tarea_id)
            messagebox.showinfo("Éxito", "Tarea eliminada correctamente.")
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showwarning("Selecciona una tarea", "Seleccione una tarea para eliminar.")

def actualizar():
    seleccionado = lista_tareas.selection()
    if seleccionado:
        tarea_id = lista_tareas.item(seleccionado)["values"][0]
        nuevo_estado = combo_estado.get()
        try:
            actualizar_tarea(tarea_id, nuevo_estado)
            messagebox.showinfo("Éxito", "Estado actualizado correctamente.")
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showwarning("Selecciona una tarea", "Seleccione una tarea para actualizar.")



ventana = tk.Tk()
ventana.title("Gestión de Tareas Escolares")
ventana.geometry("650x500")


tk.Label(ventana, text="Materia:").pack()
entrada_materia = tk.Entry(ventana)
entrada_materia.pack()

tk.Label(ventana, text="Descripción:").pack()
entrada_descripcion = tk.Entry(ventana)
entrada_descripcion.pack()

tk.Label(ventana, text="Fecha de Entrega (YYYY-MM-DD):").pack()
entrada_fecha = tk.Entry(ventana)
entrada_fecha.pack()

tk.Button(ventana, text="Agregar Tarea", command=agregar).pack(pady=5)


columnas = ("ID", "Materia", "Descripción", "Fecha de Entrega", "Estado")
lista_tareas = ttk.Treeview(ventana, columns=columnas, show="headings")
for col in columnas:
    lista_tareas.heading(col, text=col)
lista_tareas.pack(fill="both", expand=True)

tk.Button(ventana, text="Eliminar Tarea", command=eliminar).pack(pady=5)

tk.Label(ventana, text="Nuevo Estado:").pack()
combo_estado = ttk.Combobox(ventana, values=["pendiente", "completado"])
combo_estado.pack()

tk.Button(ventana, text="Actualizar Estado", command=actualizar).pack(pady=5)


actualizar_lista()
ventana.mainloop()
