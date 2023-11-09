import psutil

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
from datetime import datetime


import plotly.graph_objects as go

# Se cargan los datos desde Google Drive
link = "https://www.dropbox.com/scl/fi/u9kqopx449lgp2k5ouq02/BASE_DATOS_RG_ALTURAS_LIMPIO.xlsx?rlkey=tmy8griwuzk55m1s3z0fowfk8&dl=1"
# Cargar tus datos
df = pd.read_excel(link, sheet_name="Sheet1", engine="openpyxl")

memoria_bytes = psutil.Process().memory_info().rss
memoria_mb = memoria_bytes / (1024 * 1024)
print(f"Memoria en uso por el proceso: {memoria_mb:.2f} MB")

# Crear la aplicación de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Definir la función para crear el gráfico de competencia
def grafico_competencia(df):
    competencia_cantidad = df["CER TSA"].value_counts().nlargest(5)
    competencia_sort = competencia_cantidad.sort_values(ascending=False)
    colores = [
    "#5A5E5A",
    "#726B72",
    "#8A788D",
    "#A28598",
    "#BA92A3",
    "#CCAAAE",
    "#D6BEB7",
    "#E3C9C2",
    "#F0D6C7",
    "#F7E3D2"
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=competencia_sort.index, y=competencia_sort.values, marker_color=colores))
    fig.update_layout(
        title="Los 5 centros de entrenamiento de donde más vienen los trabajadores",
        xaxis_title="Cantidad de personas",
        yaxis_title="Centros de entrenamiento",
        
    )

    return fig

# Definir la función para crear el gráfico de los cursos
def grafico_cursos(df):
    colores = [
    "#5A4177",
    "#724E82",
    "#8A5B8D",
    "#A26898",
    "#BA75A3",
    "#CC82AE",
    "#D78FB7",
    "#E49CC2",
    "#F1A9C7",
    "#F7B6D2"
]
    fig = go.Figure()
    fig.add_trace(go.Bar(x = df["CURSO"].unique(),
                         y = df["CURSO"].value_counts(),
                         marker_color = colores))
    
    fig.update_layout(
        title = "Número de personas en los diferentes tipos de cursos",
        xaxis_title = "Curso",
        yaxis_title = "Cantidad de personas",
        xaxis_tickmode = "array",
        xaxis_tickvals = df["CURSO"][:3531]
    
    )

    return fig

# Definir la función para crear el gráfico de los cursos
def grafico_pais_nacimiento(df):
    colores = ["#31293F", "#554D74", "#796EA8"]
    contenido = df["PAIS  NACIMIENTO"].value_counts()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=contenido.index, y=contenido, marker_color = colores))
    fig.update_layout(
        title="Países de origen de las personas que asisten al curso",
        xaxis_title="Paises",
        yaxis_title="Cantidad de personas"
    )

    return fig

# Definir la función para crear el gráfico de los instructores
def grafico_instructor(df):
    colores = colores_10 = [
    "#75827A",
    "#828F87",
    "#9C9C92",
    "#A9A9A7",
    "#B6B6D2"
    ]
    instructor_cantidad = df["INSTRUCTOR"].value_counts().nlargest(5)
    instructor_sort = instructor_cantidad.sort_values(ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=instructor_sort, y=instructor_sort.index, orientation="h", marker_color=colores))
    fig.update_layout(
    title="Los 5 instructores que más cursos dictan en la empresa RG ALTURAS",
    xaxis_title="Cantidad de personas a las que les dictó clase",
    yaxis_title="Instructor"
    )
    
    return fig

# Definir la función para crear el gráfico del nivel educativo
def grafico_nivel_edu(df):
    contenido = df["NIVEL EDUCATIVO"].value_counts()
    colores = [
    "#ff0000",
    "#ff7f00",
    "#ffff00",
    "#ff9900",
    "#ffcc00",
    "#ffc000",
    "#ffffcc",
    "#ffeeee",
    "#ffeeff",
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x = contenido.index, y = contenido, marker_color = colores))
    fig.update_layout(
    title = "Número de personas en los diferentes niveles educativos",
    yaxis_title = "Cantidad de personas",
    xaxis_title = "Nivel Educativo"
    )
    
    return fig

# Definir la función para crear el gráfico del nivel educativo
def grafico_analisis_emp(df):
    emp = df["EMPRESA"].value_counts().nlargest(10)
    emp_sort = emp.sort_values(ascending=True)
    colores = [
    "#726A72",
    "#8A778D",
    "#A28498",
    "#BA91A3",
    "#CCA8AE",
    "#D6B5B7",
    "#E3C2C2",
    "#F0CFC7",
    "#F7D9D2"
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=emp_sort, y=emp_sort.index, orientation="h", marker_color= colores))
    fig.update_layout(
    title = "Las 10 empresas de donde vienen más trabajadores a realizar el curso de alturas",
    xaxis_title = "Empresas",
    yaxis_title = "Cantidad de personas"
    )
    
    return fig

# Definir la función para crear el gráfico del área de trabajo de los inscritos en el curso
def grafico_area_tra(df):
    area = df["AREA DE TRABAJO"].value_counts().nlargest(10)
    valores = area.index
    frecuencias = area.values
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=valores, values=frecuencias))
    fig.update_layout(title = "Las 10 áreas de trabajo donde más trabajan las personas que asisten al curso")
    
    return fig

# Definir la función para crear el gráfico de los cargos que ejercen los estudiantes
def grafico_cargos(df):
    cargo = df["CARGO ACTUAL"].value_counts().nlargest(10).sort_values(ascending=False)
    valores = cargo.index
    frecuencias = cargo.values
    colores = [
    "#52C41A",
    "#72D924",
    "#93E429",
    "#B4ED2E",
    "#D5F033",
    "#F5F338",
    "#F8E63C",
    "#F1D940",
    "#E4D244",
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=valores, y=frecuencias, marker_color = colores))
    fig.update_layout(
    title="Los 10 cargos de trabajo donde más se encuentran las personas que asisten al curso",
    xaxis_title="Cantidad de personas",
    yaxis_title="Cargo"
    )
    
    return fig

# Definir la función para crear el gráfico del género de los estudiantes
def grafico_genero(df):
        cantidad = df["GENERO"].value_counts()
        genero = df["GENERO"].unique()
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=genero, values=cantidad))
        fig.update_layout(title="Gráfica sobre la asistencia a los cursos según su género")
        
        return fig
    
# Definir la función para crear el gráfico de la edad de los estudiantes
def grafico_edad(df):
    frecuencias = go.histogram.XBins(size=10)
    colores = ["#E7939A",
    "#F5A59C",
    "#F8B7A0",
    "#F9C9A4",
    "#FABBA8",
    "#E7CCBE",
    "#F5D6C2",
    "#F8E8D6",
    "#F9F9DE"
    ]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df["EDAD"], xbins=frecuencias, marker_color=colores))
    fig.update_layout(
        title="Gráfico de la edad de las personas que asisten al curso de alturas",
        xaxis_title="Edad",
        yaxis_title="Cantidad de personas"
    )

    return fig

"""
# Definir la función para crear el gráfico del estado de la asistencia a los cursos
def grafico_estado_asistencia(df):
    years_of_interest = [2021, 2022, 2023]
    asistencia = df["AÑO"].value_counts()
    min_year = int(asistencia.index.min())
    max_year = int(asistencia.index.max())

    fig = go.Figure()

    # Línea de asistencia
    fig.add_trace(
        go.Scatter(
            x=years_of_interest,
            y=asistencia[years_of_interest].fillna(0),
            line=dict(color="#2b9172"),
            name="Asistencia"
        )
    )

    # Puntos de interés
    fig.add_trace(
        go.Scatter(
            x=years_of_interest,
            y=[asistencia.get(year, 0) for year in years_of_interest],
            mode="markers",
            marker=dict(
                color="#2b9175",
                size=20,
                symbol="circle"
            ),
            name="Punto de interés anual"
        )
    )

    # Título, ejes y etiquetas
    fig.update_layout(
        title="Cantidad de asistencia en los diferentes años a RG ALTURAS",
        xaxis_title="Año",
        yaxis_title="Cantidad de asistencia",
        xaxis_range=[round(min_year, 0), round(max_year, 0)],
        showlegend=True,
        images=[dict(
            source="C:\\Users\\theas\\OneDrive\\Escritorio - PC\\Ejemplo Dash\\Imagen de WhatsApp 2023-10-03 a las 16.41.37_119eb856.jpg",
            xref="paper", yref="paper",
            x=0, y=1,
            sizex=1, sizey=1,
            sizing="stretch",
            opacity=0.7,
            layer="below")]
    )
    
    return fig
"""

# Definir el diseño del dashboard
app.layout = dbc.Container([
    
    html.H1("ANALISIS DE DATOS DEL CURSO DE ALTURAS"),    
    dcc.Graph(
        id = 'grafico-competencia',
        figure = grafico_competencia(df)
    ),
    dcc.Graph(
        id = 'grafico-cursos',
        figure = grafico_cursos(df)
    ),
    dcc.Graph(
        id = 'grafico-pais-nacimiento',
        figure = grafico_pais_nacimiento(df)
    ),
    dcc.Graph(
        id = 'grafico-instructores',
        figure = grafico_instructor(df)
    ),
    dcc.Graph(
        id = 'grafico-nivel-educativo',
        figure = grafico_nivel_edu(df)
    ),
    dcc.Graph(
        id = 'grafico-analisis-empresas',
        figure = grafico_analisis_emp(df)
    ),
    dcc.Graph(
        id = 'grafico-area-trabajo',
        figure = grafico_area_tra(df)
    ),
    dcc.Graph(
        id = 'grafico-cargos',
        figure = grafico_cargos(df)
    ),
    dcc.Graph(
        id = 'grafico-genero',
        figure = grafico_genero(df)
    ),
    dcc.Graph(
        id = 'grafico-edad',
        figure = grafico_edad(df)
    )
], fluid=True)

server = app.server # Esta linea la agrego o no funciona el servidor en render.com

# Correr el servidor del Dashboard
if __name__=='__main__':
    app.run_server(debug=True, port=8000)
