from IPython.display import display, HTML
import matplotlib.pyplot as plt
import seaborn as sns
from langdetect import detect, LangDetectException, DetectorFactory
import pandas as pd
from wordcloud import WordCloud
import pycountry


plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'

DetectorFactory.seed = 0

def show_full_dataset(df):
    with pd.option_context('display.max_columns', None,
                       'display.max_colwidth', None,
                       'display.max_rows', 100):
        display(df)

def apply_plot_config(func):
    """
    Decorador que asegura la configuración correcta de matplotlib antes de graficar.
    """
    import matplotlib.pyplot as plt

    def wrapper(*args, **kwargs):
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'DejaVu Sans'
        return func(*args, **kwargs)
    
    return wrapper


def show_image(url, width=1600):
    """
    Displays an image from a URL in a Jupyter notebook.
    """
    display(HTML(f"<img src='{url}' width={width}>"))

@apply_plot_config
def plot_histo(df, variable):
    plt.figure(figsize=(10, 5))
    sns.histplot(df[variable], bins=50, color='skyblue', kde=True)
    plt.title('Histograma: Distribución de ' + variable)
    plt.xlabel('Cantidad de caracteres')
    plt.ylabel('Frecuencia')
    plt.show()

@apply_plot_config
def plot_comments_by_time(df, time_column='time', period='M', color='lightcoral'):
    """
    Distribución de comentarios por periodo temporal.
    
    Parámetros:
    - time_column: columna ya en formato datetime.
    - period: 'M' para mes, 'Y' para año.
    """
    comments_by_period = df[time_column].dt.to_period(period).value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    comments_by_period.plot(kind='bar', color=color)
    plt.title(f'Distribución de comentarios por {"mes" if period == "M" else "año"}')
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad de comentarios')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

@apply_plot_config
def plot_correlation_scatter(df, x_var, y_var, color='blue', alpha=0.5):
    """
    Scatterplot entre dos variables numéricas.
    
    Parámetros:
    - x_var: nombre de la columna para el eje X.
    - y_var: nombre de la columna para el eje Y.
    - alpha: transparencia de los puntos.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x_var, y=y_var, color=color, alpha=alpha)
    plt.title(f'Relación entre {x_var.capitalize()} y {y_var.capitalize()}')
    plt.xlabel(x_var.capitalize())
    plt.ylabel(y_var.capitalize())
    plt.grid(True)
    plt.show()

def get_language_name(code):
    """
    Traduce un código de idioma (ISO 639-1 o 639-3) a su nombre completo.
    Si no se encuentra, devuelve el código original.
    """
    if code == 'unknown':
        return 'Desconocido'
    try:
        lang = pycountry.languages.get(alpha_2=code)
        if lang is None:
            lang = pycountry.languages.get(alpha_3=code)
        return lang.name if lang else code
    except:
        return code

@apply_plot_config
def plot_language_distribution(comment_series, sample_size=500, color='mediumseagreen'):
    """
    Detecta y grafica la distribución de idiomas en una muestra de comentarios.
    
    Parámetros:
    - comment_series: Serie de texto (columna de comentarios).
    - sample_size: número de muestras aleatorias a analizar.
    """
    def safe_detect(text):
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'
    
    sample = comment_series.dropna().astype(str)
    sample = sample[sample.apply(lambda x: len(x.strip()) > 10)]
    sample = sample.sample(n=min(sample_size, len(sample)), random_state=42)
    
    languages = sample.apply(safe_detect)
    lang_counts = languages.value_counts()
    lang_counts.index = lang_counts.index.map(get_language_name)
    
    plt.figure(figsize=(12, 6))
    lang_counts.plot(kind='bar', color=color)
    plt.title('Distribución de idiomas en muestra de comentarios', fontsize=14, fontname='DejaVu Sans')
    plt.xlabel('Idioma detectado', fontsize=12)
    plt.ylabel('Cantidad', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

@apply_plot_config
def plot_correlation_heatmap(df, numeric_cols):
    """
    Plotea un heatmap de correlación entre variables numéricas.
    
    Parámetros:
    - numeric_cols: lista de columnas numéricas a analizar
    """
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Heatmap de Correlación')
    plt.show()

def plot_class_distribution(df, class_col):
    """
    Grafica la distribución de clases en un gráfico de barras.
    
    Parámetros:
    - class_col: columna de clase (string)
    """
    plt.figure(figsize=(8, 6))
    sns.countplot(x=class_col, data=df, order=df[class_col].value_counts().index)
    plt.title('Distribución de Clases')
    plt.ylabel('Cantidad')
    plt.xlabel('Clase')
    plt.show()   

def generar_grupos(df, variable, bins, labels, nueva_columna=None):
    if nueva_columna is None:
        nueva_columna = variable + '_group'
    df[nueva_columna] = pd.cut(df[variable], bins=bins, labels=labels, right=False)
    return df

def plot_grouped_scatter_likes_reply(df, sentiment_col='bert_sentiment', likes_col='likes', reply_col='reply_count'):
    # Agrupar por clase
    grouped = df.groupby(sentiment_col).agg({
        likes_col: 'mean',
        reply_col: 'mean'
    }).reset_index()
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=grouped, x=likes_col, y=reply_col, hue=sentiment_col, s=200)
    plt.title('Promedio de Likes vs. Reply Count por Clase de Sentimiento')
    plt.xlabel('Promedio de Likes')
    plt.ylabel('Promedio de Reply Count')
    plt.legend(title='Sentimiento')
    plt.show()

def plot_bivariate_rate(df, col_x, target='bert_sentiment', group_col=None, order=None):
    count_df = df.groupby([col_x, target], observed=True).size().reset_index(name='count')
    total_df = df.groupby(col_x, observed=True).size().reset_index(name='total')
    merged = count_df.merge(total_df, on=col_x)
    merged['rate'] = merged['count'] / merged['total']
    
    plt.figure(figsize=(13, 7))
    ax = sns.pointplot(x=col_x, y='rate', hue=target, data=merged, dodge=True, markers='o', linestyles='-')
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    
    plt.title(f"Tasa proporcional de {target} por {col_x}")
    plt.xlabel(f"{col_x}")
    plt.ylabel("Tasa proporcional")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

def plot_wordcloud_for_class(df, text_col, class_col, class_value, max_words=100):
    """
    Genera un WordCloud para una clase específica.
    
    Parámetros:
    - text_col: columna de texto limpio.
    - class_col: columna de clase (categoría).
    - class_value: valor de la clase a filtrar.
    - max_words: máximo de palabras a mostrar.
    """
    text_data = df[df[class_col] == class_value][text_col].dropna().astype(str)
    full_text = ' '.join(text_data)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          max_words=max_words, collocations=False).generate(full_text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'WordCloud para clase: {class_value}')
    plt.show()

