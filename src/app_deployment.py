import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


import base64

# # Obtener la ruta de la carpeta 'src'
# src_dir = os.path.dirname(os.path.abspath(__file__))

# # Construir la ruta completa al archivo de la base de datos
# db_path = os.path.join(src_dir, 'assets/images/EV Charging Station 00.png')

# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png" if image_file.name.endswith(".png") else "jpg"};base64,{encoded_string.decode()});
#         background-size: cover;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )

def add_bg_from_local(image_url):
    
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Ejemplo de uso
add_bg_from_local('https://i.imgur.com/Rf3nJHm.png')


# Estilo CSS personalizado para los títulos de pestañas

estilo_css = """
<style>
    .css-1aumxhk {
        font-size: 20px; /* Ajusta el tamaño de fuente para los títulos de pestañas y el texto de las pestañas */
    }

    textarea {
        font-size: 20px !important;
    }
    
    input {
        font-size: 20px !important;
    }

    .label_font {
        font-size: 20px; /* Ajusta el tamaño de fuente para los labels de input */
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:20px;
    }

    .stNumberInput > label {
        font-size: 20px; /* Ajusta el tamaño de fuente para los labels de los number_input */
    }

    .stMarkdown {
        font-size: 20px; /* Ajusta el tamaño de fuente para el contenido de las pestañas */
    }
</style>
"""

st.markdown(estilo_css, unsafe_allow_html=True)


# def set_bg_color(color):
#     color_code = f"background-color: {color};"
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             {color_code}
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# set_bg_color("#00012e")  # Reemplaza "#F0F0F0" con el código de color deseado



# Carga de datos
data = """state,area,stations,vehicles
Alabama,135768,17832,8700
Alaska,1723702,415,2000
Arizona,295234,2499,65800
Arkansas,137732,1379,5100
California,423970,1427,903600
Colorado,269837,223,59900
Connecticut,14371,4335,22000
Delaware,6452,3724,5400
District of Columbia,177,645,5900
Florida,170312,400,168000
Georgia,153910,1318,60100
Hawaii,28313,1915,19800
Idaho,216632,1447,5900
Illinois,149997,3590,66900
Indiana,94326,634,17700
Iowa,145753,1004,6200
Kansas,213100,1714,7600
Kentucky,104659,166,7600
Louisiana,135659,1347,5900
Maine,91635,969,5000
Maryland,32133,586,46100
Massachusetts,27337,3293,49400
Michigan,250487,2400,33100
Minnesota,225181,620,24300
Mississippi,125443,1559,2400
Missouri,180533,293,17900
Montana,380832,835,3300
Nebraska,200330,1733,4600
Nevada,286637,277,32900
New Hampshire,24217,1736,7000
New Jersey,22587,992,87000
New Mexico,314917,466,7100
New York,141297,2226,84700
North Carolina,139391,422,45600
North Dakota,183108,647,600
Ohio,116096,1906,34100
Oklahoma,181038,341,16300
Oregon,254806,366,47000
Pennsylvania,119283,386,47400
Rhode Island,4001,436,4300
South Carolina,82933,511,13500
South Dakota,199514,328,1200
Tennessee,109153,273,22000
Texas,695622,173,149000
Utah,219882,104,28000
Vermont,24906,232,5300
Virginia,110787,318,56600
Washington,184665,133,104100
West Virginia,62755,101,1900
Wisconsin,169637,114,15700
Wyoming,253335,67,800"""

df = pd.DataFrame([x.split(',') for x in data.split('\n')[1:-1]],
                  columns=data.split('\n')[0].split(','))
df = df.astype({'area': int, 'stations': int, 'vehicles': int})

# Definición de las funciones
def show_inicio():
    st.subheader("Objetivo")
    st.markdown("<span style='font-size:20px;'>Este proyecto tiene como objetivo estimar la cantidad de estaciones de carga necesarias para vehículos eléctricos en base al área y la cantidad de vehículos registrados en cada estado.</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>El enfoque es entrenar y desplegar un modelo predictivo utilizando datos del Laboratorio Nacional de Energía Renovable (en inglés: National Renewable Energy Laboratory, abreviado NREL) de EE.UU. y otras fuentes, para que pueda ser aplicado en cualquier parte del mundo donde este sector tecnológico esté en auge.</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>A medida que más países adoptan vehículos eléctricos, es crucial planificar una infraestructura adecuada de estaciones de carga para satisfacer la demanda.</span>", unsafe_allow_html=True)

def show_analisis():

    st.subheader("Análisis Exploratorio de Datos (EDA)")
    st.markdown("<span style='font-size:20px;'>- Descripción de los datos iniciales (70,830 filas, 74 columnas)</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Tratamiento de valores nulos y limpieza de datos</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Análisis de variables categóricas y numéricas</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Creación de la variable objetivo 'stations_number'</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Visualizaciones clave (histogramas, gráficos de barras, etc.)</span>", unsafe_allow_html=True)

    st.subheader("Preparación de datos")
    st.markdown("<span style='font-size:20px;'>- Codificación de variables categóricas</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Normalización de datos</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- División en conjuntos de entrenamiento y prueba</span>", unsafe_allow_html=True)

    st.subheader("Modelado")
    st.markdown("<span style='font-size:20px;'>- Selección del modelo (e.g. regresión lineal, árbol de decisión)</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Entrenamiento del modelo</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Evaluación del rendimiento (métricas relevantes)</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Optimización de hiperparámetros</span>", unsafe_allow_html=True)

    # Estadísticas descriptivas
    st.subheader("Estadísticas descriptivas:")
    st.write(df.describe())

    # Correlación entre variables numéricas
    corr = df[['area', 'stations', 'vehicles']].corr()
    st.subheader("Correlación entre variables numéricas:")
    st.write(corr)

    # Visualización de datos
    st.subheader("Visualización de datos")
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    sns.scatterplot(data=df, x='area', y='stations', ax=ax[0])
    ax[0].set_title('Área vs Estaciones')
    sns.scatterplot(data=df, x='vehicles', y='stations', ax=ax[1])
    ax[1].set_title('Vehículos vs Estaciones')
    st.pyplot(fig)

    # Separación de datos en conjuntos de entrenamiento y prueba
    X = df[['area', 'vehicles']]
    y = df['stations']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenamiento del modelo
    global model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluación del modelo
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    st.subheader("Métricas de evaluación del modelo")
    st.write(f"R^2 en el conjunto de entrenamiento: {r2_score(y_train, y_pred_train):.2f}")
    st.write(f"R^2 en el conjunto de prueba: {r2_score(y_test, y_pred_test):.2f}")
    st.write(f"Error absoluto medio en el conjunto de prueba: {mean_absolute_error(y_test, y_pred_test):.2f}")

    return model


def show_modelo(model):
    #st.title("Modelo de Estimación")

    # Despliegue del modelo
    st.subheader("Estimación de Estaciones de Carga")
    area = st.number_input("Área (km²)", min_value=0, value=0, label_visibility="visible", key="area_input")
    vehicles = st.number_input("Cantidad de vehículos", min_value=0, value=0, label_visibility="visible", key="vehicle_input")

    if st.button("Estimar Estaciones"):
        if area <= 0 or vehicles <= 0:
            st.error('Por favor, ingresa un valor mayor que cero.')
        else:
            st.markdown("<span style='font-size:20px;'>Resultados del modelo:</span>", unsafe_allow_html=True)
            stations = model.predict([[area, vehicles]])[0]
            st.markdown(f"<span style='font-size:20px'>La cantidad estimada de estaciones de carga para un área de <span style='color:blue;font-weight:bold;font-size:22px'>{area} km<sup>2</sup></span></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:20px'>y <span style='color:blue;font-weight:bold;font-size:22px'>{vehicles} vehículos</span> es de: <span style='color:green;font-weight:bold;font-size:24px'>{int(stations)} estaciones de carga</span></span>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:20px;'>- Tipos de conectores recomendados (Nivel 1, Nivel 2, Carga rápida)</span>", unsafe_allow_html=True)

            st.markdown("<span style='font-size:20px;'>Opciones adicionales:</span>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:20px;'>- Visualización de resultados en un mapa</span>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:20px;'>- Descarga de resultados en formato CSV</span>", unsafe_allow_html=True)

def show_info_adicional():
    st.subheader("Información Adicional")
    st.markdown("<span style='font-size:20px;'>Para mejorar el contenido de la aplicación, aquí se podrá agregar más información, fotografías, artículos, etc.", unsafe_allow_html=True)
    # Agrega tu contenido adicional aquí

    st.subheader("Conceptos básicos de vehículos eléctricos")
    st.markdown("<span style='font-size:20px;'>- Descripción general de la tecnología de vehículos eléctricos</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Beneficios ambientales y de eficiencia energética</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Desafíos actuales y futuros de la movilidad eléctrica</span>", unsafe_allow_html=True)

    st.subheader("Tipos de estaciones de carga y conectores")
    st.markdown("<span style='font-size:20px;'>- Estaciones de carga Nivel 1, Nivel 2 y Carga rápida (descripción y diferencias)</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>- Tipos de conectores más comunes (J1772, CCS, CHAdeMO, etc.)</span>", unsafe_allow_html=True)

    st.subheader("Políticas e incentivos gubernamentales")
    st.markdown("<span style='font-size:20px;'>- Resumen de políticas y programas de incentivos para la adopción de vehículos eléctricos en diferentes países</span>", unsafe_allow_html=True)

    st.subheader("Recursos adicionales")
    st.markdown("<span style='font-size:20px;'>- Enlaces a sitios web, publicaciones y organizaciones relevantes para obtener más información</span>", unsafe_allow_html=True)

def main():
    st.title('Estimación de Estaciones de Carga para Vehículos Eléctricos')

    st.markdown(estilo_css, unsafe_allow_html=True)

    # Crear una lista de títulos de pestañas
    titulos_pestanas = ['Inicio', 'Análisis', 'Modelo', 'Información Adicional']

    # Crear las pestañas
    inicio, analisis, pest_modelo, info = st.tabs(titulos_pestanas)

    # Agregar contenido a cada pestaña
    with inicio:
        show_inicio()
        # Crear un botón para redirigir a la pestaña del modelo
    
    with analisis:
        show_analisis()
        # Crear un botón para redirigir a la pestaña del modelo

    with pest_modelo:
        show_modelo(model)

    with info:
        show_info_adicional()

    # Obtener el índice de la pestaña actual
    indice_actual = titulos_pestanas.index(st.session_state.current_tab)

    # Guardar el estado de la pestaña actual
    st.session_state.current_tab = titulos_pestanas[indice_actual]

if __name__ == '__main__':
    st.session_state.current_tab = 'Inicio'  # Inicializar la pestaña actual
    main()