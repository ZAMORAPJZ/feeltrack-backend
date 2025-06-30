import emoji
import re
from langdetect import detect
from tqdm import tqdm
import torch
from transformers import BertTokenizer, BertModel
import numpy as np

def clean_basic_text_preserve_emojis(text):
    """
    Limpieza básica de texto preservando mayúsculas, emojis y símbolos emocionales.
    
    - Elimina URLs, menciones y hashtags.
    - Compacta espacios.
    """
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r'\s+([?.!,])', r'\1', text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_bert_embeddings(text_list, 
                            model_name='bert-base-multilingual-cased', 
                            batch_size=16, 
                            max_length=512):
    """
    Extrae embeddings BERT [CLS] para una lista de textos.
    
    Parámetros:
    - text_list: lista de textos (ya preprocesados).
    - model_name: nombre del modelo BERT (por defecto multilingüe cased).
    - batch_size: tamaño de batch para optimización.
    - max_length: longitud máxima de tokens (BERT trunca a 512).
    
    Retorna:
    - Array NumPy (n_samples, embedding_dim).
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    model.to(device)
    model.eval()
    
    all_embeddings = []
    with torch.no_grad():
        for i in range(0, len(text_list), batch_size):
            batch = text_list[i:i + batch_size]
            inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True, max_length=max_length)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            outputs = model(**inputs)
            cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            all_embeddings.append(cls_embeddings)
    
    return np.vstack(all_embeddings)