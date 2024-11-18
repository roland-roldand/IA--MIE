import streamlit as st # importar la libreria
from groq import Groq 

# configuracion de la ventana en la web 
st.set_page_config(page_title= "Mi chat de IA", page_icon= "🎀")

# Titulo de la pagina
st.title("Mi primera aplicación con Streamlit")

# ingreso datos de usuario
nombre = st.text_input("¿Cuál es tu nombre?")

# boton con funcionalidad
if st.button("saludar"):
    st.write(f"hola {nombre}, gracias por venir al super chat")

PELICULAS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] 
# lleva este nombre por la lista anterior. Mientras sepas que es el valor de MODELOS

# para conectarte a la API
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] # obtiee la clave del API
    return Groq(api_key = clave_secreta)

# configurar a la ia
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, # indica el modelo de la IA
        messages = [{"role" : "user", "content": mensajeDeEntrada}],
        stream = True # para que el modelo responda a tiempo 
    ) #devuelve la respuesta d la IA

# historial de mensaje
def inicializar_estado(): 
    # si no existe una lista "mensajes" -< creas una
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] # lista vacia = historial vacio

# cree una funcion para darle un disño a la pagina
def configurar_pagina():
    st.title("mi chat de IA") # titulo

    st.sidebar.title("Configuración") # barra lateral
    st.sidebar.write("Stanley Kubrick fue un director estadounidense reconocido por su enfoque perfeccionista y su influencia en el cine del siglo XX. A traves de sus obras, exploro temas como la psicología humana y la violencia, usando una estetica meticulosa y provocadora.") # texto en la barra lateral

   
    elegirPelicula = st.sidebar.selectbox(
        "Elegí el que más se adapte", # titulo
        PELICULAS, # opciones del menu
        index= 0
    )
    return elegirPelicula

#
def actualizar_historial(rol, contenido, avatar):
    # metodo append() agrega datod a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

# sector del chat, el espacio bonito
def area_chat():
    contenedor_del_chat = st.container(height=400, border = True ) #para poner borde
    with contenedor_del_chat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" # variable vacia para que acumule
    for frase in chat_completo:
        if frase.choices[0].delta.content: # si tiene contenido NONE esta vacio
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa # python lo lee cuando se termina el for


def main():
    # funciones especificas del chatbot
    modelo = configurar_pagina() # llamo a la funcion
    clienteUsuario = crear_usuario_groq() # crea el usuario para usar la API
    inicializar_estado() # crea el historial de mensajes
    area_chat() # en la web visualizas el contenedor

    mensaje = st.chat_input("Escribí un mensaje ...")

    # verificas si el mensaje tiene contenido
    if mensaje :
        actualizar_historial("user", mensaje, "👽") # icono de usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) # obtiene la respuesta
        if chat_completo: #verifica que tenga contenido
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "👼")
                st.rerun() #actualiza

if __name__ == "__main__": 
    main() # le decis que es una funcion principal y que siempre se invoca