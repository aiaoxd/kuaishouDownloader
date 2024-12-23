# 快手视频下载器

这个 Python 脚本允许你根据关键词从快手（Kuaishou）搜索并下载视频。它通过获取视频并进行下载，同时提供下载进度条显示。脚本还会处理视频标题中的非法字符，并将视频保存在有序的文件夹结构中。

## 功能

关键词搜索视频：根据给定的关键词搜索并下载快手上的视频。
自定义下载数量：你可以指定下载的视频数量。如果没有输入，默认为下载 10 个视频。
下载进度条：使用 tqdm 库显示下载进度条。
文件名规范化：视频文件名会去除非法字符，确保在文件系统中安全保存。
文件夹结构：下载的视频会按照关键词存储在相应的文件夹中。
前置条件

## 在使用此脚本之前，请确保你已安装以下内容：

Python 3.x 版本。
安装 requests 和 tqdm 库，可以使用以下命令安装：
```bash
pip install requests tqdm
```
使用方法

1. 克隆仓库或下载脚本
你可以通过克隆仓库或者复制代码到一个 Python 文件中（例如 kuaishouDownloader.py）来下载此脚本。

2. 运行脚本
安装好依赖后，运行脚本：
```bash
python kuaishouDownloader.py
```
3. 输入关键词和下载数量

关键词：输入你想搜索的视频关键词（例如 "舞蹈"、"搞笑视频" 等）。

脚本会根据关键词在快手上搜索视频。

下载数量：你将被提示输入想要下载的视频数量。

如果直接按 回车，则默认为下载 10 个视频。

4. 视频下载
脚本将开始下载视频，并为每个视频显示下载进度条。下载的视频将保存在一个以关键词命名的文件夹中。

示例

请输入下载关键词: 舞蹈
请输入下载数量（回车默认10个）: 5
将下载 5 个视频。
```bash
Downloading Video_1.mp4: 100%|██████████| 5.0MB/5.0MB [00:02<00:00, 2.50MB/s]
Downloaded: kuaishouVideo/dance/Video_1.mp4
Downloading Video_2.mp4: 100%|██████████| 6.5MB/6.5MB [00:03<00:00, 2.17MB/s]
Downloaded: kuaishouVideo/dance/Video_2.mp4
...

```
