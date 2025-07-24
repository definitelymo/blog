import requests
import re
import json

# 视频URL
url = 'https://www.bilibili.com/video/BV1ez3UzgEKD'

# 伪装浏览器头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}

# 获取网页内容
response = requests.get(url, headers=headers)
html = response.text

# 提取嵌入的初始 JSON 数据（window.__INITIAL_STATE__）
initial_state_pattern = re.search(r'window\.__INITIAL_STATE__=({.*?});', html)

if initial_state_pattern:
    json_data = json.loads(initial_state_pattern.group(1))

    # 提取信息（结构复杂，我们只挑几个）
    video_data = json_data.get('videoData', {})
    stat = json_data.get('videoData', {}).get('stat', {})

    print("标题：", video_data.get('title'))
    print("UP主：", video_data.get('owner', {}).get('name'))
    print("播放量：", stat.get('view'))
    print("点赞数：", stat.get('like'))
    print("弹幕数：", stat.get('danmaku'))

else:
    print("❌ 无法提取视频信息，页面结构可能已更新。")
