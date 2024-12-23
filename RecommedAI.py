from zhipuai import ZhipuAI
from pathlib import Path
import logging
import json

import os
import json
import glob
import random
Recommendd_PROMPT = f"""
你是一名优秀的保险推销， 你需要根据用户信息，推荐合适的保险产品，返回推荐的保险产品列表，格式为：
["产品1","产品2"], 推销一个产品或者两个，最多不要超过两个
"""
def read_json_files_from_path(path):
    json_data_dict = {}

    # 使用glob模块查找所有以.json结尾的文件
    json_files = glob.glob(os.path.join(path, '*.json'))

    count = 0
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                file_name = os.path.basename(file_path)
                # print(data)
                json_data_dict[file_name.replace('.json','')] = str(count) + "[" + str(data) + "]"
                count += 1
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return json_data_dict

def get_random_insurance_products(json_lists, num_samples):
    """
    从保险产品列表中随机抽取指定数量的产品。

    :param json_lists: 包含所有保险产品的列表
    :param num_samples: 需要抽取的产品数量
    :return: 抽取的保险产品列表
    """
     # 获取所有产品列表（字典的值）
    product_list = list(json_lists.values())

    # 确保请求的数量不超过列表长度
    num_samples = min(num_samples, len(product_list))

    # 使用random.sample()随机抽取指定数量的产品
    sampled_products = random.sample(product_list, num_samples)

    # 如果需要返回的是文件名，则可以这样处理：
    sampled_product_names = [key for key, value in json_lists.items() if value in sampled_products]

    return sampled_product_names
    
def recommend_insurance_products(client, person_info, path):
    result = []
    try:
    # 填写您自己的APIKey
    # client = ZhipuAI(api_key=api_key)
    # 读取path路径下的所有json文件形成列表
    # print(path)
    # print(person_info)
        json_lists=read_json_files_from_path(path)
        # 生成请求消息
        message_content = f"""
        请根据个人信息\n{person_info}\n和保险产品摘要字典\n{json_lists}\n，推荐适合的保险产品，要求：返回必须只是一个列表，只包含产品名称，例如：`["保险1", "保险2", ...]`
        """
        # print(message_content)
        response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": Recommendd_PROMPT},
                    {"role": "user", "content": message_content}])
        result = response.choices[0].message.content
        # print(response.choices[0].message.content)
        # result=response.choices[0].message.content.replace('```json','')
        print(result)
        if len(result) == 0:
            result = get_random_insurance_products(json_lists, 1)
    except Exception as e:
        logging.error(f'error in recommend_insurance_products: {e}')
    return result