import gradio as gr
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image

# 加载模型和特征提取器
model_name = "google/vit-base-patch16-224-in21k"
model = ViTForImageClassification.from_pretrained(model_name)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)

# 打印每个标签的含义
print(model.config.id2label)

def classify_image(image):
    # 转换图片数据
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    # 获取最高概率的类别
    predicted_class_idx = logits.argmax(-1).item()
    confidence = logits.softmax(dim=-1).max(-1).values.item()
    # 获取模型配置中的标签
    labels = model.config.id2label
    # 返回类别和置信度
    return {labels[predicted_class_idx]: float(confidence)}

# 创建 Gradio 界面
iface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(),
    outputs=gr.Label(num_top_classes=3),
    title="Image Classification"
)

iface.launch(share=True)

