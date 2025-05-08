# -- coding:utf-8 --
import networkx as nx
import matplotlib.pyplot as plt
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import io
from pydub import AudioSegment

ffmpeg_path = r"C:\ffmpeg\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"
ffprobe_path = r"C:\ffmpeg\ffmpeg-7.1-essentials_build\bin\ffprobe.exe"
AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

app = FastAPI()

# Configurar CORS
origins = ["http://127.0.0.1:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

G = nx.DiGraph()

# Definir ingredientes y platillos
relaciones = {
    ("Categorías", "Frutas"),
    ("Frutas", "Manzana"),
    ("Frutas", "Plátano"),
    ("Frutas", "Naranja"),
    ("Frutas", "Fresa"),
    ("Frutas", "Pera"),
    ("Frutas", "Mango"),
    ("Frutas", "Uva"),
    ("Frutas", "Piña"),
    ("Frutas", "Melón"),
    ("Frutas", "Sandía"),
    ("Frutas", "Durazno"),
    ("Frutas", "Ciruela"),
    ("Frutas", "Cereza"),
    ("Frutas", "Kiwi"),
    ("Frutas", "Papaya"),
    ("Frutas", "Higo"),
    ("Frutas", "Granada"),
    ("Frutas", "Maracuyá"),
    ("Frutas", "Chirimoya"),
    ("Frutas", "Tamarindo"),
    ("Frutas", "Coco"),
    ("Frutas", "Lima"),
    ("Frutas", "Limón"),
    ("Frutas", "Mandarina"),
    ("Frutas", "Toronja"),
    ("Frutas", "Frambuesa"),
    ("Frutas", "Mora"),
    ("Frutas", "Grosella"),
    ("Frutas", "Guayaba"),
    ("Frutas", "Lichi"),
    ("Frutas", "Dátil"),
    ("Frutas", "Carambola"),
    ("Frutas", "Pitahaya"),
    ("Frutas", "Feijoa"),
    ("Frutas", "Aguacate"),
    ("Frutas", "Zapote"),
    ("Frutas", "Arándano"),
    ("Frutas", "Zarzamora"),
    ("Frutas", "Mangostán"),
    ("Frutas", "Rambután"),
    ("Frutas", "Melocotón"),
    ("Frutas", "Alquejenje"),
    ("Frutas", "Jaca"),
    ("Frutas", "Mirtilo"),
    ("Frutas", "Mora azul"),
    ("Frutas", "Pomelo"),
    ("Frutas", "Macadamia"),
    ("Frutas", "Durián"),
    ("Categorías", "Verduras"),
    ("Verduras", "Zanahoria"),
    ("Verduras", "Lechuga"),
    ("Verduras", "Espinaca"),
    ("Verduras", "Brócoli"),
    ("Verduras", "Coliflor"),
    ("Verduras", "Cebolla"),
    ("Verduras", "Pimiento"),
    ("Verduras", "Calabacín"),
    ("Verduras", "Tomate"),
    ("Verduras", "Pepino"),
    ("Verduras", "Ajo"),
    ("Verduras", "Apio"),
    ("Verduras", "Berenjena"),
    ("Verduras", "Rábano"),
    ("Verduras", "Repollo"),
    ("Verduras", "Col"),
    ("Verduras", "Puerro"),
    ("Verduras", "Ejote"),
    ("Verduras", "Betabel"),
    ("Verduras", "Nabo"),
    ("Verduras", "Perejil"),
    ("Verduras", "Cilantro"),
    ("Verduras", "Champiñón"),
    ("Verduras", "Papa"),
    ("Verduras", "Camote"),
    ("Verduras", "Jengibre"),
    ("Verduras", "Alcachofa"),
    ("Verduras", "Esparrago"),
    ("Verduras", "Chayote"),
    ("Categorías", "Legumbres"),
    ("Legumbres", "Lentejas"),
    ("Legumbres", "Frijoles"),
    ("Legumbres", "Garbanzos"),
    ("Legumbres", "Habas"),
    ("Legumbres", "Alubias"),
    ("Legumbres", "Soja"),
    ("Legumbres", "Guisantes"),
    ("Categorías", "Lácteos"),
    ("Lácteos", "Leche"),
    ("Lácteos", "Queso"),
    ("Lácteos", "Yogur"),
    ("Lácteos", "Mantequilla"),
    ("Lácteos", "Crema"),
    ("Lácteos", "Requesón"),
    ("Lácteos", "Nata"),
    ("Lácteos", "Leche condensada"),
    ("Lácteos", "Leche evaporada"),
    ("Categorías", "Aceites"),
    ("Aceites", "Aceite de oliva"),
    ("Aceites", "Aceite de girasol"),
    ("Aceites", "Aceite de maíz"),
    ("Aceites", "Aceite de canola"),
    ("Aceites", "Aceite de soya"),
    ("Aceites", "Aceite de coco"),
    ("Aceites", "Aceite de palma"),
    ("Aceites", "Aceite de ajonjolí"),
    ("Aceites", "Aceite de nuez"),
    ("Aceites", "Aceite de almendra"),
    ("Aceites", "Aceite de aguacate"),
    ("Aceites", "Aceite de linaza"),
    ("Aceites", "Aceite de pepita de uva"),
    ("Categorías", "Cereales"),
    ("Cereales", "Arroz"),
    ("Cereales", "Trigo"),
    ("Cereales", "Avena"),
    ("Cereales", "Maíz"),
    ("Cereales", "Cebada"),
    ("Cereales", "Centeno"),
    ("Cereales", "Quinoa"),
    ("Categorías", "Setas"),
    ("Setas", "Champiñón"),
    ("Setas", "Trufa"),
    ("Categorías", "Pescados"),
    ("Pescados", "Salmón"),
    ("Pescados", "Atún"),
    ("Pescados", "Bacalao"),
    ("Pescados", "Merluza"),
    ("Pescados", "Sardina"),
    ("Pescados", "Trucha"),
    ("Pescados", "Lubina"),
    ("Pescados", "Dorada"),
    ("Pescados", "Tilapia"),
    ("Pescados", "Pez espada"),
    ("Pescados", "Jurel"),
    ("Pescados", "Caballa"),
    ("Pescados", "Rodaballo"),
    ("Pescados", "Anchoa"),
    ("Pescados", "Corvina"),
    ("Categorías", "Carnes"),
    ("Carnes", "Res"),
    ("Carnes", "Cerdo"),
    ("Carnes", "Pollo"),
    ("Carnes", "Cordero"),
    ("Carnes", "Pavo"),
    ("Carnes", "Conejo"),
    ("Carnes", "Ternera"),
    ("Carnes", "Búfalo"),
    ("Carnes", "Codorniz"),
    ("Carnes", "Pato"),
    ("Categorías", "Especias"),
    ("Especias", "Pimienta negra"),
    ("Especias", "Canela"),
    ("Especias", "Clavo de olor"),
    ("Especias", "Nuez moscada"),
    ("Especias", "Jengibre"),
    ("Especias", "Cúrcuma"),
    ("Especias", "Comino"),
    ("Especias", "Pimentón"),
    ("Especias", "Cilantro"),
    ("Especias", "Orégano"),
    ("Especias", "Tomillo"),
    ("Especias", "Romero"),
    ("Especias", "Laurel"),
    ("Especias", "Azafrán"),
    ("Especias", "Anís estrellado"),
    ("Especias", "Mostaza en grano"),
    ("Especias", "Cardamomo"),
    ("Especias", "Hinojo"),
    ("Especias", "Ajo en polvo"),
    ("Especias", "Cebolla en polvo"),
    ("Categorías", "Frutos Secos"),
    ("Frutos Secos", "Nueces"),
    ("Frutos Secos", "Almendras"),
    ("Frutos Secos", "Avellanas"),
    ("Frutos Secos", "Pistachos"),
    ("Frutos Secos", "Castañas"),
    ("Frutos Secos", "Anacardos"),
    ("Frutos Secos", "Cacahuates"),
    ("Frutos Secos", "Piñones"),
    ("Categorías", "Tubérculos"),
    ("Tubérculos", "Papa"),
    ("Tubérculos", "Camote"),
    ("Tubérculos", "Yuca"),
    ("Tubérculos", "Jengibre"),
    ("Tubérculos", "Jícama"),
    ("Tubérculos", "Rábano"),
    ("Tubérculos", "Betabel"),
    ("Tubérculos", "Zanahoria"),
    ("Tubérculos", "Chayote"),
    ("Categorías", "Mariscos"),
    ("Mariscos", "Camarón"),
    ("Mariscos", "Langosta"),
    ("Mariscos", "Mejillón"),
    ("Mariscos", "Calamar"),
    ("Mariscos", "Ostra"),
    ("Categorías", "Endulzantes"),
    ("Endulzantes", "Azúcar blanca"),
    ("Endulzantes", "Azúcar morena"),
    ("Endulzantes", "Miel"),
    ("Endulzantes", "Panela"),
    ("Endulzantes", "Melaza"),
    ("Endulzantes", "Stevia"),
    ("Endulzantes", "Jarabe de agave"),
    ("Endulzantes", "Jarabe de arce"),
    ("Categorías", "Salsas"),
    ("Salsas", "Salsa de tomate"),
    ("Salsas", "Salsa de soya"),
    ("Salsas", "Mayonesa"),
    ("Salsas", "Mostaza"),
    ("Salsas", "Salsa BBQ"),
    ("Salsas", "Salsa bechamel"),
    ("Salsas", "Salsa pesto"),
    ("Salsas", "Salsa tártara"),
    ("Salsas", "Salsa holandesa"),
    ("Salsas", "Salsa de mostaza"),
    ("Salsas", "Salsa de ostras"),
    ("Salsas", "Salsa agridulce"),
    ("Salsas", "Salsa de chile"),
    ("Salsas", "Salsa verde"),
    ("Salsas", "Salsa roja"),
    ("Salsas", "Salsa guacamole"),
    ("Salsas", "Salsa de ajo"),
    ("Categorías", "Hierbas Aromáticas"),
    ("Hierbas Aromáticas", "Albahaca"),
    ("Hierbas Aromáticas", "Orégano"),
    ("Hierbas Aromáticas", "Tomillo"),
    ("Hierbas Aromáticas", "Romero"),
    ("Hierbas Aromáticas", "Perejil"),
    ("Hierbas Aromáticas", "Cilantro"),
    ("Hierbas Aromáticas", "Menta"),
    ("Hierbas Aromáticas", "Hierbabuena"),
    ("Hierbas Aromáticas", "Laurel"),
    ("Hierbas Aromáticas", "Salvia"),
    ("Hierbas Aromáticas", "Estragón"),
    ("Hierbas Aromáticas", "Eneldo"),
    ("Hierbas Aromáticas", "Cebollino"),
    ("Hierbas Aromáticas", "Lemongrass"),
    ("Zanahoria", "Ensaladas de zanahoria"),
    ("Zanahoria", "Pastel de zanahoria"),
    ("Zanahoria", "Galletas de zanahoria"),
    ("Zanahoria", "Crema de zanahoria"),
    ("Zanahoria", "Tortilla de zanahoria"),
    ("Albahaca", "Salsa de tomate casera"),
    ("Albahaca", "Pasta pesto"),
    ("Albahaca", "Ensalada caprese"),
    ("Albahaca", "Gnocchi al pesto"),
    ("Albahaca", "Sándwich de mozzarella y tomate"),
    ("Orégano", "Berenjenas a la parmesana"),
    ("Orégano", "Pasta puttanesca"),
    ("Orégano", "Chili con carne"),
    ("Orégano", "Sopa minestrone"),
    ("Orégano", "Quesadillas de pollo y orégano"),
    ("Tomillo", "Risotto de setas"),
    ("Tomillo", "Guiso de ternera"),
    ("Tomillo", "Salsa de champiñones"),
    ("Tomillo", "Pan casero con hierbas"),
    ("Tomillo", "Tarta de cebolla y tomillo"),
    ("Romero", "Aceite aromatizado con romero"),
    ("Romero", "Salmón al horno con romero"),
    ("Romero", "Costillas de cerdo asadas"),
    ("Romero", "Pechuga de pavo al horno"),
    ("Romero", "Pasta con mantequilla de romero"),
    ("Perejil", "Salsa verde"),
    ("Perejil", "Pasta al ajillo con perejil"),
    ("Perejil", "Crema de zanahoria y perejil"),
    ("Perejil", "Albóndigas en salsa"),
    ("Perejil", "Frittata de espinacas y perejil"),
    ("Cilantro", "Arroz con pollo al cilantro"),
    ("Cilantro", "Chutney de cilantro"),
    ("Cilantro", "Salsa de yogur con cilantro"),
    ("Cilantro", "Brochetas de pollo con cilantro"),
    ("Cilantro", "Curry de garbanzos y cilantro"),
    ("Menta", "Batido de fresa y menta"),
    ("Menta", "Galletas de chocolate y menta"),
    ("Menta", "Pollo al limón y menta"),
    ("Menta", "Ensalada de sandía y menta"),
    ("Menta", "Bizcocho de menta y chocolate"),
    ("Hierbabuena", "Sorbete de limón y hierbabuena"),
    ("Hierbabuena", "Arroz al estilo marroquí"),
    ("Hierbabuena", "Sopa de tomate fría con hierbabuena"),
    ("Hierbabuena", "Zumo de piña y hierbabuena"),
    ("Hierbabuena", "Brochetas de cordero y hierbabuena"),
    ("Laurel", "Salsa de carne con laurel"),
    ("Laurel", "Arroz con mariscos"),
    ("Laurel", "Pollo guisado"),
    ("Laurel", "Sopa de alubias"),
    ("Laurel", "Cazuela de mariscos"),
    ("Salvia", "Ñoquis con mantequilla de salvia"),
    ("Salvia", "Risotto de calabaza y salvia"),
    ("Salvia", "Salsa cremosa de salvia"),
    ("Salvia", "Lentejas estofadas con salvia"),
    ("Salvia", "Frittata de queso y salvia"),
    ("Estragón", "Pechuga de pollo al estragón"),
    ("Estragón", "Sopa de mariscos"),
    ("Estragón", "Verduras al vapor con estragón"),
    ("Estragón", "Tortilla francesa con estragón"),
    ("Estragón", "Salsa de crema con estragón"),
    ("Eneldo", "Pasta con eneldo y salmón"),
    ("Eneldo", "Crema de calabacín y eneldo"),
    ("Eneldo", "Pan con semillas de eneldo"),
    ("Eneldo", "Salsa de mostaza y eneldo"),
    ("Eneldo", "Patatas al horno con eneldo"),
    ("Cebollino", "Dip de queso crema y cebollino"),
    ("Cebollino", "Sopa de pollo y cebollino"),
    ("Cebollino", "Fideos chinos con cebollino"),
    ("Cebollino", "Crepes saladas con cebollino"),
    ("Cebollino", "Tortilla de patatas con cebollino"),
    ("Lemongrass", "Pollo asado al lemongrass"),
    ("Lemongrass", "Sopa vietnamita Pho"),
    ("Lemongrass", "Arroz jazmín con lemongrass"),
    ("Lemongrass", "Tofu al lemongrass"),
    ("Lemongrass", "Salmón marinado con lemongrass"),
    ("Albahaca", "Pesto"),
    ("Albahaca", "Pizza Margarita"),
    ("Albahaca", "Caprese"),
    ("Albahaca", "Sopa de tomate"),
    ("Albahaca", "Pasta al pomodoro"),
    ("Orégano", "Pizza"),
    ("Orégano", "Salsa boloñesa"),
    ("Orégano", "Lasaña"),
    ("Orégano", "Pan de ajo"),
    ("Orégano", "Pollo al horno"),
    ("Tomillo", "Pollo al horno"),
    ("Tomillo", "Sopa de lentejas"),
    ("Tomillo", "Guiso de cordero"),
    ("Tomillo", "Papas asadas"),
    ("Tomillo", "Pescado al vapor"),
    ("Romero", "Pollo rostizado"),
    ("Romero", "Cordero asado"),
    ("Romero", "Papas al horno"),
    ("Romero", "Focaccia"),
    ("Romero", "Sopa de calabaza"),
    ("Perejil", "Tabulé"),
    ("Perejil", "Sopa de pescado"),
    ("Perejil", "Hummus"),
    ("Perejil", "Tortilla de patatas"),
    ("Perejil", "Ensalada griega"),
    ("Cilantro", "Guacamole"),
    ("Cilantro", "Ceviche"),
    ("Cilantro", "Pho"),
    ("Cilantro", "Tacos"),
    ("Cilantro", "Ensalada de mango"),
    ("Menta", "Té de menta"),
    ("Menta", "Tabulé"),
    ("Menta", "Helado de menta"),
    ("Menta", "Limonada de menta"),
    ("Menta", "Cordero con menta"),
    ("Hierbabuena", "Mojito"),
    ("Hierbabuena", "Té árabe"),
    ("Hierbabuena", "Ensalada de frutas"),
    ("Hierbabuena", "Salsa verde"),
    ("Hierbabuena", "Sopa fría de pepino"),
    ("Laurel", "Estofado de carne"),
    ("Laurel", "Sopa de lentejas"),
    ("Laurel", "Arroz con pollo"),
    ("Laurel", "Caldo de res"),
    ("Laurel", "Pasta con salsa de tomate"),
    ("Salvia", "Ravioles de calabaza"),
    ("Salvia", "Pollo a la mantequilla"),
    ("Salvia", "Sopa de verduras"),
    ("Salvia", "Chuletas de cerdo"),
    ("Salvia", "Mantequilla de salvia"),
    ("Estragón", "Salsa bearnesa"),
    ("Estragón", "Pollo al estragón"),
    ("Estragón", "Sopa de pollo"),
    ("Estragón", "Ensalada de papas"),
    ("Estragón", "Salmón a la parrilla"),
    ("Eneldo", "Salmón gravlax"),
    ("Eneldo", "Sopa de pepino"),
    ("Eneldo", "Salsa tártara"),
    ("Eneldo", "Papas con crema"),
    ("Eneldo", "Pescado al eneldo"),
    ("Cebollino", "Crema agria con cebollino"),
    ("Cebollino", "Omelette"),
    ("Cebollino", "Sopa de papa"),
    ("Cebollino", "Puré de papas"),
    ("Cebollino", "Salmón ahumado"),
    ("Lemongrass", "Sopa tailandesa Tom Yum"),
    ("Lemongrass", "Pollo al curry"),
    ("Lemongrass", "Té de lemongrass"),
    ("Lemongrass", "Sopa de coco tailandesa"),
    ("Lemongrass", "Camarones al lemongrass"),
    ("Salsa BBQ", "Costillas con salsa BBQ"),
    ("Salsa BBQ", "Pastel de carne con salsa BBQ"),
    ("Salsa BBQ", "Calamar con salsa BBQ"),
    ("Salsa BBQ", "Albondigas con salsa BBQ"),
    ("Salsa BBQ", "Alitas con salsa BBQ"),
    ("Salsa BBQ", "Fajitas de pollo con salsa BBQ"),
    ("Salsa BBQ", "Pollo con salsa BBQ"),
    ("Salsa BBQ", "Lomo de cerdo con salsa BBQ"),
    ("Salsa BBQ", "Empanadas de pollo con salsa BBQ"),
    ("Pollo", "Pollo con salsa BBQ"),
    ("Pollo", "Pollo rostizado"),
    ("Pollo", "Empanadas de pollo"),
    ("Pollo", "Tostadas de pollo desebreado rostizado"),
    ("Pollo", "Tostadas de pollo desebreado"),
    ("Pollo", "Empanadas de pollo con salsa BBQ"),
    ("Harina", "Tortillas"),
    ("Harina", "Galletas"),
    ("Harina", "Pastel"),
    ("Harina", "Hotcakes"),
    ("Harina", "Muffins"),
    ("Harina", "Crepas"),
    ("Harina", "Donas"),
    ("Harina", "Buñuelos"),
    ("Harina", "Empanadas"),
    ("Harina", "Pizza"),
    ("Leche", "Pastel"),
    ("Leche", "Flan"),
    ("Leche", "Helado"),
    ("Leche", "Atole"),
    ("Leche", "Natilla"),
    ("Leche", "Budín"),
    ("Leche", "Arroz con leche"),
    ("Leche", "Batido"),
    ("Leche", "Crema pastelera"),
    ("Leche", "Cajeta"),
    ("Huevo", "Pastel"),
    ("Huevo", "Flan"),
    ("Huevo", "Omelette"),
    ("Huevo", "Tortilla española"),
    ("Huevo", "Huevos revueltos"),
    ("Huevo", "Huevos rancheros"),
    ("Huevo", "Soufflé"),
    ("Huevo", "Quiche"),
    ("Huevo", "Crepas"),
    ("Huevo", "Mayonesa"),
    ("Azúcar", "Pastel"),
    ("Azúcar", "Flan"),
    ("Azúcar", "Galletas"),
    ("Azúcar", "Merengue"),
    ("Azúcar", "Dulce de leche"),
    ("Azúcar", "Natilla"),
    ("Azúcar", "Caramelo"),
    ("Azúcar", "Tarta"),
    ("Azúcar", "Helado"),
    ("Azúcar", "Mermelada"),
    ("Queso", "Pizza"),
    ("Queso", "Lasagna"),
    ("Queso", "Quesadilla"),
    ("Queso", "Fondue"),
    ("Queso", "Enchiladas"),
    ("Queso", "Empanadas"),
    ("Queso", "Pan de queso"),
    ("Queso", "Tarta de queso"),
    ("Queso", "Sandwich"),
    ("Queso", "Soufflé"),
    ("Tomate", "Pizza"),
    ("Tomate", "Salsa"),
    ("Tomate", "Sopa"),
    ("Tomate", "Ensalada"),
    ("Tomate", "Gazpacho"),
    ("Tomate", "Bruschetta"),
    ("Tomate", "Ketchup"),
    ("Tomate", "Pico de gallo"),
    ("Tomate", "Shakshuka"),
    ("Tomate", "Ratatouille"),
    ("Carne", "Hamburguesa"),
    ("Pan", "Hamburguesa"),
    ("Lechuga", "Ensalada"),
    ("Zanahoria", "Ensalada"),
    ("Pepino", "Ensalada"),
    ("Pollo", "Pollo asado"),
    ("Pimienta", "Pollo asado"),
    ("Pasta", "Espagueti"),
    ("Salsa de Tomate", "Espagueti"),
    ("Albahaca", "Espagueti"),
    ("Zanahoria", "Ensaladas de zanahoria"),
    ("Zanahoria", "Pastel de zanahoria"),
    ("Zanahoria", "Galletas de zanahoria"),
    ("Zanahoria", "Crema de zanahoria"),
    ("Zanahoria", "Tortilla de zanahoria"),
    ("Salsa BBQ", "Costillas con salsa BBQ"),
    ("Salsa BBQ", "Pastel de carne con salsa BBQ"),
    ("Salsa BBQ", "Calamar con salsa BBQ"),
    ("Salsa BBQ", "Albondigas con salsa BBQ"),
    ("Salsa BBQ", "Alitas con salsa BBQ"),
    ("Salsa BBQ", "Fajitas de pollo con salsa BBQ"),
    ("Salsa BBQ", "Pollo con salsa BBQ"),
    ("Salsa BBQ", "Lomo de cerdo con salsa BBQ"),
    ("Salsa BBQ", "Empanadas de pollo con salsa BBQ"),
    ("Pollo", "Pollo con salsa BBQ"),
    ("Pollo", "Pollo rostizado"),
    ("Pollo", "Empanadas de pollo"),
    ("Pollo", "Tostadas de pollo desebreado rostizado"),
    ("Pollo", "Tostadas de pollo desebreado"),
    ("Pollo", "Empanadas de pollo con salsa BBQ"),
}

G.add_edges_from(relaciones)


# Definimos el modelo de datos para las solicitudes de la API
class PreguntaRequest(BaseModel):
    pregunta: str

@app.get("/")
def home():
    return {"mensaje": "Chat de cocina activo."}
@app.post("/pregunta")
def responder_pregunta(pregunta_req: PreguntaRequest):
    pregunta = pregunta_req.pregunta.lower()
    # pREGUNTA ¿QUE SON?
    
    for nodo in G.nodes:
        if f"qué son las {nodo.lower()}" in pregunta or f"que son los {nodo.lowler()}" in pregunta:
            subcategorias = list(G.successors(nodo))
            if subcategorias:
                return JSONResponse(
                    content={
                        "respuesta": f"{nodo} es una categoría de alimentos que incluye: {', '.join(subcategorias)}."
                    }
                )
            else:
                return JSONResponse(
                    content={
                        "respuesta": f"{nodo} es un alimento en esta clasificación."
                    }
                )
    for nodo in G.nodes:
        if f"qué platillos contienen {nodo.lower()}" in pregunta:
            hijos = list(G.successors(nodo))
            if hijos:
                return JSONResponse(
                    content={
                        "respuesta": f"Los platillos que contienen {nodo} son: {', '.join(hijos)}."
                    }
                )
    for nodo in G.nodes:
        if f"cuál es la categoría de {nodo.lower()}" in pregunta or f"cuales son las categorias de {nodo.lowler()}" in pregunta:
            padres = list(G.predecessors(nodo))
            if padres:
                return JSONResponse(
                    content={
                        "respuesta": f"{nodo} pertenece a la categoría: {', '.join(padres)}."
                    }
                )

    # Pregunta: ¿Qué relación tienen ... y ...?
    # conceptos = [nodo for nodo in G.nodes if nodo.lower() in pregunta]

    # if len(conceptos) == 2:
    #     nodo1, nodo2 = conceptos
    #     if G.has_edge(nodo1, nodo2):
    #         return JSONResponse(content={"respuesta": f"{nodo2} es una subcategoría de {nodo1}."})
    #     elif G.has_edge(nodo2, nodo1):
    #         return JSONResponse(content={"respuesta": f"{nodo2} es una subcategoría de {nodo1}."})
    #     else:
    #         return JSONResponse(content={"respuesta": f"{nodo1} y {nodo2} son alimentos, pero no tienen una relación directa en esta clasificación."})

    for nodo in G.nodes:
        if nodo.lower() in pregunta:
            if G.in_degree(nodo) == 0 and G.out_degree(nodo) > 0:
                return JSONResponse(content={"respuesta": f"{nodo} es un ingrediente."})
            elif G.in_degree(nodo) > 0:
                return JSONResponse(content={"respuesta": f"{nodo} es un platillo."})
    # Manejo de pregunta: "¿Qué ingredientes tiene .....?"
    nodos_en_pregunta = [nodo for nodo in G.nodes if nodo.lower() in pregunta]
    if len(nodos_en_pregunta) == 1:
        platillo = nodos_en_pregunta[0]
        ingredientes = list(G.predecessors(platillo))
        if ingredientes:
            return JSONResponse(
                content={
                    "respuesta": f"Los ingredientes(s) que contiene el platillo {platillo} son: {', '.join(ingredientes)}."
                }
            )
        else:
            return JSONResponse(
                content={
                    "respuesta": f"{platillo} no tiene ingredientes registrados en este modelo."
                }
            )
    # Manejo de pregunta: "¿Qué ingredientes comparten....?"
    if "comparten" in pregunta:
        # Buscar platillos en la pregunta
        platillos = [
            nodo
            for nodo in G.nodes
            if nodo.lower() in pregunta and list(G.predecessors(nodo))
        ]
        if len(platillos) >= 2:
            ingredientes_sets = [set(G.predecessors(p)) for p in platillos]
            ingredientes_comunes = set.intersection(*ingredientes_sets)
            if ingredientes_comunes:
                return JSONResponse(
                    content={
                        "respuesta": f"Los platillos {', '.join(platillos)} comparten los siguientes ingredientes: {', '.join(ingredientes_comunes)}."
                    }
                )
            else:
                return JSONResponse(
                    content={
                        "respuesta": f"Los platillos {', '.join(platillos)} no comparten ingredientes en este modelo."
                    }
                )


    # Manejo de pregunta: "¿Cuáles platillos contienen los ingredientes ...?"
    if "contienen" in pregunta and "ingrediente" in pregunta:
        # Extraer posibles ingredientes buscando nodos que no tengan salidas (considerados ingredientes)
        posibles_ingredientes = [
            nodo for nodo in G.nodes if G.out_degree(nodo) > 0 or G.in_degree(nodo) == 0
        ]
        ingredientes_preg = [
            ing for ing in posibles_ingredientes if ing.lower() in pregunta
        ]
        if ingredientes_preg:
            # Buscar platillos que tengan TODOS esos ingredientes
            platillos_result = []
            for nodo in G.nodes:
                # Considerar nodos que tienen ingredientes (platillos)
                if list(G.predecessors(nodo)):
                    ing_platillo = set(G.predecessors(nodo))
                    if all(ing in ing_platillo for ing in ingredientes_preg):
                        platillos_result.append(nodo)
            if platillos_result:
                return JSONResponse(
                    content={
                        "respuesta": f"Los platillos que contienen {', '.join(ingredientes_preg)} son: {', '.join(platillos_result)}."
                    }
                )
            else:
                return JSONResponse(
                    content={
                        "respuesta": f"No se encontraron platillos que contengan todos los ingredientes {', '.join(ingredientes_preg)}."
                    }
                )

    if pregunta.strip().lower() == "hola":
        posibles_preguntas = [
            "¿Qué son las ? ",
            "¿Qué se puede preparar con ?",
            "¿Qué ingredientes tiene ?",
            "¿Qué ingredientes comparten  y ?",
            "¿Qué platillos contienen los ingredientes y ?",
            "¿Cuáles son los ingredientes principales de?",
            "¿Es un ingrediente o un platillo?",
            "¿Qué contiene ?",
            "Con que se puede preparar?",
        ]
    mensaje = (
        "Hola, soy un asistente que te ayudará a saber más sobre cocina. "
        "Puedo responder las siguientes preguntas:\n"
        + "\n".join(f"\n - {p}" for p in posibles_preguntas)
    )

    return JSONResponse(content={"respuesta": mensaje})


@app.post("/reconoce")
async def recognize(audio_file: UploadFile = File(...)):
    try:
        contents = await audio_file.read()
        if not contents:
            raise HTTPException(
                status_code=400, detail="El archivo de audio está vacío."
            )
        audio_input = io.BytesIO(contents)
        try:
            audio_segment = AudioSegment.from_file(audio_input, format="webm")
        except Exception:
            audio_input.seek(0)
            audio_segment = AudioSegment.from_file(audio_input)

        # Exportar  WAV al buffer
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            print(f"Texto transcrito: {text}")

            # Ahora comparamos el texto con las preguntas directamente
            pregunta = text.lower()

            # Pregunta: ¿Qué es ...?
            for nodo in G.nodes:
                if f"qué son las {nodo.lower()}" in pregunta:
                    subcategorias = list(G.successors(nodo))
                    if subcategorias:
                        return JSONResponse(
                            content={
                                "respuesta": f"{nodo} es una categoría de alimentos que incluye: {', '.join(subcategorias)}."
                            }
                        )
                    else:
                        return JSONResponse(
                            content={
                                "respuesta": f"{nodo} es un alimento en esta clasificación."
                            }
                        )

            # Pregunta: ¿Qué se puede preparar con ....?
            for nodo in G.nodes:
                if f"qué se puede preparar con {nodo.lower()}" in pregunta:
                    platillos = list(G.successors(nodo))
                    if platillos:
                        return JSONResponse(
                            content={
                                "respuesta": f"Con {nodo} puedes preparar: {', '.join(platillos)}."
                            }
                        )
                    else:
                        return JSONResponse(
                            content={
                                "respuesta": f"{nodo} es un ingrediente, pero no está relacionado con ningún platillo en este modelo."
                            }
                        )

            # Pregunta: ¿Qué ingredientes tiene .....?
            nodos_en_pregunta = [nodo for nodo in G.nodes if nodo.lower() in pregunta]
            if len(nodos_en_pregunta) == 1:
                platillo = nodos_en_pregunta[0]
                ingredientes = list(G.predecessors(platillo))
                if ingredientes:
                    return JSONResponse(
                        content={
                            "respuesta": f"{platillo} se prepara con: {', '.join(ingredientes)}."
                        }
                    )
                else:
                    return JSONResponse(
                        content={
                            "respuesta": f"{platillo} no tiene ingredientes registrados en este modelo."
                        }
                    )

            # Pregunta: ¿Qué ingredientes comparten....?
            if "comparten" in pregunta:
                platillos = [
                    nodo
                    for nodo in G.nodes
                    if nodo.lower() in pregunta and list(G.predecessors(nodo))
                ]
                if len(platillos) >= 2:
                    ingredientes_sets = [set(G.predecessors(p)) for p in platillos]
                    ingredientes_comunes = set.intersection(*ingredientes_sets)
                    if ingredientes_comunes:
                        return JSONResponse(
                            content={
                                "respuesta": f"Los platillos {', '.join(platillos)} comparten los siguientes ingredientes: {', '.join(ingredientes_comunes)}."
                            }
                        )
                    else:
                        return JSONResponse(
                            content={
                                "respuesta": f"Los platillos {', '.join(platillos)} no comparten ingredientes en este modelo."
                            }
                        )

            # Pregunta: ¿Cuáles platillos contienen los ingredientes ...?
            if "contienen" in pregunta and "ingrediente" in pregunta:
                posibles_ingredientes = [
                    nodo
                    for nodo in G.nodes
                    if G.out_degree(nodo) > 0 or G.in_degree(nodo) == 0
                ]
                ingredientes_preg = [
                    ing for ing in posibles_ingredientes if ing.lower() in pregunta
                ]
                if ingredientes_preg:
                    platillos_result = []
                    for nodo in G.nodes:
                        if list(G.predecessors(nodo)):
                            ing_platillo = set(G.predecessors(nodo))
                            if all(ing in ing_platillo for ing in ingredientes_preg):
                                platillos_result.append(nodo)
                    if platillos_result:
                        return JSONResponse(
                            content={
                                "respuesta": f"Los platillos que contienen {', '.join(ingredientes_preg)} son: {', '.join(platillos_result)}."
                            }
                        )
                    else:
                        return JSONResponse(
                            content={
                                "respuesta": f"No se encontraron platillos que contengan todos los ingredientes {', '.join(ingredientes_preg)}."
                            }
                        )

            # Si no se encuentra una respuesta
            return JSONResponse(
                content={"respuesta": "No se pudo responder a la pregunta."}
            )

        except sr.UnknownValueError:
            return {"text": "No se pudo entender el audio"}
        except sr.RequestError as e:
            return {"text": f"Error al conectar con el servicio: {e}"}
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
