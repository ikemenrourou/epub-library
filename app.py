
import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from ebooklib import epub
from PIL import Image
from waitress import serve
import io
import webbrowser
import threading

app = Flask(__name__)

# 定义存放 EPUB 文件和封面的文件夹
BOOKS_FOLDER = "books/"  # 存放 EPUB 文件的目录
COVERS_FOLDER = "static/covers/"  # 存放封面的目录
DICTIONARY_FOLDER = "dictionaries/"  # 存放字典的目录

# 确保封面和字典目录存在
os.makedirs(COVERS_FOLDER, exist_ok=True)
os.makedirs(DICTIONARY_FOLDER, exist_ok=True)


# 函数：提取 EPUB 书籍的书名和封面
def get_epub_metadata(epub_file_path):
    try:
        # 打开 EPUB 文件
        book = epub.read_epub(epub_file_path)

        # 获取书名
        title = (
            book.get_metadata("DC", "title")[0][0]
            if book.get_metadata("DC", "title")
            else "Unknown Title"
        )

        # 初始化封面图片变量
        cover_image = None
        image_000 = None
        image_001 = None
        image_image = None
        largest_image = None
        largest_size = 0
        image_1 = None

        # 遍历所有资源
        for item in book.get_items():
            # 检查资源是否是图片（通过 MIME 类型过滤）
            if item.media_type in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
                image_content = item.get_content()
                image = Image.open(io.BytesIO(image_content))

                file_name = item.get_name().lower()

                # 1. 假设文件名包含 'cover' 的图片是封面
                if "cover" in file_name:
                    cover_image = image
                    break  # 优先使用带有 "cover" 的图片作为封面
                # 2. 假设文件名包含 '000' 的图片
                elif "000" in file_name:
                    image_000 = image
                # 3. 假设文件名包含 '001' 的图片
                elif "001" in file_name:
                    image_001 = image
                # 4. 假设文件名包含 'image' 的图片
                elif "image" in file_name:
                    image_image = image
                # 5. 假设文件名包含 '1' 的图片
                elif "1" in file_name:
                    image_image = image
                else:
                    # 选择最大的一张图片作为备选封面
                    image_size = image.size[0] * image.size[1]
                    if image_size > largest_size:
                        largest_size = image_size
                        largest_image = image

        # 优先级顺序：cover > 000 > 001 > image
        if not cover_image:
            if image_000:
                cover_image = image_000
            elif image_001:
                cover_image = image_001
            elif image_image:
                cover_image = image_image
            elif image_1:
                cover_image = image_1

        # 如果 "cover"、"000"、"001" 和 "image" 都没有找到，使用最大的一张图片
        if not cover_image:
            cover_image = largest_image

        return title, cover_image

    except Exception as e:
        print(f"Error reading {epub_file_path}: {e}")
        return None, None


# 函数：获取所有 EPUB 文件的书名和封面
def get_all_books():
    books = []
    for file_name in os.listdir(BOOKS_FOLDER):
        if file_name.endswith(".epub"):
            file_path = os.path.join(BOOKS_FOLDER, file_name)

            # 检查封面文件是否已经存在
            cover_image_path = os.path.join(COVERS_FOLDER, f"{file_name}.png")
            if not os.path.exists(cover_image_path):
                # 如果封面文件不存在，提取封面
                title, cover_image = get_epub_metadata(file_path)
                if title and cover_image:
                    # 保存封面为 PNG 格式
                    cover_image.save(cover_image_path)
                else:
                    # 如果未找到封面或书名，跳过该书籍
                    continue
            else:
                # 如果封面文件存在，从文件名推测书名（可以根据需求调整）
                title = file_name.replace(".epub", "")

            # 添加书籍信息到列表
            books.append(
                {
                    "title": title,
                    "cover_image": cover_image_path,
                    "file_path": file_name,  # 仅保存文件名，供阅读页面使用
                }
            )
    return books

@app.route('/covers/<path:filename>')
def serve_covers(filename):
    return send_from_directory('covers', filename)

# 首页路由：展示所有书籍
@app.route("/")
def index():
    books = get_all_books()
    return render_template("index.html", books=books)


# 阅读页面路由
@app.route("/read/<path:book_name>")
def read_book(book_name):
    return render_template("read.html", filename=book_name)


# 提供书籍文件
@app.route("/books/<path:filename>")
def serve_book(filename):
    return send_from_directory(BOOKS_FOLDER, filename)


# 获取或创建书籍字典
@app.route("/dictionary/<book_name>", methods=["GET", "POST"])
def manage_dictionary(book_name):
    dict_path = os.path.join(DICTIONARY_FOLDER, f"{book_name}.json")

    if request.method == "POST":
        # 保存字典条目
        data = request.get_json()
        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify({"status": "success"})
    else:
        # 获取字典条目
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                dictionary = json.load(f)
        else:
            dictionary = []
        return jsonify(dictionary)


def open_browser():
    # 等待服务启动，防止浏览器打开过早
    webbrowser.open("http://localhost:5001")

if __name__ == "__main__":
    # 使用线程在后台启动浏览器，避免阻塞主进程
    threading.Timer(1, open_browser).start()
    # 启动 WSGI 服务
    serve(app, host="0.0.0.0", port=5001, threads=8) 