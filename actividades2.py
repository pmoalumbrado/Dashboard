import streamlit as st

# Debe estar antes de cualquier otra instrucción de Streamlit
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================
# Librerías
# ==========================
import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl
import streamlit.components.v1 as components
import os
import platform

# Configurar título de la aplicación
st.markdown("<h1 class='titulo-principal'>SEGUIMIENTO ACTIVIDADES Y CUMPLIMIENTO POR PROYECTO</h1>", unsafe_allow_html=True)


import os
import platform
import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Dashboard", layout="wide")
st.markdown("<h1 class='titulo-principal'>SEGUIMIENTO ACTIVIDADES Y CUMPLIMIENTO POR PROYECTO</h1>", unsafe_allow_html=True)

# ==========================
# Funciones para obtener rutas (usando la raíz del repositorio)
# ==========================
def get_base_path():
    """
    Retorna la ruta base, asumiendo que los archivos están en la raíz del repositorio.
    """
    return os.getcwd()

def get_images_path():
    """
    Retorna la ruta base para imágenes, asumiendo que están en la raíz del repositorio.
    """
    return os.getcwd()

# ==========================
# Funciones para Cargar Datos
# ==========================
@st.cache_data
def datos_planner():
    base_path = get_base_path()
    ruta_actividades = os.path.join(base_path, "1. Actividades Agregadas.xlsx")
    try:
        return pd.read_excel(ruta_actividades)
    except FileNotFoundError:
        st.error(f"Archivo '1. Actividades Agregadas.xlsx' no encontrado en: {ruta_actividades}")
        return pd.DataFrame()

@st.cache_data
def datos_adicionales():
    base_path = get_base_path()
    ruta_datos = os.path.join(base_path, "2. Datos.xlsx")
    try:
        workbook = openpyxl.load_workbook(ruta_datos, data_only=True)
        data = workbook.active.values
        columns = next(data)
        return pd.DataFrame(data, columns=columns)
    except FileNotFoundError:
        st.error(f"Archivo '2. Datos.xlsx' no encontrado en: {ruta_datos}")
        return pd.DataFrame()

# ==========================
# Cargar Datos
# ==========================
datos1 = datos_planner()
datos2 = datos_adicionales()

# ==========================
# Mostrar Logos en la barra lateral
# ==========================
col1, col2 = st.sidebar.columns(2)
imgs_path = get_images_path()
with col1:
    try:
        st.image(os.path.join(imgs_path, "Imagen1.png"), width=None)
    except Exception as e:
        st.warning("No se encontró Imagen1.png en la raíz del proyecto.")
with col2:
    try:
        st.image(os.path.join(imgs_path, "Imagen2.png"), width=None)
    except Exception as e:
        st.warning("No se encontró Imagen2.png en la raíz del proyecto.")

# ==========================
# CSS - TEXTO
# ==========================

# ==========================
# CSS para Estilizar la Aplicación
# ==========================
st.markdown("""
    <style>
    /* Estilos para la palabra "NAVEGACIÓN" en la barra lateral */
    .titulo-navegacion {
        font-size: 20px !important; 
        color: black !important; 
        font-weight: bold !important; 
        text-align: left; /* Si quieres que aparezca centrado */
    }
    /* Estilos para el título principal */
    .titulo-principal {
        font-size: 40px !important; 
        color: black !important; 
        font-weight: bold !important;
        text-align: center;
    }
    /* Estilos para el subtítulo consolidado */
    .titulo-consolidado {
        font-size: 30px !important; 
        color: #2477bc !important; 
        font-weight: bold !important;
    }
        
    </style>
""", unsafe_allow_html=True)


# Barra lateral: Navegación
st.sidebar.markdown("""
<h2 class="titulo-navegacion">NAVEGACIÓN</h2>
""", unsafe_allow_html=True)

pagina_seleccionada = st.sidebar.radio(
    "Elige una opción:",
    ["Consolidado", "Ver por área"]
)


# ==========================
# Filtros Globales
# ==========================



# ==========================
# Consolidado
# ==========================
if pagina_seleccionada == "Consolidado":
    st.markdown("<h2 class='titulo-consolidado'>CONSOLIDADO GENERAL EN LOS PROYECTOS AÑO 2024</h2>", unsafe_allow_html=True)


    # ==========================
    # Tabla de Inversión y Fecha (antes del gráfico)
    # ==========================
    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black;'>Inversión contractual pendiente ejercicio</h2>", unsafe_allow_html=True)
    
    html_inversion = """
    <style>
        table {width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
        table th, table td {padding: 10px; border: 1px solid #ddd;}
        table th {background-color: #2477bc; color: white;}
    </style>
    <table>
        <thead>
            <tr>
                <th>Municipio</th>
                <th>Inversión</th>
                <th>Fecha</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Jericó</td>
                <td>$303.588.683</td>
                <td>No especificada</td>
            </tr>
            <tr>
                <td>Tarso</td>
                <td>$2.202.293</td>
                <td>No especificada</td>
            </tr>
        </tbody>
    </table>
    """
    
    st.markdown(html_inversion, unsafe_allow_html=True)



    # ==========================
    # INICIO DEL GRÁFICO DE LUINARIAS
    # ==========================

    

    # Filtrar los datos para el mes de diciembre
    datos_diciembre = datos2[datos2['Mes'] == 'Diciembre']
    
    # Agrupar y sumar las luminarias por municipio
    tabla_luminarias = datos_diciembre.groupby('Municipio', as_index=False)['Total de Luminarias'].sum()
    
    # Orden personalizado de municipios
    orden_municipios = [
        "Guacarí", "Jamundí", "El Cerrito", "Quimbaya", "Circasia",
        "Jericó", "Ciudad Bolívar", "Pueblorrico", "Tarso", 
        "Santa Bárbara", "Puerto Asís"
    ]
    
    # Convertir 'Municipio' a categoría para respetar el orden personalizado
    tabla_luminarias['Municipio'] = pd.Categorical(tabla_luminarias['Municipio'], categories=orden_municipios, ordered=True)
    tabla_luminarias = tabla_luminarias.sort_values('Municipio')
    
    # Reemplazar valores NaN con 0 en "Total de Luminarias"
    tabla_luminarias['Total de Luminarias'] = tabla_luminarias['Total de Luminarias'].fillna(0).astype(int)
    
    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(
        tabla_luminarias,
        x='Municipio',
        y='Total de Luminarias',
        title="Total de luminarias por proyecto a Diciembre 2024",
        text='Total de Luminarias',
        color_discrete_sequence=["#2171b5"]  # Color en tonos de azul
    )
    
    # Mostrar los números sobre la barra (fuera) y en negro
    fig.update_traces(
        textposition='outside',
        textfont=dict(color='black')
    )
    
    # Actualizar layout para títulos y ejes en negro, y ajustar la orientación de las etiquetas si es necesario
    fig.update_layout(
        title=dict(
            text="Total de luminarias por proyecto a Diciembre 2024",
            font=dict(size=20)  # Ajustar el tamaño del título a 20px
        ),
        xaxis=dict(
            title=dict(text='Proyecto', font=dict(color='black')),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title=dict(text='Total de luminarias', font=dict(color='black')),
            tickfont=dict(color='black')
        ),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    # ==========================
    # FIN DEL GRÁFICO DE LUINARIAS
    # ==========================


    # ==========================
    # INICIO DEL GRÁFICO JUDICIAL
    # ==========================
    
    # Datos de ejemplo
    # Datos de ejemplo: Procesos Judiciales y sus cantidades
        # Datos de ejemplo
    data_j = {
        "Proceso Judicial": [
            "Acción de tutela",
            "Acción popular Ley 472 de 1998",
            "Acción popular Ley 472 de 1999",
            "Acción popular Ley 472 de 2000",
            "Nulidad simple",
            "Nulidad y restablecimiento del derecho",
            "Ordinario Laboral de Única Instancia",
            "Recurso extraordinario de anulación de Laudo Arbritral",
            "Reparación directa",
            "Revisión constitucionalidad y legalidad acuerdo"
        ],
        "Cantidad": [1, 2, 1, 1, 8, 16, 1, 1, 3, 1]
    }
    
    df_procesos = pd.DataFrame(data_j)
    
    # Agrupar todas las "Acciones populares" en una sola categoría
    df_procesos['Proceso Judicial'] = df_procesos['Proceso Judicial'].apply(
        lambda x: "Acción Popular" if "Acción popular" in x else x
    )
    
    # Agrupar por nombre después de la transformación
    df_procesos = df_procesos.groupby("Proceso Judicial", as_index=False).sum()
    
    # Definir una paleta de colores pastel con predominio de azules
    custom_colors = [
        "#cfe2f3",  # azul muy claro
        "#b3d4f1",  # azul claro
        "#99c6ef",  # azul claro intermedio
        "#80b8ed",  # azul intermedio
        "#66aae9",  # azul intermedio
        "#4d9ce7",  # azul intermedio
        "#3390e4",  # azul un poco más intenso
        "#1a84e2",  # azul intenso
        "#0078df",  # azul intenso
        "#0065cb"   # azul un poco más oscuro
    ]
    
    # Crear el gráfico de pastel
    fig = px.pie(
        df_procesos,
        names="Proceso Judicial",
        values="Cantidad",
        title="Distribución de Procesos Judiciales",
        color_discrete_sequence=custom_colors
    )
    
    # Configurar para que se muestre solo el porcentaje en cada rebanada, con texto en negro y fuera del pastel
    fig.update_traces(
        textinfo="percent",
        textposition="outside",
        textfont=dict(color="black", size=14)
    )
    
    # Actualizar layout para ajustar márgenes, título y posición de la leyenda
    fig.update_layout(
        margin=dict(l=50, r=50, t=70, b=50),
        legend=dict(
            font=dict(color="black", size=12),
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.1
        ),
        title=dict(font=dict(size=20, color="black"))
    )
    
    # Crear la tabla HTML con estilo
    html_table = """
    <table style="width:100%; border-collapse: collapse; text-align: center; font-size: 14px;">
        <thead style="background-color: #2477bc; color: white;">
            <tr>
                <th style="padding: 10px;">Proceso Judicial</th>
                <th style="padding: 10px;">Cantidad</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, row in df_procesos.iterrows():
        html_table += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['Proceso Judicial']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['Cantidad']}</td>
            </tr>
        """
    html_table += """
        </tbody>
    </table>
    """
    
    # Mostrar el gráfico y la tabla en columnas
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<h2 style='text-align: center;font-size: 16px;'>Cantidades por Proceso Judicial</h2>", unsafe_allow_html=True)
        components.html(html_table, height=300, scrolling=True)

    # ==========================
    # FIN DEL GRÁFICO DE JUDICIAL
    # ==========================

    # Crear un filtro de municipio
    st.markdown("<h2 style='text-align: center; font-size: 25px; color: black;'>Filtrar por Proyecto</h2>", unsafe_allow_html=True)
    municipio_seleccionado = st.selectbox(
        "Selecciona un Proyecto:",
        options=datos1['Municipio'].unique(),
        index=0,
        key="municipio_filtro_principal"  # Clave única para evitar conflictos
    )

    # ==========================
    # Información Global (Dos Tablas Separadas por Municipio) sobre luminarias y CREG
    # ==========================
    st.markdown("<h2 style='text-align: center;font-size: 30px; color: black;'>Operación y Mantenimiento</h2>", unsafe_allow_html=True)

    # Filtrar datos adicionales por el municipio seleccionado
    datos_municipio_global = datos2[datos2['Municipio'] == municipio_seleccionado]
    
    if not datos_municipio_global.empty:
        # Filtrar los datos para el mes de diciembre
        datos_diciembre = datos_municipio_global[datos_municipio_global['Mes'] == 'Diciembre']
        
        if not datos_diciembre.empty:
            # Tomar el valor de "Total de Luminarias" exclusivamente del mes de diciembre
            total_luminarias_diciembre = datos_diciembre['Total de Luminarias'].iloc[0]
        else:
            # Si no hay datos de diciembre, mostrar un mensaje de advertencia
            total_luminarias_diciembre = "No disponible"
            st.warning("No hay datos disponibles para el mes de diciembre en este municipio.")
        
        # Calcular otros totales y promedios globales por municipio
        totales_globales = datos_municipio_global.agg({
            'Total de Luminarias atendidas': 'sum',
            'Luminarias atentidas correctivo': 'sum',
            'Luminarias atentidas preventido': 'sum',
            'Indice de falla': 'mean',
            'Indice de eficiencia': 'mean',
            'Valor total a pagar AOM': 'sum',
            'Costo de inversión y facturación': 'sum',
            'Valor total a pagar': 'sum'
        })
        
        # Crear dos columnas para dividir las tablas
        col_izquierda_global, col_derecha_global = st.columns(2)
        
        # Tabla de "Información 1" (Global)
        with col_izquierda_global:
            st.markdown("<h3 style='text-align: center; font-size: 20px; color: black; '>Eficiencia de Operación</h3>", unsafe_allow_html=True)
            html_table_global_1 = f"""
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 16px;
                    text-align: left;
                }}
                table th, table td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                }}
                table th {{
                    background-color: #2477bc;
                    color: white;
                    text-align: center;
                }}
                table tbody tr:nth-child(even) {{
                    background-color: #f3f3f3;
                }}
                table tbody tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Total de Luminarias (Diciembre)</th>
                        <th>Correctivo</th>
                        <th>Preventivo</th>
                        <th>Índice de Eficiencia</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{total_luminarias_diciembre}</td>
                        <td>{totales_globales['Luminarias atentidas correctivo']:.0f}</td>
                        <td>{totales_globales['Luminarias atentidas preventido']:.0f}</td>
                        <td>{totales_globales['Indice de eficiencia']:.2f}%</td>
                    </tr>
                </tbody>
            </table>
            """
            components.html(html_table_global_1, height=200, scrolling=False)

    # Tabla de "CREG" (Global)
        with col_derecha_global:
            st.markdown("<h3 style='text-align: center; font-size: 20px; color: black; '>CREG</h3>", unsafe_allow_html=True)
            html_table_global_2 = f"""
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 16px;
                    text-align: left;
                }}
                table th, table td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                }}
                table th {{
                    background-color: #2477bc;
                    color: white;
                    text-align: center;
                }}
                table tbody tr:nth-child(even) {{
                    background-color: #f3f3f3;
                }}
                table tbody tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>CAOM</th>
                        <th>CINV</th>
                        <th>TOTAL</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${totales_globales['Valor total a pagar AOM']:,.2f}</td>
                        <td>${totales_globales['Costo de inversión y facturación']:,.2f}</td>
                        <td>${totales_globales['Valor total a pagar']:,.2f}</td>
                    </tr>
                </tbody>
            </table>
            """
            components.html(html_table_global_2, height=200, scrolling=False)
    
    else:
        st.warning("No hay datos disponibles para el municipio seleccionado.")


    # ==========================
# Información Mensual por Proyecto y Jurídica
# ==========================
    st.markdown("<h2 style='text-align: center; font-size: 30px; color: black;'>Información Mensual por Proyecto</h2>", unsafe_allow_html=True)
    
    # Filtrar datos adicionales por el municipio seleccionado
    datos_municipio_global = datos2[datos2['Municipio'] == municipio_seleccionado]
    
    # Obtener meses disponibles y agregar el filtro por mes
    if 'Mes' in datos2.columns:
        meses_disponibles = datos_municipio_global['Mes'].dropna().unique()
        mes_seleccionado = st.selectbox(
            "Selecciona un Mes:", options=meses_disponibles, key="mes_filtro_datos2"
        )
        # Filtrar los datos adicionales por el mes seleccionado
        datos_municipio_global = datos_municipio_global[datos_municipio_global['Mes'] == mes_seleccionado]
    
    # Sección de Información Global (Información 1 y CREG)
    if not datos_municipio_global.empty:
        # Calcular totales y promedios globales por municipio y mes
        totales_globales = datos_municipio_global.agg({
            'Total de Luminarias': 'sum',
            'Total de Luminarias atendidas': 'sum',
            'Luminarias atentidas correctivo': 'sum',
            'Luminarias atentidas preventido': 'sum',
            'Indice de falla': 'mean',
            'Indice de eficiencia': 'mean',
            'Valor total a pagar AOM': 'sum',
            'Costo de inversión y facturación': 'sum',
            'Valor total a pagar': 'sum'
        })
        
        # Crear dos columnas para dividir las tablas
        col_izquierda_global, col_derecha_global = st.columns(2)
        
        # Tabla de "Información 1" (Global por Mes)
        with col_izquierda_global:
            
            st.markdown("<h3 style='text-align: center; font-size: 20px; color: black;'>Eficiencia de Operación</h3>", unsafe_allow_html=True)
            html_table_global_1 = f"""
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 16px;
                    text-align: left;
                }}
                table th, table td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                }}
                table th {{
                    background-color: #2477bc;
                    color: white;
                    text-align: center;
                }}
                table tbody tr:nth-child(even) {{
                    background-color: #f3f3f3;
                }}
                table tbody tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Total de Luminarias</th>
                        <th>Correctivo</th>
                        <th>Preventivo</th>
                        <th>Índice de Eficiencia</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{totales_globales['Total de Luminarias']:.0f}</td>
                        <td>{totales_globales['Luminarias atentidas correctivo']:.0f}</td>
                        <td>{totales_globales['Luminarias atentidas preventido']:.0f}</td>
                        <td>{totales_globales['Indice de eficiencia']:.2f}%</td>
                    </tr>
                </tbody>
            </table>
            """
            components.html(html_table_global_1, height=200, scrolling=False)
        
        # Tabla de "CREG" (Global por Mes)
        with col_derecha_global:
       
            st.markdown("<h3 style='text-align: center; font-size: 20px; color: black;'>CREG</h3>", unsafe_allow_html=True)
            html_table_global_2 = f"""
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 16px;
                    text-align: left;
                }}
                table th, table td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                }}
                table th {{
                    background-color: #2477bc;
                    color: white;
                    text-align: center;
                }}
                table tbody tr:nth-child(even) {{
                    background-color: #f3f3f3;
                }}
                table tbody tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>CAOM</th>
                        <th>CINV</th>
                        <th>TOTAL</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${totales_globales['Valor total a pagar AOM']:,.2f}</td>
                        <td>${totales_globales['Costo de inversión y facturación']:,.2f}</td>
                        <td>${totales_globales['Valor total a pagar']:,.2f}</td>
                    </tr>
                </tbody>
            </table>
            """
            components.html(html_table_global_2, height=200, scrolling=False)

####################################################################
## ver por area
####################################################################
# Verifica que 'pagina_seleccionada' y 'datos1' existan
if pagina_seleccionada == "Ver por área":
    st.markdown("<h2 class='titulo-consolidado'>CONSOLIDADO GENERAL POR ÁREA FECHA DE ACTUALIZACIÓN: 19/02/25 </h2>", unsafe_allow_html=True)
    
    if datos1.empty:
        st.warning("No hay datos disponibles para mostrar.")
    else:
        # ==========================================================
        # Filtro global de actividades retrasadas (afecta a gráfico y tabla)
        # ==========================================================
        mostrar_retrasadas = st.radio(
            "¿Qué actividades deseas ver?",
            options=["Todas las actividades", "Solo actividades con retraso"],
            index=0,
            key="filtro_retraso_area"
        )
        
        # Filtrar datos para gráficos según la opción seleccionada
        datos_filtrados = datos1.copy()
        if mostrar_retrasadas == "Solo actividades con retraso":
            datos_filtrados = datos_filtrados[datos_filtrados['Con retraso'] == True]
        
        # ==========================================================
        # Gráfico de barras: Actividades por Municipio y Área
        # ==========================================================
        df_actividades_chart = datos_filtrados.groupby(['Municipio', 'Nombre del depósito']).size().reset_index(name='Conteo')
        
        fig_actividades = px.bar(
            df_actividades_chart,
            x='Municipio',
            y='Conteo',
            color='Nombre del depósito',
            title="Actividades por Municipio y Área",
            text='Conteo',
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_actividades.update_traces(textposition='inside', textfont_size=10)
        fig_actividades.update_layout(
            title=dict(text="Actividades por Proyecto y Área", font=dict(color="black", size=20)),
            xaxis=dict(title=dict(text="Municipio", font=dict(color="black", size=14)), tickfont=dict(color="black", size=12)),
            yaxis=dict(title=dict(text="Cantidad de Actividades", font=dict(color="black", size=14)), tickfont=dict(color="black", size=12)),
            legend=dict(title=dict(text="Área (Depósito)", font=dict(size=14))),
            uniformtext_minsize=10,
            uniformtext_mode='hide'
        )
        st.plotly_chart(fig_actividades, use_container_width=True)
        
        
        # ==========================================================
        # Cálculo de métricas de tareas (usando datos1, no filtrados globalmente)
        # ==========================================================
        total_tareas = len(datos1)
        tareas_retrasadas = datos1[datos1['Con retraso'] == True]
        total_retrasadas = len(tareas_retrasadas)
        total_sin_retraso = total_tareas - total_retrasadas
        
        # Clasificación de tareas retrasadas por estado
        no_iniciadas = len(tareas_retrasadas[tareas_retrasadas['Progreso'] == 'No iniciado'])
        completado = len(tareas_retrasadas[tareas_retrasadas['Progreso'] == 'Completado'])
        en_curso = len(tareas_retrasadas[tareas_retrasadas['Progreso'] == 'En curso'])
        en_curso_c = no_iniciadas + en_curso
        
        # ==========================================================
        # Gráfico de pastel: Distribución de Tareas
        # ==========================================================
        labels = ["Sin retraso", "En curso con retraso", "Completado con retraso"]
        values = [total_sin_retraso, en_curso_c, completado]
        title_str = f"Distribución de Tareas (Total: {total_tareas})"
        # Nota: si se selecciona "Solo actividades con retraso", total_sin_retraso será 0.
        color_sequence = ["#6baed6", "#4292c6", "#2171b5"]
        
        fig_pie = px.pie(
            names=labels,
            values=values,
            title=title_str,
            color_discrete_sequence=color_sequence
        )
        fig_pie.update_traces(
            textinfo='percent+label',
            textposition='inside',
            textfont=dict(size=18)
        )
        fig_pie.update_layout(
            title=dict(
            text=title_str,
            font=dict(size=20)  # Ajustar el tamaño del título a 20px
        ),
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
            margin=dict(t=80, b=20, l=20, r=20)
        )
        
        # Mostrar gráfico de pastel y tabla resumen en columnas
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                <h2 style="margin-bottom: 10px; font-size: 16px;">Total de Tareas: {total_tareas}</h2>
                <style>
                    table {{width: 100%; border-collapse: collapse; text-align: center; font-size: 14px;}}
                    table th, table td {{padding: 10px; border: 1px solid #ddd;}}
                    table th {{background-color: #2477bc; color: white;}}
                </style>
                <table>
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th>Cantidad</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Sin retraso</td>
                            <td>{total_sin_retraso}</td>
                        </tr>
                        <tr>
                            <td>En curso con retraso</td>
                            <td>{en_curso_c}</td>
                        </tr>
                        <tr>
                            <td>Completado con retraso</td>
                            <td>{completado}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        
        # ==========================================================
        # Gráfico de barras: Desglose de Tareas con Retraso por Depósito
        # ==========================================================
        # Se filtran las tareas con retraso (usando datos1)
        tareas_retrasadas = datos1[datos1['Con retraso'] == True]
        
        df_summary = tareas_retrasadas.groupby('Nombre del depósito').agg(
            Completado=('Progreso', lambda x: (x == 'Completado').sum()),
            En_curso_con_retraso=('Progreso', lambda x: x.isin(['En curso', 'No iniciado']).sum())
        ).reset_index()
        # Renombrar para que los labels se muestren con espacios
        df_summary = df_summary.rename(columns={"En_curso_con_retraso": "En curso con retraso",
                                                 "Completado": "Completado con retraso"})
        df_summary['Total'] = df_summary['Completado con retraso'] + df_summary['En curso con retraso']
        df_summary = df_summary.sort_values(by='Total', ascending=False)
        
        fig_bar = px.bar(
            df_summary,
            x='Nombre del depósito',
            y=['Completado con retraso', 'En curso con retraso'],
            title='Desglose de Tareas con Retraso por Depósito',
            text_auto=True,
            color_discrete_map={
                "Completado con retraso": "#4292c6",
                "En curso con retraso": "#2171b5"
            }
        )
        fig_bar.update_traces(
            textposition='outside',
            textfont=dict(color='black')
        )
        fig_bar.update_layout(
            title=dict(
                text='Desglose de Tareas con Retraso por Depósito',
                font=dict(size=20,color='black' ) # Ajustar el tamaño del título a 20px
                
            ),
            barmode='group',
            xaxis=dict(title=dict(text='Nombre del depósito', font=dict(color='black')),
                       tickfont=dict(color='black')),
            yaxis=dict(title=dict(text='Número de tareas con retraso', font=dict(color='black')),
                       tickfont=dict(color='black')),
            uniformtext_minsize=12,
            uniformtext_mode='hide'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        
        # ==========================================================
        # Filtros adicionales para la tabla (afectan solo la tabla)
        # ==========================================================
        proyectos_disponibles = sorted(datos1['Municipio'].dropna().unique().tolist())
        proyecto_seleccionado = st.selectbox(
            "Selecciona un Proyecto:",
            options=["Todos los Proyectos"] + proyectos_disponibles,
            index=0,
            key="filtro_proyecto_table"
        )
        
        depositos_disponibles = sorted(datos1['Nombre del depósito'].dropna().unique().tolist())
        deposito_seleccionado = st.selectbox(
            "Selecciona un depósito para filtrar:",
            options=["Todos los depósitos"] + depositos_disponibles,
            index=0,
            key="filtro_deposito_table"
        )
        
        datos_table = datos1.copy()
        if proyecto_seleccionado != "Todos los Proyectos":
            datos_table = datos_table[datos_table['Municipio'] == proyecto_seleccionado]
        if deposito_seleccionado != "Todos los depósitos":
            datos_table = datos_table[datos_table['Nombre del depósito'] == deposito_seleccionado]
        if mostrar_retrasadas == "Solo actividades con retraso":
            datos_table = datos_table[datos_table['Con retraso'] == True]
        
        # Usar la columna "Días de retraso" ya existente en el Excel, formateándola para que no muestre NaN ni decimales.
        if 'Días de retraso' in datos_table.columns:
            datos_table['Días de retraso'] = pd.to_numeric(datos_table['Días de retraso'], errors='coerce')
        else:
            datos_table['Días de retraso'] = ""
        
        # ==========================================================
        # Construir la tabla HTML con los detalles de actividades:
        # Se muestran: Nombre del depósito, Progreso, Nombre de la tarea y Días de retraso.
        # ==========================================================
        st.markdown("<h3 style='text-align: center; font-size: 30px; color: black;'>Detalles de Actividades</h3>", unsafe_allow_html=True)
        if not datos_table.empty:
            html_table = """
            <style>
                table {width: 100%; border-collapse: collapse; text-align: center; font-size: 14px;}
                table th, table td {padding: 10px; border: 1px solid #ddd;}
                table th {background-color: #2477bc; color: white;}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Nombre del depósito</th>
                        <th>Progreso</th>
                        <th>Nombre de la tarea</th>
                        <th>Días de retraso</th>
                    </tr>
                </thead>
                <tbody>
            """
            for idx, row in datos_table.iterrows():
                deposito = str(row['Nombre del depósito']).replace('\r\n', '<br>').replace('\n', '<br>')
                progreso = str(row['Progreso']).replace('\r\n', '<br>').replace('\n', '<br>')
                tarea = str(row['Nombre de la tarea']).replace('\r\n', '<br>').replace('\n', '<br>')
                dias = row['Días de retraso']
                if pd.isna(dias):
                    dias_str = "a tiempo"
                else:
                    try:
                        dias_str = str(int(round(dias)))
                    except Exception:
                        dias_str = str(dias)
                html_table += f"""
                    <tr>
                        <td>{deposito}</td>
                        <td>{progreso}</td>
                        <td>{tarea}</td>
                        <td>{dias_str}</td>
                    </tr>
                """
            html_table += """
                </tbody>
            </table>
            """
            components.html(html_table, height=400, scrolling=True)
        else:
            st.warning("No se encontraron actividades con los criterios seleccionados para la tabla.")
