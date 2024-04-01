import gradio as gr
from transformers import AutoModelForImageSegmentation, AutoFeatureExtractor
from PIL import Image
import requests
from io import BytesIO

# 定义模型名称
model_name = "trysem/DualStyleGANplus"
# 加载模型和特征提取器
model = AutoModelForImageSegmentation.from_pretrained(model_name)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)

# 定义图片风格转换函数
def style_transfer(image):
    # 转换输入图像
    inputs = feature_extractor(images=image, return_tensors="pt")
    # 进行风格转换
    outputs = model(**inputs)
    # 处理输出
    processed_image = outputs.logits[0].argmax(0).detach().numpy()
    # 将处理后的图像转换为 PIL Image
    return Image.fromarray(processed_image)

# 设置 Gradio 界面
iface = gr.Interface(
    fn=style_transfer,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="Image Style Transfer",
    description="Upload an image to apply the Candy style transfer."
)

# 启动应用
iface.launch(share=True)

