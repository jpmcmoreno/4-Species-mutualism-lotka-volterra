import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración inicial para usar pantalla completa
st.set_page_config(layout="wide")

# Define el sistema de ecuaciones diferenciales
def f(t, x):
    x1, x2, x3, x4 = x

    if x1 <= 0:
        x1 = 0.1
    if x2 <= 0:
        x2 = 0.1
    if x3 <= 0:
        x3 = 0.1
    if x4 <= 0:
        x4 = 0.1

    dx1_dt = epsilon * x1 * x2 - delta * x1
    dx2_dt = eta * x2 * x3 - xi * x1 * x2
    dx3_dt = r1 * x3 - alpha11 * x3**2 + beta12 * x3 * x4 - sigma * x2 * x3
    dx4_dt = r2 * x4 - alpha22 * x4**2 + beta21 * x3 * x4

    return np.array([dx1_dt, dx2_dt, dx3_dt, dx4_dt])

# Método de Euler para resolver ecuaciones diferenciales
def euler_method(f, t0, x0, h, n):
    
    t = t0
    x = x0

    t_values = [t]
    x_values = [x]

    for i in range(n):
        x = x + h * f(t, x)
        t = t + h
        t_values.append(t)
        x_values.append(x)
    return np.array(t_values), np.array(x_values)

st.title('Aplicación de interacción entre especies')

# Dividimos en 3 columnas para mejor distribución
col1, col2, col3 = st.columns([1, 1, 1.5])

with col1:
    # Sección Depredador
    with st.expander('**Parámetros del depredador** 🦅', expanded=True):
        nombre_depredador = st.text_input('Nombre depredador', 'Águilas')
        P1 = st.slider("Población inicial", 0, 100, 2, key="sliderP1")
        epsilon = st.slider("Tasa de crecimiento", 0., 3., 0.5, 0.1, key="epsilon")
        delta = st.slider("Tasa de mortalidad", 0., 3., 0.2, 0.1, key="delta")

    # Sección Presa
    with st.expander('**Parámetros de la presa** 🐸', expanded=True):
        nombre_presa = st.text_input('Nombre presa', 'Sapos')
        P2 = st.slider("Población inicial", 0, 100, 2, key="sliderP2")
        eta = st.slider("Tasa de crecimiento", 0., 3., 0.2, 0.1, key="eta")
        xi = st.slider("Tasa de mortalidad", 0., 3., 0.3, 0.1, key="xi")

with col2:
    # Especie Mutualista 1
    with st.expander("**Especie Mutualista 1** 🐝", expanded=True):
        nombre_mutualista_1 = st.text_input('Nombre', 'Abejas')
        P3 = st.slider("Población inicial", 0, 100, 3, key="sliderP3")
        r1 = st.slider("Tasa de crecimiento", 0., 3., 0.3, 0.1, key="r1")
        alpha11 = st.slider("Hacinamiento", 0., 3., 0.9, 0.1, key="alpha11")
        beta12 = st.slider("Beneficio mutualista", 0., 3., 0.3, 0.1, key="beta12")
        sigma = st.slider("Muerte por depredación", 0., 3., 0.5, 0.1, key="sigma")

    # Especie Mutualista 2
    with st.expander("**Especie Mutualista 2** 🌸", expanded=True):
        nombre_mutualista_2 = st.text_input('Nombre ', 'Flores')
        P4 = st.slider("Población inicial", 0, 100, 6, key="sliderP4")
        r2 = st.slider("Tasa de crecimiento", 0., 3., 0.3, 0.1, key="r2")
        alpha22 = st.slider("Hacinamiento", 0., 3., 0.2, 0.1, key="alpha22")
        beta21 = st.slider("Beneficio mutualista", 0., 3., 0.3, 0.1, key="beta21")

with col3:
    # Parámetros de simulación en la sidebar
    with st.expander("**Configuración de simulación** ⚙️",expanded=True):
        t_final = st.slider("Tiempo final", 0, 1000, 100, 10)
        n = st.slider("Número de pasos", 0, 1000, 500, 10)
    
    # Espacio para resultados
    with st.container():
        
            x0 = np.array([P1, P2, P3, P4])
            h = (t_final - 0)/n
            t_values, x_values = euler_method(f, 0, x0, h, n)
            
            # Crear figura con tamaño adaptable
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(t_values, x_values[:, 0], label=nombre_depredador)
            ax.plot(t_values, x_values[:, 1], label=nombre_presa)
            ax.plot(t_values, x_values[:, 2], label=nombre_mutualista_1)
            ax.plot(t_values, x_values[:, 3], label=nombre_mutualista_2)
            
            ax.set_xlabel('Tiempo')
            ax.set_ylabel('Población')
            ax.set_title('Dinámica de poblaciones')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True)
            
            st.pyplot(fig)