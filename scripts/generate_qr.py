#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信收款码生成示例脚本

这是一个示例脚本，展示如何为打赏功能准备收款码图片。
注意：实际使用时，您需要使用微信官方生成的收款码。
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_sample_qr_code(text="微信收款码示例", save_path="sample_wechat_qr.png"):
    """
    创建示例二维码图片
    
    Args:
        text: 二维码内容
        save_path: 保存路径
    """
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(text)
    qr.make(fit=True)
    
    # 生成二维码图片
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # 创建最终图片 (300x300)
    final_img = Image.new('RGB', (300, 300), 'white')
    
    # 调整二维码大小并居中
    qr_img = qr_img.resize((200, 200))
    final_img.paste(qr_img, (50, 30))
    
    # 添加文字说明
    draw = ImageDraw.Draw(final_img)
    
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        # 如果系统字体不可用，使用默认字体
        font = ImageFont.load_default()
    
    # 添加标题
    text_title = "微信收款码"
    bbox = draw.textbbox((0, 0), text_title, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(((300 - text_width) // 2, 240), text_title, fill="black", font=font)
    
    # 添加说明
    text_desc = "示例二维码，请替换为真实收款码"
    try:
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        small_font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text_desc, font=small_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((300 - text_width) // 2, 265), text_desc, fill="gray", font=small_font)
    
    # 保存图片
    final_img.save(save_path, "PNG", quality=95)
    print(f"示例二维码已保存到: {save_path}")
    
    return final_img

def image_to_base64(image_path):
    """
    将图片转换为 Base64 编码字符串
    
    Args:
        image_path: 图片路径
        
    Returns:
        Base64 编码的字符串
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

def generate_html_preview(base64_string, output_path="qr_preview.html"):
    """
    生成包含二维码的 HTML 预览文件
    
    Args:
        base64_string: Base64 编码的图片
        output_path: HTML 输出路径
    """
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信收款码预览</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
        }}
        .qr-code {{
            width: 200px;
            height: 200px;
            border: 3px solid #f0f0f0;
            border-radius: 10px;
            margin: 0 auto 15px;
        }}
        .title {{
            color: #333;
            margin-bottom: 20px;
            font-size: 24px;
        }}
        .description {{
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        .wechat-text {{
            color: #09bb07;
            font-weight: 600;
            font-size: 18px;
            margin-top: 15px;
        }}
        .copy-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            font-size: 14px;
        }}
        .copy-btn:hover {{
            transform: translateY(-2px);
            transition: transform 0.3s ease;
        }}
        .base64-input {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
            margin-top: 10px;
            word-break: break-all;
            height: 60px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2 class="title">💖 微信收款码预览</h2>
        <p class="description">
            这是生成的示例收款码。<br>
            实际使用时，请使用微信官方生成的真实收款码。
        </p>
        
        <img src="{base64_string}" alt="微信收款码" class="qr-code">
        <div class="wechat-text">微信扫一扫</div>
        
        <button class="copy-btn" onclick="copyBase64()">复制 Base64 代码</button>
        <textarea class="base64-input" id="base64Input" readonly>{base64_string}</textarea>
        
        <script>
            function copyBase64() {{
                const input = document.getElementById('base64Input');
                input.select();
                document.execCommand('copy');
                alert('Base64 代码已复制到剪贴板！');
            }}
        </script>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 预览文件已保存到: {output_path}")

def main():
    """主函数"""
    print("🔧 微信收款码生成工具")
    print("=" * 50)
    
    # 生成示例二维码
    print("1. 生成示例二维码...")
    qr_path = "sample_wechat_qr.png"
    create_sample_qr_code(save_path=qr_path)
    
    # 转换为 Base64
    print("2. 转换为 Base64 编码...")
    base64_string = image_to_base64(qr_path)
    print(f"   Base64 长度: {len(base64_string)} 字符")
    
    # 生成 HTML 预览
    print("3. 生成 HTML 预览...")
    generate_html_preview(base64_string)
    
    print("\n✅ 完成！")
    print("\n📋 使用说明:")
    print("1. 打开 qr_preview.html 查看效果")
    print("2. 复制 Base64 代码替换到管理页面")
    print("3. 或者直接在管理页面上传 sample_wechat_qr.png")
    print("\n⚠️  重要提醒:")
    print("- 这只是示例代码，实际使用请用真实的微信收款码")
    print("- 可以通过微信「收付款」->「二维码收款」获取真实收款码")
    print("- 建议收款码图片大小不超过 500KB")

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("❌ 缺少依赖库，请安装:")
        print("pip install qrcode pillow")
        print(f"\n错误详情: {e}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")