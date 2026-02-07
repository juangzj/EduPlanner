import os
from openai import OpenAI
from django.db import connection


class GaideIAService:
    """
    Servicio de comunicacion con OpenAI para el flujo GAIDE.
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
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"ERROR_IA: {str(e)}"

    def procesar_flujo(self, planeacion_id, prompt_usuario="", modo="estructura"):
        """
        Orquestador principal del flujo de planeacion GAIDE
        """
        from ..models.planeacionClaseGaide import PlaneacionClaseGaide

        try:
            planeacion = PlaneacionClaseGaide.objects.get(id=planeacion_id)
            contenido_previo = planeacion.contenido_generado or ""

            # =========================
            # MODO: CREAR ESTRUCTURA
            # =========================
            if modo == "estructura":
                system_msg = (
                    "Actúa como docente experto en educación media y diseñador instruccional."
                )

                user_prompt = (
                    "Tu tarea es crear únicamente la estructura de una clase, sin desarrollar contenidos.\n"
                    "Debes presentar secciones claras, tipos de actividades y tipos de recursos, "
                    "pero no escribir actividades completas ni explicaciones largas.\n\n"
                    "Respeta estrictamente estas reglas:\n\n"
                    "- No desarrolles contenidos\n"
                    "- No expliques conceptos\n"
                    "- No escribas ejemplos extensos\n"
                    "- Solo entrega la estructura organizada\n\n"
                    "Usa el siguiente contexto:\n\n"
                    f"Grado: {planeacion.grado}\n"
                    f"Área: {planeacion.area}\n"
                    f"Tema: {planeacion.tema}\n"
                    f"Competencia: {planeacion.competencia}\n"
                    f"Objetivos de aprendizaje: {planeacion.objetivo_aprendizaje}\n"
                    f"Duración de la clase: {planeacion.duracion_clase}\n"
                    f"Nivel del grupo: {planeacion.nivel_grupo}\n"
                    f"Información adicional: {planeacion.informacion_adicional or 'N/A'}"
                )

                temp = 0.4

            # =========================
            # MODO: REFINAR ESTRUCTURA
            # =========================
            elif modo == "refinar":
                system_msg = (
                    "Eres un diseñador instruccional experto en educación media."
                )

                user_prompt = (
                    "Debes ajustar la estructura existente según la observación del docente.\n\n"
                    f"ESTRUCTURA ACTUAL:\n{contenido_previo}\n\n"
                    f"OBSERVACIÓN DEL DOCENTE:\n{prompt_usuario}\n\n"
                    "INSTRUCCIÓN:\n"
                    "Reescribe la estructura completa aplicando los cambios solicitados. "
                    "No desarrolles contenidos ni explicaciones."
                )

                temp = 0.3

            # =========================
            # MODO: DESARROLLO FINAL
            # =========================
            elif modo == "final":
                system_msg = (
                    "Actúa como docente experto en educación media y diseñador instruccional."
                )

                user_prompt = (
                    "A partir de la siguiente estructura de clase, debes desarrollar la clase completa, "
                    "creando actividades claras, coherentes y aplicables al aula real.\n\n"
                    "Reglas obligatorias:\n\n"
                    "- Respeta exactamente la estructura entregada\n"
                    "- No cambies los títulos ni el orden de las secciones\n"
                    "- Desarrolla actividades paso a paso\n"
                    "- Incluye tiempos aproximados por actividad\n"
                    "- Usa lenguaje claro para docentes\n"
                    "- Adapta las actividades al contexto de educación media\n\n"
                    "Entrada base:\n\n"
                    f"{contenido_previo}"
                )

                temp = 0.7

            else:
                raise ValueError("Modo no valido")

            # =========================
            # LLAMADA A IA
            # =========================
            resultado = self._generar_completion(
                system_msg=system_msg,
                user_prompt=user_prompt,
                temperature=temp
            )

            # =========================
            # PERSISTENCIA
            # =========================
            if modo == "estructura":
                planeacion.contenido_generado = resultado

            elif modo == "refinar":
                historial = planeacion.historial_refinamientos or []
                historial.append({
                    "observacion": prompt_usuario,
                    "resultado": resultado
                })
                planeacion.historial_refinamientos = historial
                planeacion.intentos_refinamiento += 1
                planeacion.contenido_generado = resultado

            elif modo == "final":
                planeacion.contenido_generado = resultado
                planeacion.planeacion_finalizada = True

            planeacion.save()
            return resultado

        except Exception as e:
            print(f"Error critico en procesar_flujo: {e}")
            return None

        finally:
            connection.close()
