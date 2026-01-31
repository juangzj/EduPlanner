import os
from openai import OpenAI
from django.db import connection

class GaideIAService:
    """
    Clase especializada en la comunicación con OpenAI para el flujo GAIDE.
    Mantiene el contexto pedagógico para evitar respuestas genéricas o vacías.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def _generar_completion(self, system_prompt, user_prompt, temperature=0.4):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"ERROR_IA: {str(e)}"

    def procesar_flujo(self, planeacion_id, prompt_usuario, modo="estructura"):
        """
        Orquestador de las fases de la planeación con memoria de contexto.
        """
        from ..models.planeacionClaseGaide import PlaneacionClaseGaide
        
        try:
            # Recuperamos la planeación actual de la BD
            planeacion = PlaneacionClaseGaide.objects.get(id=planeacion_id)
            contenido_previo = planeacion.contenido_generado or ""

            # --- CONFIGURACIÓN DE PROMPTS SEGÚN EL MODO ---
            
            if modo == "final":
                system_msg = (
                    "Eres un experto pedagogo y diseñador instruccional. Tu tarea es DESARROLLAR "
                    "COMPLETAMENTE una estructura previa. No uses corchetes [], no dejes campos vacíos "
                    "y no entregues plantillas. Escribe actividades reales, ejemplos claros y explicaciones detalladas."
                )
                user_prompt = (
                    f"Basado en esta estructura aprobada:\n\n{contenido_previo}\n\n"
                    "INSTRUCCIÓN: Desarrolla el contenido completo de la clase. "
                    "Crea los textos de las actividades, redacta las explicaciones y detalla la evaluación."
                )
                temp = 0.7 # Mayor creatividad para el desarrollo de contenido

            elif modo == "refinar":
                system_msg = (
                    "Eres un diseñador instruccional experto. Tu tarea es ajustar una estructura existente "
                    "basándote en las observaciones del docente. Mantén la coherencia con el tema original."
                )
                user_prompt = (
                    f"ESTRUCTURA ACTUAL:\n{contenido_previo}\n\n"
                    f"OBSERVACIÓN DEL DOCENTE: {prompt_usuario}\n\n"
                    "INSTRUCCIÓN: Reescribe la estructura completa aplicando los cambios solicitados. "
                    "Asegúrate de que la estructura sea sólida y no contenga espacios en blanco."
                )
                temp = 0.3 # Menor temperatura para mantener consistencia

            else: # MODO: ESTRUCTURA INICIAL
                system_msg = (
                    "Actúa como docente experto en educación media y diseñador instruccional. "
                    "Tu tarea es crear únicamente la estructura de una clase, sin desarrollar contenidos. "
                    "Debes presentar secciones claras, tipos de actividades y tipos de recursos. "
                    "Reglas estrictas: No desarrolles contenidos extensos, no expliques conceptos, "
                    "solo entrega la estructura organizada pero con ejemplos breves de qué incluir."
                )
                # Usamos el contexto dinámico de la planeación
                user_prompt = (
                    f"Genera la estructura para:\n"
                    f"Grado: {planeacion.grado}\n"
                    f"Área: {planeacion.area}\n"
                    f"Tema: {planeacion.tema}\n"
                    f"Competencia: {planeacion.competencia}\n"
                    f"Objetivos: {planeacion.objetivo_aprendizaje}\n"
                    f"Duración: {planeacion.duracion_clase}\n"
                    f"Nivel: {planeacion.nivel_grupo}\n"
                    f"Adicional: {planeacion.informacion_adicional or 'N/A'}"
                )
                temp = 0.4

            # 2. Llamada a la IA
            resultado = self._generar_completion(system_msg, user_prompt, temperature=temp)

            # 3. Persistencia de datos
            if modo == "final":
                planeacion.contenido_generado = resultado
                planeacion.planeacion_finalizada = True
            elif modo == "refinar":
                historial = planeacion.historial_refinamientos or []
                historial.append({"input": prompt_usuario, "output": resultado})
                planeacion.historial_refinamientos = historial
                planeacion.intentos_refinamiento += 1
                planeacion.contenido_generado = resultado
            else: # Estructura inicial
                planeacion.contenido_generado = resultado
            
            planeacion.save()

        except Exception as e:
            print(f"Error crítico en procesar_flujo: {e}")
        finally:
            connection.close()