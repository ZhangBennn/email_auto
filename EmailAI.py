# import gradio as gr
# import requests
from zhipuai import ZhipuAI

# 假设这是你的GLM API的URL
GLM_API_URL = "http://your-glm-api-endpoint/generate"
API_KEY = "xxx"  # 如果有的话
email_template_path = "./templates/email_template_gpt.html"

with open(email_template_path, 'r', encoding='utf-8') as file:
    email_template_html_content = file.read()

EMAIL_PROMP = f"""
你是一名优秀的保险推销员，你需要撰写一封推销邮件，需要按要求生成邮件正文，邮件模板如下:
输出格式模版如下：
'```html{email_template_html_content}\n```'
正文要求:
1. 结合用户画像，生成定制化的保险介绍邮件。注意除了邮件内容本身外不要有任何其他句子。
2. 邮件内容可包含动态生成的保险亮点总结、客户案例分享等，以提高打开率和转化率。
3. 同时注意生成内容应该符合邮件格式。
4. 为了美观，格式需要是HTML格式，除了HTML邮件内容本身，不要出现其他字符。
5. 邮件正文内容应当尽量避免提及隐私信息，如收入。
6. 附加信息很重要
7. 不要无中生有，不要夸大其词，不要出现虚假信息, 优惠信息如未提供则不写。
8. 注意提供的产品信息，其中包含了保险的名字和公司的信息，请根据这些信息生成并替换模板中的信息。
9. 保险名称里面包含公司信息。
"""

def generate_email(API_KEY, sender_info, customer_info, product_info):
    """
    调用GLM API生成保险推销邮件。
    :param customer_info: 客户信息
    :param product_info: 产品信息
    :return: 生成的邮件内容
    """

    if product_info is not None:
        prompt = f"发件人信息为{str(sender_info)} 请为以下客户 {customer_info} 推销保险产品, 生成一封推销邮件。 附加信息为{str(product_info)}"
    else:
        prompt = f"发件人信息为{str(sender_info)} 请为以下客户 {customer_info} 推销保险产品, 生成一封推销邮件。"
    
    # response = requests.post(
    #     GLM_API_URL,
    #     json={"prompt": prompt},
    #     headers={"Authorization": f"Bearer {API_KEY}"}
    # )

    client = ZhipuAI(api_key=API_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": EMAIL_PROMP},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content

def generate_email_client(client, sender_info, customer_info, product_info, addtion_info=''):
    """
    调用GLM API生成保险推销邮件。
    :param customer_info: 客户信息
    :param product_info: 产品信息
    :return: 生成的邮件内容
    """
    # product_info += addtion_info

    if product_info is not None:
        prompt = f"发件人信息为{str(sender_info)} 请为以下客户 {customer_info} 推销保险产品，保险产品详情为{str(product_info)}, 生成一封推销邮件。 请注意保险名称， 附加信息为{str(addtion_info)}"
    else:
        prompt = f"发件人信息为{str(sender_info)} 请为以下客户 {customer_info} 推销保险产品, 生成一封推销邮件。 附加信息为{str(addtion_info)}"
    
    # print(prompt)
    # response = requests.post(
    #     GLM_API_URL,
    #     json={"prompt": prompt},
    #     headers={"Authorization": f"Bearer {API_KEY}"}
    # )

    # client = ZhipuAI(api_key=API_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": EMAIL_PROMP},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    # 创建Gradio界面
    with gr.Blocks() as demo:
        gr.Markdown("# 保险推销邮件生成器")
        with gr.Row():
            customer_input = gr.Textbox(label="请输入客户信息")
            product_input = gr.Textbox(label="请输入产品信息")
        output_text = gr.HTML(label="生成的邮件")
        submit_button = gr.Button("生成邮件")
        submit_button.click(fn=generate_email, inputs=[API_KEY, customer_input, product_input], outputs=output_text)
    # 启动服务
    demo.launch()
