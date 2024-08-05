# import json
# from source.data_models import Word, Category, CategoryWord
#
#
# def load_data_from_json(file_path) -> list | None:
#     models = {'Word': Word, 'Category': Category, 'CategoryWord': CategoryWord}
#     data_models = []
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#             for line in data:
#                 current_model = line.get("model")
#                 model_data_dict = line.get("fields")
#                 data_models.append(models.get(current_model)(**model_data_dict))
#     except FileNotFoundError:
#         print('File not found')
#         return
#     return data_models
