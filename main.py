import gradio as gr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailAI import generate_email
import pandas as pd
import re

# 定义全局变量来存储邮箱账号和密码
global_sender_email = None
global_sender_password = None
global_sender_zhipuapikey = None
global_sender_name = None
global_sender_phone = None
global_sender_company = None

# 状态变量，用于控制显示哪个界面
show_credentials_page = True
global_customer_data_path = "./customer_data/customer_details_excel.csv"
# 自定义 CSS
custom_css = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

.gradio-container {
    max-width: 600px;
    margin: 50px auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 30px;
}

.gradio-container h1 {
    text-align: center;
    color: #333;
}

.gradio-container .gr-input, .gradio-container .gr-button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.gradio-container .gr-button {
    background-color: #007bff;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
}

.gradio-container .gr-button:hover {
    background-color: #0056b3;
}
</style>
"""

def send_email(sender_email, sender_password, recipient, subject, body):
    # 创建消息对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'html'))

    try:
        # 连接到 SMTP 服务器
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()

        # 登录到你的邮箱
        server.login(sender_email, sender_password)

        # 发送邮件
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def set_credentials(email_input, password_input, apikey_input, name_input, phone_input, company_input):
    global global_sender_email, global_sender_password, global_sender_zhipuapikey, show_credentials_page
    global global_sender_name, global_sender_phone, global_sender_company
    global_sender_email = email_input
    global_sender_password = password_input
    global_sender_zhipuapikey = apikey_input
    global_sender_name = name_input
    global_sender_phone = phone_input
    global_sender_company = company_input

    show_credentials_page = False
    return "Credentials set. You can now send an email."

def send_email_interface(product_input):
    if global_sender_email and global_sender_password and global_sender_zhipuapikey:        
        sender_info = {
            "name": global_sender_name,
            "phone": global_sender_phone,
            "company": global_sender_company,
        }
        # 读取 Excel 文件
        customer_data_df = pd.read_csv(global_customer_data_path,encoding='gbk')
        for row in customer_data_df.itertuples(index=True, name='Pandas'):
            # 在这里对每一行进行处理
            # 创建一个字符串，包含所有列的信息
            customer_data_str = (
                f"姓名: {row.姓名}, "
                f"性别: {row.性别}, "
                f"年龄: {row.年龄}, "
                f"职业: {row.职业}, "
                f"婚姻状况: {row.婚姻状况}, "
                f"子女情况: {row.子女情况}, "
                f"保险需求: {row.保险需求}, "
                f"经济状况: {row.经济状况}, "
                f"兴趣爱好: {row.兴趣爱好}, "
                f"其他备注: {row.其他备注}")

            recipient = row.邮箱

            body = generate_email(global_sender_zhipuapikey, sender_info, customer_data_str, product_input)[8:-3]
            subject = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE | re.DOTALL).group(1)
            result = send_email(global_sender_email, global_sender_password, recipient, subject, body)
        return result
    else:
        return "Please set your credentials first."

def update_interface():
    return [
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=show_credentials_page),
        gr.update(visible=not show_credentials_page),
        gr.update(visible=not show_credentials_page),
        gr.update(visible=not show_credentials_page)
    ]

# 创建 Gradio Blocks
with gr.Blocks(css=custom_css) as demo:
    with gr.Row():
        email_input = gr.Textbox(lines=1, placeholder="Sender Email", label="Sender Email", visible=True)
        password_input = gr.Textbox(lines=1, placeholder="Sender Password", label="Sender Password", type="password", visible=True)
        apikey_input = gr.Textbox(lines=1, placeholder="Sender ApiKey", label="Sender ApiKey", type="password", visible=True)
        name_input = gr.Textbox(lines=1, placeholder="Sender Name", label="Sender Name", value="李华", visible=True)
        phone_input = gr.Textbox(lines=1, placeholder="Sender Phone", label="Sender Phone", value="12345678923", visible=True)
        company_input = gr.Textbox(lines=1, placeholder="Sender Company", label="Sender Company", value="中国平平安", visible=True)
    set_credentials_button = gr.Button("Set Credentials", visible=True)
    set_credentials_output = gr.Textbox(label="Result", visible=True)

    product_input = gr.Textbox(label="Please Enter Product Information", visible=False)
    output_text = gr.HTML(label="Send Email", visible=False)
    
    send_email_button = gr.Button("Send Email", visible=False)
    send_email_output = gr.Textbox(label="Result", visible=False)

    set_credentials_button.click(
        fn=set_credentials,
        inputs=[email_input, password_input, apikey_input, name_input, phone_input, company_input],
        outputs=set_credentials_output
    ).then(
        fn=update_interface,
        outputs=[
            email_input, password_input, apikey_input, name_input, phone_input, company_input, set_credentials_button, set_credentials_output,
            product_input, send_email_button, send_email_output
        ]
    )

    # 使用 JavaScript 实现平滑滚动
    demo.load(None, [], None, js="""
    function() {
        const scrollToElement = (elementId) => {
            const element = document.querySelector(`[data-testid="${elementId}"]`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        };

        setTimeout(() => {
            if (!document.querySelector('[data-testid="block-0"]').style.display) {
                scrollToElement('block-4');
            }
        }, 500);

        return [];
    }
    """)

    send_email_button.click(
        fn=send_email_interface,
        inputs=[product_input],
        outputs=send_email_output
    )
#test
# 启动 Gradio 应用
if __name__ == "__main__":
    demo.launch()