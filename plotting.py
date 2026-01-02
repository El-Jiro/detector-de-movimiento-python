#importamos el dataframe de nuestro index
from index import df
#importamos las clases y métodos de bokeh.plotting
from bokeh.plotting import figure, output_file, show 

#Creamos la instancia de figure
p = figure(x_axis_type="datetime", width=500, height=100, sizing_mode="scale_both", title="Gráfico de movimientos")

"""
Llamamos al método p.quad para construir los cuadrantes de nuestra gráfica, este recibe cuatro argumentos: left, que determina donde comenzará
el rectángulo en el eje x, right que indica donde finaliza el mismo, y top y bottom, que son lo mismo pero para el eje Y, pero como estos son 
irrelevantes para nuestro gráfico los dejaremos en 0 y 1. También podemos especificar el color de los rectángulos de manera opcional
"""
q = p.quad(left=df["Inicio"], right=df["Fin"], bottom=0, top=1, color="green")

output_file("graph.html")
show(p)