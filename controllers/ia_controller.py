import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from models.venta_dao import VentaDAO

# 🔥 Apagamos los mensajes de alerta internos de TensorFlow para que la consola quede limpia
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

load_dotenv()

class IAController:
    def __init__(self):
        self.client = OpenAI()

    def entrenar_red_neuronal_keras(self, ventas_brutas):
        """
        Crea, entrena y ejecuta una Red Neuronal de Regresión usando Keras y TensorFlow.
        X = Secuencia de tiempo (Venta 1, Venta 2, Venta 3...)
        Y = Ganancia Neta de cada venta
        """
        try:
            if len(ventas_brutas) < 3:
                return None, "Bro, se necesitan al menos 3 ventas registradas para que la Red Neuronal pueda hallar un patrón."

            # 1. Preparar los datos con NumPy arrays (Indispensable para TensorFlow)
            # X necesita forma de matriz columna (-1, 1)
            X = np.array([i for i in range(len(ventas_brutas))], dtype=np.float32).reshape(-1, 1)
            # Y es el objetivo: Ganancia neta de la venta (v[4])
            y = np.array([float(v[4]) for v in ventas_brutas], dtype=np.float32)

            # 2. Arquitectura de la Red Neuronal (Deep Learning)
            model = Sequential([
                Dense(64, activation='relu', input_shape=(1,)), # Capa de entrada + Oculta 1
                Dense(32, activation='relu'),                  # Capa Oculta 2
                Dense(1)                                       # Capa de salida (Regresión lineal)
            ])

            # 3. Compilar el modelo con optimizador Adam y pérdida de Error Cuadrático Medio
            model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')

            # 4. Entrenar el modelo (verbose=0 para que no sature la terminal con barras de carga)
            model.fit(X, y, epochs=150, verbose=0)

            # 5. Predecir el siguiente punto en el tiempo (la próxima venta estimada)
            siguiente_punto = np.array([[len(ventas_brutas)]], dtype=np.float32)
            prediccion_futura = model.predict(siguiente_punto, verbose=0)[0][0]

            if prediccion_futura < 0: 
                prediccion_futura = 0.0

            return float(prediccion_futura), None

        except Exception as e:
            return None, f"Fallo en los tensores de Keras: {str(e)}"

    def preguntar_asistente(self, pregunta_usuario):
        try:
            # 1. Traer el historial de ventas real
            ventas_brutas = VentaDAO.obtener_todas_las_ventas()
            
            # 2. Convertir los datos a texto analizable
            historial_texto = ""
            if not ventas_brutas:
                historial_texto = "No hay ventas registradas aún en el negocio."
            else:
                for v in ventas_brutas:
                    historial_texto += f"- Producto: {v[0]} | Cantidad: {v[1]} | Costo total fab: ${v[2]} | Ingreso total: ${v[3]} | Ganancia neta: ${v[4]} | Fecha: {v[5]}\n"

            # 3. Verificar si el usuario quiere una predicción inteligente
            query = pregunta_usuario.lower()
            contexto_prediccion = ""
            
            if any(palabra in query for palabra in ["predic", "futuro", "pronostico", "keras", "tensorflow", "neuronal"]):
                # Disparamos la Red Neuronal profunda
                resultado_keras, error_keras = self.entrenar_red_neuronal_keras(ventas_brutas)
                
                if error_keras:
                    contexto_prediccion = f"\n[AVISO SISTEMA]: La red neuronal no pudo calcular por: {error_keras}\n"
                else:
                    contexto_prediccion = (
                        f"\n[DATOS DE DEEP LEARNING - KERAS/TENSORFLOW]:\n"
                        f"Acabas de ejecutar un modelo Sequential multicapa. La predicción exacta generada por las "
                        f"neuronas artificiales para la ganancia neta de la próxima transacción es de: ${resultado_keras:.2f}.\n"
                        f"Usa este dato científico obligatoriamente en tu respuesta para sorprender al usuario.\n"
                    )

            # 4. System Prompt con el contexto enriquecido
            system_prompt = (
                "Eres un experto contador y analista financiero de la pastelería 'Three Cakes'. "
                "Tu objetivo es ayudar al dueño del negocio a entender sus finanzas de forma clara, "
                "amigable, un toque ingeniosa (diciendo frases como 'bro') y muy profesional.\n\n"
                "Si te habla de algo no relacionado con las ventas o finanzas de la pastelería (como Pokémon, películas, etc.), "
                "redirígelo amablemente diciéndole que solo manejas los números de los productos de la pastelería.\n\n"
                "Aquí tienes los datos reales de las ventas actuales:\n"
                f"{historial_texto}\n"
                f"{contexto_prediccion}\n"
                "Usa estos datos exactos. Si se ejecutó la Red Neuronal, explica los resultados predichos con entusiasmo "
                "mencionando que utilizaste Keras y TensorFlow para procesar el algoritmo."
            )

            # 5. Llamada oficial a OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pregunta_usuario}
                ],
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error al conectar con el Agente de IA: {str(e)}"