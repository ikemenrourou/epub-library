# epub-light-novel-library
- **全是bug，不建议使用**
- 一个使用AI写的基于Flask、Python 和 epub.js 构建的本地 EPUB 轻小说阅读 Web 应用
- 截止2天前，楼主没有看过1秒钟编程视频，代码编辑器用的还是记事本，纯靠gpt老师
- （AI主要用的是 4O 和 copilot，claude3.5，极少数 o1）

## 截图

![首页截图](path_to_your_screenshot)

## 环境要求

- Python 3.x
- Flask
- epub.js
- PIL (Python Imaging Library)
- ebooklib
- 
## 便携版

你可以从 [Releases 页面](https://github.com/ikemenrourou/epub-light-novel-library/releases) 下载最新的发行版。
双击start.bat启动

## 源代码安装

1. 安装依赖：

   ```bash
   pip install -r requirements.txt

2. 运行应用程序：

   ```bash
   python app.py

## 使用说明

- 将 EPUB 文件放入项目的 books/ 文件夹中
- 查看书籍：打开应用程序的首页，自动显示上传的电子书封面和标题。
- 阅读电子书：点击书籍封面进入阅读页面，支持书签和目录功能。（左上角目录有bug 禁用了）
- 字典功能：阅读时可以添加自定义条目进行文字替换。（得更换章节才能顺利显示）
- 双击四周隐藏/显示UI （隐藏后可能无法使用字典功能）
