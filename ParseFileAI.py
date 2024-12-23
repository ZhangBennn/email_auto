from zhipuai import ZhipuAI
from pathlib import Path
import logging
import json

def get_summary_of_pdf(file_path, api_key):
    """目前解析有点问题，部分pdf会解析失败"""
    ans = {}
    try:
        # 填写您自己的APIKey
        client = ZhipuAI(api_key=api_key)
        # 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
        # 大小：单个文件50M、总数限制为100个文件
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")

        # 获取文本内容
        file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]

        # 生成请求消息
        message_content = f"请对\n{file_content}\n的内容进行分析，并撰写一份中文json摘要。"

        response = client.chat.completions.create(
            model="glm-4-long",  
            messages=[
                {"role": "user", "content": message_content}
            ],
        )

        # 解析响应结果
        ans = eval(str(response.choices[0].message).split('```')[1].replace('json\\n','').replace('\\n',''))
    except Exception as e:
        logging.error(f'Error in getting summary of pdf: {e}')
    
    return ans

# def get_summary_of_pdf_client(client, file_path):
#     """目前解析有点问题，部分pdf会解析失败"""
#     ans = {}
#     # print(file_path)
#     try:
#         # 填写您自己的APIKey
#         # client = ZhipuAI(api_key=api_key)
#         # 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
#         # 大小：单个文件50M、总数限制为100个文件
#         file_object = client.files.create(file=Path(file_path), purpose="file-extract")

#         # 获取文本内容
#         file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]

#         # 生成请求消息
#         message_content = f"请对\n{file_content}\n的内容进行分析，并撰写一份中文json摘要，摘要主要包括保险名称，保险范围，产品优势等。"

#         response = client.chat.completions.create(
#             model="glm-4-flash",  
#             messages=[
#                 {"role": "user", "content": message_content}
#             ],
#         )
#         # print(response.choices[0].message)
#     except Exception as e:
#         logging.error(f'Error in getting summary of pdf: {e}')
    
#     return response

def get_summary_of_pdf_client(client, file_path):
    """目前解析有点问题，部分pdf会解析失败"""
    ans = {}
    try:
        # 填写您自己的APIKey
        # client = ZhipuAI(api_key=api_key)
        # 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
        # # 大小：单个文件50M、总数限制为100个文件
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")

        # 获取文本内容
        file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]
        
        template_json = {'保险名称': '国寿美好生活团体医疗保险（惠民版）',
                        '保险范围': '当地城镇职工基本医疗保险、城乡居民基本医疗保险及公费医疗保险的参保人',
                        '保险责任': {'基本责任': '住院医疗保险责任',
                        '可选责任': ['门诊医疗保险责任',
                        '特定药品保险责任',
                        '特定住院医疗保险责任',
                        '特殊疾病门诊医疗保险责任',
                        '慢性疾病门诊医疗保险责任']},
                        '产品优势': {'保险责任灵活': '投保人可以分别设置各项保险责任的保险金额、免赔额，也可在基本医疗保险支付范围内共享保险金额、免赔额',
                        '续保优惠': '投保人按照本公司相关规定续保的，续保不受等待期的限制，且续保非保证续保',
                        '责任免除明确': '合同中详细列明了不承担保险责任的情况，保障消费者的知情权'}}

        # 生成请求消息
        message_content = f"请对\n{file_content}\n的内容进行分析，并参考模板{str(template_json)}撰写一份中文json摘要，摘要主要包括保险名称，保险范围，产品优势等。"
        response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": message_content}],)
        # ans = eval(str(response.choices[0].message).split('```')[1].replace('json\\n','').replace('\\n',''))
    except:
        logging.error('error in getting summary of pdf')
    return response

