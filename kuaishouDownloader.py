import os
import re
import requests
from tqdm import tqdm  # 导入 tqdm


def download_vide_with_keyword(keyword):
    cookies = {
        'did': 'web_ba21e19bb4c9dc720d058b9fdc7205fd',
        'didv': '1728652788655',
        '_bl_uid': 'p0m5t2pe4vhrsX8sal309C2iIqgy',
        'kpf': 'PC_WEB',
        'clientid': '3',
        'kpn': 'KUAISHOU_VISION',
    }

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'did=web_ba21e19bb4c9dc720d058b9fdc7205fd; didv=1728652788655; _bl_uid=p0m5t2pe4vhrsX8sal309C2iIqgy; kpf=PC_WEB; clientid=3; kpn=KUAISHOU_VISION',
        'Origin': 'https://www.kuaishou.com',
        'Referer': 'https://www.kuaishou.com/short-video/3xm8jkrgmf4zcx9?authorId=3x3rncaacmuhn3c&streamSource=search&area=searchxxnull&searchKey=tiaowu',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'accept': '*/*',
        'content-type': 'application/json',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'operationName': 'visionSearchPhoto',
        'variables': {
            'keyword': keyword,
            'pcursor': '',
            'page': 'detail',
            'webPageArea': 'searchxxnull',
        },
        'query': 'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://www.kuaishou.com/graphql', cookies=cookies, headers=headers, json=json_data)

    json = response.json()
    video_list = json["data"]["visionSearchPhoto"]["feeds"]
    # [0]["photo"]["photoUrl"]
    os.makedirs('kuaishouVideo', exist_ok=True)
    keyword_path = os.path.join('kuaishouVideo', keyword)
    os.makedirs(keyword_path, exist_ok=True)

    if len(video_list) > input_limit_index:
        video_list = video_list[:input_limit_index]

    for video in video_list:
        title = video["photo"]["caption"]
        print(title)
        # 将非法字符替换为 '_'
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        sanitized_title = sanitized_title[:50]
        video_path = os.path.join(keyword_path, sanitized_title + ".mp4")
        url = video["photo"]["photoUrl"]

        # 请求url并保存video.mp4
        content = requests.get(url).content

        # 发送请求获取视频文件内容
        response = requests.get(url, stream=True)  # 使用stream=True来逐块下载

        # 获取文件总大小
        total_size = int(response.headers.get('Content-Length', 0))
        # 设置进度条
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {sanitized_title}.mp4") as pbar:
            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):  # 按1024字节分块下载
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))  # 更新进度条，len(chunk)是当前块的大小
        print(f"Downloaded: {video_path}")


if __name__ == '__main__':

    while True:
        input_keyword = input('请输入下载关键词:')
        # 获取用户输入的下载数量
        input_limit_index = input('请输入下载数量（回车默认10个）: ')

        # 如果用户没有输入，则默认为10个
        if not input_limit_index:
            input_limit_index = 10
        else:
            # 如果用户输入了内容，尝试将其转换为整数
            try:
                input_limit_index = int(input_limit_index)
            except ValueError:
                print("输入无效，默认下载10个视频。")
                input_limit_index = 10

        print(f"将下载 {input_limit_index} 个视频。")

        download_vide_with_keyword(input_keyword)