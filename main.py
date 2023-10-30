import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
from datetime import datetime
from gdown import download as gdownload

import plotly.graph_objects as go

# Se cargan los datos desde Google Drive
gdownload("https://docs.google.com/spreadsheets/d/1XCNSqnDDA6wqmid-pcqYHCTVTRi_AsIv/edit?usp=sharing&ouid=102944186622637096957&rtpof=true&sd=true", "BASE DATOS RG ALTURAS.xlsx", quiet=False)
# Cargar tus datos
df = pd.read_excel("BASE DATOS RG ALTURAS.xlsx", sheet_name="GENERAL", engine="openpyxl")


# Limpieza de datos
def eliminar_columnas(df):
    df = df.drop(["uni",
                "SELECCIÓN POLIZA",
                "CURSO INTERNO RG ALTURAS",
                "#SEGUIMIENTO CERTIFICADO",
                "CONSTANCIA VOCACIONAL",
                "ID CURSO MINTRAB",
                "PRIMER NOMBRE",
                "SEGUNDO NOMBRE",
                "PRIMER APELLIDO",
                "SEGUNDO APELLIDO",
                "TIPO DE DOCUMENTO",
                "# DOCUMENTO",
                "TELEFONO",
                "ARL",
                "FECHA INSCRIPCION",
                "FECHA FIN CURSO",
                "CLIENTE DE",
                "APROBO",
                "CC",
                "EPS",
                "ARL2",
                "CER MED",
                "CAR EMP",
                "POL",
                "OBSERVACIONES"],
                axis=1
                )
    
    df = df.iloc[0:3888,:]
    #df = df.dropna()
    #df = df.count()

    return df

df = eliminar_columnas(df)

limpieza_nivel_educativo = {"BACHILLERATO": "BACHILLER",
                            "TECNICO PROFESIONAL": "TECNICO",
                            "INSTALADOR": "TECNICO",
                            "TECNOLGO": "TECNOLOGO",
                            "TECNOLOGA": "TECNOLOGO",
                            "TECNOGO": "TECNOLOGO",
                            "MAESTRIA": "PROFESIONAL",
                            "POSTGRADO": "PROFESIONAL"
                            }

limpieza_empresas = {"INDEPENDIENTE": "PARTICULAR",
                    "JARAMILLO MORA": "JARAMILLO MORA CONSTRUCTORA SA",
                    "BRILLASEO": "BRILLASEO SAS",
                    "BRILLASEO AS": "BRILLASEO SAS",
                    "SERVIVALLE":"DISTRIBUIDORA SERVIVALLE SAS",
                    "EMCALI": "EMCALI EICE ESP",
                    "EMPRESAS MUNICIPALES DE CALI E.I.C.E. E.S.P.": "EMCALI EICE ESP",
                    "BECERRA GUERRERO S A S" : "BECERRA GUERRERO SAS",
                    "A Y G PROYECTOS Y MONTAJES" : "A Y G PROYECTOS Y MONTAJES SAS",
                    "DCYT": "DCYT INGENIERIA S.A.S",
                    "DCYT INGENIERIA SAS": "DCYT INGENIERIA S.A.S",
                    "PYP CONTRUCCIONES": "CONSTRUCCIONES PYP",
                    "P Y P CONSTRUCCIONES": "CONSTRUCCIONES PYP",
                    "MAKA INGENIERIA": "MAKA INGENIERIA SAS",
                    "MAKA": "MAKA INGENIERIA SAS",
                    "GESILVI": "GESILVI SAS",
                    "GOODYEAR": "GOODYEAR DE COLOMBIA SA",
                    "INCODE":"INCODE SAS",
                    "INCODE INGENIERIA CONSTRUCCION Y DISEÑO ELECTRICO S.A.S": "INCODE SAS",
                    'INCODE INGENIERIA CONSTRUCCION Y\\nDISEÑO ELECTRICO S.A.S': "INCODE SAS",
                    "CONSTRUCCIONES SAUL VIVEROS": "CONSTRUCCIONES SAUL VIVEROS SAS",
                    "SAUL VIVEROS": "CONSTRUCCIONES SAUL VIVEROS SAS",
                    "CONINGENIERIA":"CONINGENIERIA SAS",
                    "TRANSPORTES Y MANTENIMIENTO B Y B SAS.": "TRANSPORTES Y MANTYENIMIENTO B & B SAS",
                    "HIDROCONSTRUCCIONES": "HIDROCONSTRUCCIONES JV SAS",
                    "CUBIERTAS Y MACHIMBRES MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "MACHIMBRES Y CUBIERTAS MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "CUBIERTAS": "ALFA CUBIERTAS SAS",
                    "ALFA CUBIERTAS":"ALFA CUBIERTAS SAS",
                    "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE SAS": "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE S.A.S.",
                    "SAP AUTOMATIZACION": "SOLUCIONES AUTOMATICAS PROGRAMABLES SAP SAS",
                    "SAP": "SOLUCIONES AUTOMATICAS PROGRAMABLES SAP SAS",
                    "CONINGENIERIA": "CONINGENIERIA SAS",
                    "COINGENIERIA": "CONINGENIERIA SAS",
                    "ARIS GRUESO": "ARIS GRUESO CONSTRUCCIONES SAS",
                    "BLANCO Y NEGRO": "BLANCO Y NEGRO MASIVO SA",
                    "BLANCO Y NEGRO MASIVO": "BLANCO Y NEGRO MASIVO SA",
                    "RAN SERVICIOS": "RAN SERVICIOS INTEGRALES SAS",
                    "PCL": "PRODUCTOS DE CAUCHO Y LONA SAS",
                    "GESILVI":"GESILVI SAS",
                    "STORAGE GESILVI":"GESILVI SAS",
                    "JJ OS CONSTRUCCIONES":"JJ OS CONSTRUCCIONES SAS",
                    "SERVICONSTRUCCIONES": "SERVICONSTRUCCIONES HD SAS",
                    "JAM INGENIERIA": "JAM INGENIERIA Y SERVICIOS SAS",
                    "DISEÑO Y CONSTRUCCION CALI": "DISEÑO Y CONSTRUCCION CALI LTDA",
                    "JG MONTAJES":"JG INGENIERIA Y SERVICIO SAS",
                    "JG INGENIERIA": "JG INGENIERIA Y SERVICIO SAS",
                    "MARC": "MARC SAS",
                    "MANAGEMENT AND RISK CONTROL SAS": "MARC SAS",
                    "SUMA PROYECTOS": "SUMA PROYECTOS DE INGENIERIA",
                    "SUMAPROYECTOS": "SUMA PROYECTOS DE INGENIERIA",
                    "ROCAFORTE": "ROCAFORTE CONSTRUCCIONES S.A.S",
                    "REFRISERVICIOS": "REFRISERVICIOS SAS",
                    "ACABAL": "ACABAL SAS",
                    "JFR INGENIERIA": "JFR INGENIERIA CIVIL S.A.S",
                    "GEMCON": "GEMCON SAS",
                    "ACABAL JAJ SAS": "ACABADOS JAJ",
                    "RRM INGENIERIA": "RRM INGENIERIA Y CONSTRUCCION S A S",
                    "CONSTRUCCIONES Y ACABADOS  AA SAS": "CONSTRUCCIONES Y ACABADOS AA",
                    "CONSTRUCCIONES AA": "CONSTRUCCIONES Y ACABADOS AA",
                    "DISTRIACABADOS": "DISTRIACABADOS CIA Y LTDA",
                    "MACHIMBRES Y CUBIERTAS MANCILLA": "MACHIMBRES Y CUBIERTAS MANCILLA SAS",
                    "OSCAR GOMEZ Y CIA": "OSCAR GOMEZ Y CIA SAS",
                    "VENFIL INGENIERA SAS": "VENFIL INGENIERIA",
                    "HES INGENIERA": "HES INGENIERA SAS",
                    "VENFIL": "VENFIL INGENIERIA",
                    "FORMAS E INGENIERIA": "FORMAS E INGENIERIA SAS",
                    "FORMAS E INGENIERA SAS": "FORMAS E INGENIERIA SAS",
                    "LATINA INGENIERA SAS": "LATINA INGENIERIA",
                    "IMPORTACIONES TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "IMPORTADORA TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "ASESORIAS E IMPORTACIONES TROPI": "IMPORTACIONES Y ASESORIAS TROPI SAS",
                    "H Y C SOLUCIONES INTEGRALES": "H Y C SOLUCIONES INTEGRALES SAS",
                    "A Y G PROYECTOS Y MONTAJES": "A Y G PROYECTOS Y MONTAJES SAS",
                    "HIDROCONSTRUCCIONES": "HIDROCONSTRUCCIONES JV SAS",
                    "FIBER FUSION": "FIBER FUSIONES SAS",
                    "KEPPLER": "ACABADOS KEPPLER",
                    "ACABADOS KEPLEER SAS": "ACABADOS KEPPLER",
                    "ALTIVA": "ALTIVA INGENIERIA SAS",
                    "ALTIVA SAS": "ALTIVA INGENIERIA SAS",
                    "ALTIVA INGENIERIA": "ALTIVA INGENIERIA SAS",
                    "ALTIVA INGENIERIA EN TRANSPORTE VERTICAL S.A.S": "ALTIVA INGENIERIA SAS",
                    "SERVINDUSTRIALESDEL PACIFICIO SAS.": "SERVINDUSTRIALES DEL PACIFICO SAS",
                    "INSELCOM": "INSELCOM SAS",
                    "HNOVA INGENIERIA": "HNOVA INGENIERIA SAS",
                    "H NOVA INGENIERIA": "HNOVA INGENIERIA SAS",
                    "REFRIGERACION AVL": "AVL REFRIGERACION SAS",
                    "AVL REFRIGERACION": "AVL REFRIGERACION SAS",
                    "SISTEMAS AUTOMATICOS DE CONTROL": "SISTEMAS AUTOMATICOS DE CONTROL SAS",
                    "FUTURAL ALUMINIOS": "LEHNER FUTURAL Y ALUMINIOS SAS",
                    "HERNANDO OROZCO": "HERNANDO OROZCO Y CIA SAS",
                    "AMBIENTAR": "AMBIENTAR DE COLOMBIA SAS",
                    "AMBIENTAR INGENIERIA": "AMBIENTAR DE COLOMBIA SAS",
                    "APLIARQUI": "APLIARQUI SAS",
                    "PERFORACIONES Y REDES P&P SAS.": "PERFORACIONES Y REDES P&P SAS",
                    "CONSTRUCCIONES Y REDES P Y P": "PERFORACIONES Y REDES P&P SAS",
                    "CONSTRUCCIONES Y REDES": "PERFORACIONES Y REDES P&P SAS",
                    "PUBLI AP": "PUBLI AP SAS",
                    "MAKRO SOLUCIONES INDUSTRIALES LTDA.": "MAKRO SOLUCIONES INDUSTRIALES LTDA",
                    "VIDAL COBO ALEXANDER": "ACABADOS VIDAL SAS",
                    "TANK CARE": "TANK CARE SAS",
                    "REFRIPOLAR": "GRUPO REFRIPOLAR SAS",
                    "CONSTRUCTORA AIA": "CONSTRUCTORA AIA SAS",
                    "AIA": "CONSTRUCTORA AIA SAS",
                    "EDIFICAR CONSTRUCONSULTORES S.A.S": "EDIFICAR CONSTRUCONSULTORES SAS",
                    "ADVANCE ELECTRIC": "ADVANCE ELECTRIC INGENIERIA SAS",
                    "JH INVERSIONES": "JH INVERSIONES SAS",
                    "MULTISERV INDUSTRIALES": "MULTISERV INDUSTRIALES SAS",
                    "MULTISERV INDUSTRIALES S.A.S.": "MULTISERV INDUSTRIALES SAS",
                    "SERVICIOS Y SUMINISTROS DEL VALLE": "SERVICIOS Y SUMINISTROS DEL VALLE SAS",
                    "INGESA SAS": "INGESAS SAS",
                    "LUMEN": "LUMEN GRAPHICS SAS",
                    "LUMEN ": "LUMEN GRAPHICS SAS",
                    "LUMEN SAS": "LUMEN GRAPHICS SAS",
                    "DISEÑO Y CONSTRUCCION ": "DISEÑO Y CONSTRUCCION",
                    "DISEÑO Y CONSTRUCCION DE OBRAS": "DISEÑO Y CONSTRUCCION DE OBRAS SAS",
                    "AG CONSTRUCCIONES": "AG CONSTRUCCIONES SAS",
                    "CONSTRUCCIONES Y ACABADOS M.V.C S.A.S.": "CONSTRUCCIONES Y ACABADOS MVC SAS",
                    "ALMATEC LOGISTICA INTELIGENTE SAS": "ALMATEC SAS",
                    "MGA MONTAJES Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS": "MGA MONTAJE Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS",
                    "MGA": "MGA MONTAJE Y MANTENIMIENTO ELECTRICO INDUSTRIAL SAS",
                    "TRANSPORTES Y MANTYENIMIENTO B & B SAS.": "TRANSPORTES Y MANTENIMIENTO B Y B SAS",
                    "POTENCIA ELECTRICA": "POTENCIA ELECTRICA M&M SAS",
                    "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE S.A.S.": "MONTAJES ELECTRICOS INDUSTRIALES DEL VALLE SAS",
                    "INGEAS": "INGEAS SAS",
                    "TRANSPORTE YCARGA LA SULTANA S.A.S": "TRANSPORTE Y CARGA LA SULTANA SAS.",
                    "TRANSPORTE Y CARGA LA SULTANA SAS.": "TRANSPORTE Y CARGA LA SULTANA SAS",
                    "CENTRO AIRE ACONDICIONADO": "CENTRO DE SERVICIO DE AIRE ACONDICIONADO",
                    "CONSTRUCCIONES LIVIANAS": "CONSTRUCCIONES LIVIANAS ZUÑIGA SAS",
                    "SERVICIOS Y MONTAJES INDUSTRIALES ASTAIZA S.A.S.": "SERVICIOS Y MONTAJES INDUSTRIALES ASTAIZA SAS",
                    "GYG ASOCIADOS INGENIEROS CIVILIES S.A.S": "G Y G ASOCIADOS INGENIERIOS CIVILES SAS",
                    "EDGAR GONZALEZ CIA LTDA": "EDGAR GONZALEZ Y CIA LTDA",
                    "ESPECIALIDADES ELECTROMECANICAS EU": "ESPECIALIDADES ELECTROMECANICAS",
                    "MG ESTANTERIA": "MG ESTANTERIAS SAS",
                    "MG ESTANTERIA SAS": "MG ESTANTERIAS SAS",
                    "C Y F INGENIERIA": "CYF INGENIERIA Y TELECOMUNICACIONES SAS",
                    "SERVICIOS Y CONTRUCCIONES ALARCON SAS": "SERVICIOS Y CONSTRUCCIONES ALARCON SAS",
                    "UNION TEMPORAL M&C2021": "UNION TEMPORAL MYC 2021",
                    "RG ALTURAS": "RG ALTURAS SALUD Y SEGURIDAD EN EL TRABAJO SAS",
                    "REFRIGERACION CRG": "REFRIGERACION CRG SAS",
                    "JGB SAS": "JGB SA",
                    "MARIA DAISY VIAFARA": "MARIA DAYSI VIAFARA",
                    "ARTIARE SAS": "ARTIAIRE",
                    "JRINCON INGENIERIA": "J RINCON INGENIERIA",
                    "CONSMACOL ": "CONSMACOL",
                    'INGENIERIA Y \\nSUPERVISION TECNICA S.A.S': "INGENIERIA Y SUPERVISION TECNICA S.A.S",
                    "TRAZAMOS INGENIERIA": "TRAZAMOS INGENIERIA SAS",
                    "INGENIERIA DE INVERSIONES MPF": "INGENIERIA E INVERSIONES MPF SAS",
                    "DISPAPELES SAS": "DISPAPELES",
                    'EVENTOS Y LOGISTICA\\nCARVAJAL MEJIA SAS': "EVENTOS Y LOGISTICA CARVAJAL MEJIA SAS",
                    'GESTION\\nTECNOLOGIA Y DESARROLLO EMPRESARIAL SAS': "GESTION TECNOLOGIA Y DESARROLLO EMPRESARIAL SAS",
                    "MULTIPROYECTOS JERC": "MULTIPROYECTOS JERC SAS",
                    "SELDA SOLUCIONES SAS": "SELDA SAS",
                    "BANNER PRINT PUBLICIDAD": "BANNER PRINT PUBLICIDAD SAS",
                    "GR PUBLICIDAD": "GR PUBLICIDAD LTDA",
                    "FORMAS CREATIVAS": "FORMAS CREATIVAS PUBLICIDAD SAS",
                    "FORMAS CREATIVAS ": "FORMAS CREATIVAS PUBLICIDAD SAS",
                    "AMAYA": "MIGUEL AMAYA SAS",
                    "MERV": "MERV SAS",
                    "TOPOGRAFIA Y CONSTRUCCION D.C": "TOPOGRAFIA Y CONSTRUCCION DC",
                    "PROFESOR EDUARDO": "EDUARDO PROFESOR",
                    "CONCRETOS Y REDES": "CONCRETO Y REDES RYM SAS",
                    "BRICO": "BRICO INGENIERIA",
                    "TECCOI": "TECCOI SAS",
                    "VENTURELLO SAS": "VENTURELLO DISTRIBUCIONES SAS",
                    'SOLUTIONS\\nTECHNOLOGY GLOBAL SAS': "SOLUTIONS TECHNOLOGY GLOBAL SAS",
                    'PROGRESAR AL\\nFUTURO S.A.S.': "PROGRESAR AL FUTURO S.A.S.",
                    'GLOBAL\\nCONSTRUCTION COMPANY S.A.S.': "GLOBAL CONSTRUCTION COMPANY S.A.S.",
                    "ESRUCTURAS Y MAMPOSTERIA CASTRO": "ESTRUCTURAS Y MAMPOSTERIA CASTRO",
                    "ESTRUCTURA Y MAMPOSTERIA": "ESTRUCTURAS Y MAMPOSTERIA CASTRO",
                    "RESET ": "RESET- REDES SEGURIDAD Y TECNOLOGIA",
                    'ELECTRICOS LIAM\\nDAVID SAS': "ELECTRICOS LIAM DAVID SAS",
                    "RED A GAS": "RED A GAS Y CALEFACCION SAS",
                    "ELETRINTEC SAS": "ELECTRINTEC SAS",
                    "BUFALO CERRAMIENTOS Y COSNTRUCCIONES": "BUFALO CERRAMIENTOS Y CONSTRUCCIONES",
                    "ACABADOS FERNANDO PENA BERMUDEZ E HIJO S": "ACABADOS FERNANDO PENA BERMUDEZ E HIJOS",
                    "SERVI CONSTRUCCIONES": "SERVICONSTRUCCIONES HD SAS",
                    "CONVICICON SAS": "CONVICCION SAS",
                    "STG SAS": "SOLUTIONS TECHNOLOGY GLOBAL SAS",
                    "SOLITEMP S.A..": "SOLITEMP S.A.",
                    "RICARD": "RICARD RESPUESTAS"
                    }

def limpieza_columnas(df):
    # Limpieza de la columna de "NIVEL EDUCATIVO"
    df.loc[:3887, "NIVEL EDUCATIVO"] = df.loc[:3887, "NIVEL EDUCATIVO"].replace(limpieza_nivel_educativo)
    
    df["CURSO"].replace("TRABAJADOR AUTORIZADO", "AUTORIZADO", inplace=False)
    
    # Limpieza de la columna de "EMPRESA"
    df.loc[:3887, "EMPRESA"] = df.loc[:3887, "EMPRESA"].replace(limpieza_empresas)
    
    df["FECHA INICIO CURSO"] = pd.to_datetime(df["FECHA INICIO CURSO"], format="%m/%d/%Y", errors="coerce")
    df['AÑO'] = df['FECHA INICIO CURSO'].dt.year
    df = df.dropna(subset=['AÑO'])  # Elimina filas con valores nulos en "AÑO"
    df.loc[:, 'AÑO'] = df['AÑO'].round().astype(int)
    
    df["FECHA  NACIMIENTO"] = pd.to_datetime(df["FECHA  NACIMIENTO"], format='%m/%d/%Y', errors='coerce')
    df_fechas_validas = df[df["FECHA  NACIMIENTO"].notnull()]
    fecha_actual = datetime.now()
    df_fechas_validas.loc[:, "DIFERENCIA DE DIAS"] = (fecha_actual - df_fechas_validas["FECHA  NACIMIENTO"]).dt.days
    df_fechas_validas.loc[:, "EDAD"] = df_fechas_validas["DIFERENCIA DE DIAS"] / 365
    # Ahora, "EDAD" contendrá la edad de cada persona en años en el dataframe 
    df["EDAD"] = df_fechas_validas["EDAD"]
    
    return df

df = limpieza_columnas(df)

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
