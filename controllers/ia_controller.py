import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from models.venta_dao import VentaDAO

# 🔥 Apagamos los mensajes de alerta internos
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 👇 Librerías pesadas comentadas para que Render no explote
# import numpy as np
# import tensorflow as tf
# from keras.models import Sequential
# from keras.layers import Dense

load_dotenv()

class IAController:
    def __init__(self):
        self.client = OpenAI()

    def entrenar_red_neuronal_keras(self, ventas_brutas):
        """
        Crea, entrena y ejecuta una Red Neuronal de Regresión usando Keras y TensorFlow.
        (ESTA FUNCIÓN ESTÁ APAGADA TEMPORALMENTE PARA EL DESPLIEGUE EN RENDER)
        """
        # 🔥 Simplemente devolvemos un mensaje de error controlado. 
        # Esto evita que se ejecute toda la matemática pesada de abajo.
        return None, "La predicción avanzada con Redes Neuronales está desactivada en la nube por límites de memoria."

        # 👇 Todo el código original se queda aquí abajo comentado (apagado) por si un día lo quieres reactivar
        # try:
        #     if len(ventas_brutas) < 3:
        #         return None, "Bro, se necesitan al menos 3 ventas registradas para que la Red Neuronal pueda hallar un patrón."
        #
        #     X = np.array([i for i in range(len(ventas_brutas))], dtype=np.float32).reshape(-1, 1)
        #     y = np.array([float(v[4]) for v in ventas_brutas], dtype=np.float32)
        #
        #     model = Sequential([
        #         Dense(64, activation='relu', input_shape=(1,)), 
        #         Dense(32, activation='relu'),                  
        #         Dense(1)                                       
        #     ])
        #
        #     model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')
        #     model.fit(X, y, epochs=150, verbose=0)
        #
        #     siguiente_punto = np.array([[len(ventas_brutas)]], dtype=np.float32)
        #     prediccion_futura = model.predict(siguiente_punto, verbose=0)[0][0]
        #
        #     if prediccion_futura < 0: 
        #         prediccion_futura = 0.0
        #
        #     return float(prediccion_futura), None
        #
        # except Exception as e:
        #     return None, f"Fallo en los tensores de Keras: {str(e)}"

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
                # Disparamos la función (que ahora solo devolverá nuestro mensaje de que está desactivada)
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