import requests
import re
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.douyin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'douyin.com; ttwid=1%7CIDopHIq0HOsVuyO76-gDkdGq5GUtaIh3Mh3mz6mU2vA%7C1702016103%7Cd093b140bc954523e4302ab5e9cdd14a24e9717edffbf6f22eec688b6200c75a; douyin.com; device_web_cpu_core=24; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; dy_swidth=1920; dy_sheight=1080; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A24%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; passport_csrf_token=affdc78e91ae5f8984731e972169fd7b; passport_csrf_token_default=affdc78e91ae5f8984731e972169fd7b; csrf_session_id=3d630f002b178cb8d6bf6b9a33f1937d; strategyABtestKey=%221702016102.473%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; s_v_web_id=verify_lpw8fxrd_VALeImtM_UvxQ_4lK0_BdAc_dsj3vb6lDVrF; bd_ticket_guard_client_web_domain=2; ttcid=65350e6002484ef2b7fcbfbd17a9fddb35; download_guide=%223%2F20231208%2F0%22; __ac_nonce=06572dbab002546f2b547; __ac_signature=_02B4Z6wo00f01CvitJgAAIDAq-BO2LvcQEQrwrAAAG-R7x0bPYhi.qzw23zymMhH6pV2bUZVCSxGhp-CNAs7HgUPCg6k29pIYrimS9bBpLD14QoUnNYZx3cJrOwEGVsJ3YhXcboDoljDb5D-bf; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; SEARCH_RESULT_LIST_TYPE=%22single%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCT0NxelYrc2tXOUpBdDc4NVBjYnNCNjIyQmhLd3g1cUIxdnU3cXpQTXppM3JJV1lsZWY5Ni9CemlYUSt0ZXZSc0RMSnhWZ0p1b0Q5MkVTNHVSdTZtN289IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=UnR2al63rAgO0DInrCTQjOYWxagDSLTbZZu2NQrxqBu_fnBUQYnJ5r3PrTBGOa5uSX6kiCVr_G5OlTTXfcvxjZPoq7mLBmJK4430IFO1Ujm46TRSQA==; tt_scid=GrhZxBcisdXjF0KcEBf7mtUs-obvWGyKuqQwUgUSxqHCrGF4kSsdcdcilVvlXF3L613e; msToken=CgyYAgqfxEO8KbOt7kX6yG5Jyna-QfrSjAOHWzWUyJYzKOe3ZsKcs2PoO6Z6Bw_henK8yYqnXEsAVi8UGee5X5a22JdZHnMnAKK3BN-4vLV822WlVg==; IsDouyinActive=false',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

response = requests.get('https://www.douyin.com/note/7117919249837985060', headers=headers).text
html = response.replace("\\u002F", "/").replace("\n", "").replace(" ", "")
mp3 = re.search(r'src="(https\:\/\/sf3-cdn-tos.douyinstatic.com.*?)"', html).group(1) #音频
print(mp3)