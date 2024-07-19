import jinja2
import pdfkit
import os

def crea_pdf(ruta_template, info, rutacss=""):
    nombre_template = ruta_template.split("\\")[-1]
    ruta_template = ruta_template.replace(nombre_template, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_template)
    html = template.render(info)
    
    options = {
        'page-size': 'Letter',
        'margin-top': '0.05in',
        'margin-right': '0.05in',
        'margin-bottom': '0.05in',  # Corregido 'botton' a 'bottom'
        'margin-left': '0.05in',
        'encoding': 'UTF-8'
    }
    
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  # Corregido 'wkhtmltopdp' a 'wkhtmltopdf'
    
    ruta_salida = os.path.join("C:\\Users\\ASUS I5\\OneDrive\\Desktop", f"{info['pelicula']}.pdf")
    pdfkit.from_string(html, ruta_salida, css=rutacss, options=options, configuration=config)

