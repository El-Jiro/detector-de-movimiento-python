#importamos el dataframe de nuestro index
from index import df
from bokeh.plotting import figure, output_file, show 
from bokeh.models import HoverTool, FixedTicker, ColumnDataSource

"""
Ya que HoverTool no es capaz de parsear correctamente los objetos de tipo DateTime, necesitaremos convertir nuestras marcas de tiempo
a strings antes de parsear el DataFrame a un ColumnDataSource, para esto añadimos al objeto df dos nuevas columnas llamadas Inicio_string
y Fin_String, que serán igual a las columnas inicio y fin originales pero aplicándoles el método .dt.srtftime
"""
df["Inicio_string"] = df["Inicio"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["Fin_string"] = df["Fin"].dt.strftime("%Y-%m-%d %H:%M:%S")

#Convertimos nuestro dataframe de pandas a un objeto ColumnDataSource, que es una manera estandarizada de añadir datos a bokeh
cds = ColumnDataSource(df)

#Creamos la instancia de figure
p = figure(x_axis_type="datetime", width=500, height=100, sizing_mode="scale_both", title="Gráfico de movimientos")

#Eliminamos la cuadrícula vertical
p.ygrid.visible = False

#Eliminamos los ticks menores
p.yaxis.minor_tick_line_color = None
p.yaxis.minor_tick_in = 0
p.yaxis.minor_tick_out = 0

#Eliminamos los ticks mayores intermedios con FixedTicker, dejando únicamente 0 y 1
p.yaxis.ticker = FixedTicker(ticks=[0,1])

"""
Creamos una instancia de HoverTools, la cual recibe en su constructor un único argumento llamado tooltips, es decir el texto que se
mostrará al posar el cursor sobre cada cuadrante en forma de una lista de tuplas o un diccionario, cada tupla contendrá dos elementos: 
una etiqueta (Inicio/Fin) y el valor del timestamp para la misma, para obtener el valor simplemente hacemos referencia al nombre de la 
columna correspondiente de nuestro objeto cds con @
"""
hover = HoverTool(tooltips = {"Inicio": "@Inicio_string", "Fin": "@Fin_string"})

#Añadimos el objeto hover a nuestro gráfico con el método add_tools
p.add_tools(hover)

"""
Llamamos al método p.quad para construir los cuadrantes de nuestra gráfica, este recibe cuatro argumentos: left, que determina donde comenzará
el rectángulo en el eje x, right que indica donde finaliza el mismo, y top y bottom, que son lo mismo para el eje Y, pero como estos son 
irrelevantes para nuestro gráfico los dejaremos en 0 y 1. También podemos especificar el color de los rectángulos de manera opcional. Añadimos
nuestra instancia de ColumnDataSource en el atributo source, de esta manera ya no necesitamos referenciar el dataframe, simplemente pasamos los 
nombres de las columnas como strings
"""
p.quad(left="Inicio", right="Fin", bottom=0, top=1, color="green", source=cds)

#Preparamos el archivo de salida
output_file("graph.html", title="Gráfico de Movimiento")
#mostramos el gráfico
show(p)