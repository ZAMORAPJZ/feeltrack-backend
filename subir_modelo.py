from huggingface_hub import upload_folder

upload_folder(
    repo_id="ZAMORAPJ/feeltrack-model",  # tu repo en Hugging Face
    folder_path="./model",               # carpeta local
    commit_message="Subida inicial del modelo Feel-Track"
)