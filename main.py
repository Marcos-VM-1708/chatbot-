from create_fine_tune import train_gpt

# ------------------------------------------------

path : str = "categorias\data_raw.txt"

if __name__ == "__main__":
    model = train_gpt(path_data = path, model_name = "gpt-3.5-turbo",load = False, api_key = "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")
    model.split_data()
    model.transformer_data()
    # model.resize()
    model.validate_data()
    model.training(file_id = None, N_epocas = 7)