# Feel-Track 🎭🧠

![Pipeline](https://i.imgur.com/1wkvHHD.png)

**Feel-Track** es una aplicación de análisis emocional basada en NLP que clasifica emociones en reseñas online utilizando modelos de lenguaje avanzados (BERT) y aprendizaje automático. La app ofrece visualizaciones interactivas y está desplegada en la nube (AWS EC2 + Docker).

---

## 🔍 Funcionalidades principales

- **Extracción automatizada de comentarios** desde YouTube, TikTok e Instagram mediante sus APIs oficiales.
- **Limpieza y preprocesamiento** de texto con funciones personalizadas que preservan la semántica emocional y permiten el análisis fino.
- **Clasificación multiclase de emociones** (alegría, tristeza, enojo, sorpresa, etc.) usando embeddings de BERT y modelos de machine learning.
- **Visualización interactiva de resultados** con Matplotlib y Seaborn para explorar patrones emocionales.
- **Interfaz web accesible** a través de Streamlit, contenerizada con Docker y desplegada en AWS EC2.

---

## ⚙️ Tecnologías y herramientas

- Python (pandas, scikit-learn, transformers)
- BERT (Hugging Face Transformers)
- Matplotlib & Seaborn
- Streamlit
- Docker
- AWS EC2

---

## 🚀 Cómo funciona

El pipeline general sigue estos pasos:

1️⃣ **Extracción de datos:**  
Recupera comentarios mediante las APIs de YouTube, TikTok e Instagram.

2️⃣ **Preprocesamiento:**  
Elimina ruido (URLs, menciones, símbolos irrelevantes) y preserva signos emocionales clave para un análisis más preciso.

3️⃣ **Vectorización:**  
Convierte el texto en vectores densos usando embeddings de BERT, capturando el significado contextual profundo.

4️⃣ **Clasificación emocional:**  
Aplica un modelo entrenado para asignar etiquetas emocionales (por ejemplo, alegría, tristeza, frustración).

5️⃣ **Visualización:**  
Presenta los resultados mediante gráficos y dashboards interactivos.

6️⃣ **Despliegue:**  
Toda la aplicación es desplegada en Streamlit, contenida en Docker y ejecutada en AWS EC2 para acceso global.
