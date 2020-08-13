# coding: utf-8
'''
@author: sy-records
@license: https://github.com/sy-records/v-checkin/blob/master/LICENSE
@contact: 52o@qq52o.cn
@desc: 腾讯视频好莱坞会员V力值签到，支持两次签到：一次正常签到，一次手机签到。
@blog: https://qq52o.me
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests

auth_refresh_url = 'https://access.video.qq.com/user/auth_refresh?vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe&type=qq&g_tk=&g_vstk=1182418585&g_actk=1223137314&callback=jQuery1910646484216808564_1597292730064&_=1597292730065'
sckey = 'SCU109232T44ac535b93f82be73e969bbc0c808cf25f34aef51bd93'

ftqq_url = "https://sc.ftqq.com/%s.send"%(sckey)
url1 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'
url2 = 'https://v.qq.com/x/bu/mobile_checkin'

login_headers = {
    'Referer': 'https://v.qq.com',
    'Cookie': 'pgv_pvi=8591048704; pgv_si=s4709841920; _qpsvr_localtk=0.2544835028399788; RK=teTpb83HaO; ptcz=5f1c02886be0876099b4c2740b30b7ae6f5231a1d225e35fbab4b727c800d3ef; tvfe_boss_uuid=5a7115e7ddd82c12; video_guid=e1312e1fbdcf33de; video_platform=2; pgv_pvid=9591014368; pgv_info=ssid=s6424935120; ptui_loginuin=918914492; main_login=qq; vqq_access_token=0F0AA7470FD45A68DDA6ED702D7B61F6; vqq_appid=101483052; vqq_openid=704571A2210013B25D5C185413B845BA; vqq_vuserid=530398448; vqq_vusession=6bH7CKJa7xXacdeSNANiTg..; vqq_refresh_token=63B124428E4D2F479A53B7D31BA9C918; vqq_next_refresh_time=6600; vqq_login_time_init=1597292729; login_time_init=2020-8-13 12:25:29'
}

login = requests.get(auth_refresh_url, headers=login_headers)
cookie = requests.utils.dict_from_cookiejar(login.cookies)

if not cookie:
    print "auth_refresh error"
    payload = {'text': '腾讯视频V力值签到通知', 'desp': '获取Cookie失败，Cookie失效'}
    requests.post(ftqq_url, params=payload)

sign_headers = {
    'Cookie': 'pgv_pvi=8591048704; pgv_si=s4709841920; _qpsvr_localtk=0.2544835028399788; RK=teTpb83HaO; ptcz=5f1c02886be0876099b4c2740b30b7ae6f5231a1d225e35fbab4b727c800d3ef; tvfe_boss_uuid=5a7115e7ddd82c12; video_guid=e1312e1fbdcf33de; video_platform=2; pgv_pvid=9591014368; pgv_info=ssid=s6424935120; ptui_loginuin=918914492; main_login=qq; vqq_access_token=0F0AA7470FD45A68DDA6ED702D7B61F6; vqq_appid=101483052; vqq_openid=704571A2210013B25D5C185413B845BA; vqq_vuserid=530398448; vqq_refresh_token=63B124428E4D2F479A53B7D31BA9C918; vqq_next_refresh_time=6600; vqq_login_time_init=1597292729; login_time_init=2020-8-13 12:25:29; vqq_vusession=' + cookie['vqq_vusession'] + ';',
    'Referer': 'https://m.v.qq.com'
}
def start():
  sign1 = requests.get(url1,headers=sign_headers).text
  if 'Account Verify Error' in sign1:
    print 'Sign1 error,Cookie Invalid'
    status = "链接1 失败，Cookie失效"
  else:
    print 'Sign1 Success'
    status = "链接1 成功，获得V力值：" + sign1[42:-14]

  sign2 = requests.get(url2,headers=sign_headers).text
  if 'Unauthorized' in sign2:
    print 'Sign2 error,Cookie Invalid'
    status = status + "\n\n 链接2 失败，Cookie失效"
  else:
    print 'Sign2 Success'
    status = status + "\n\n 链接2 成功"

  payload = {'text': '腾讯视频V力值签到通知', 'desp': status}
  requests.post(ftqq_url, params=payload)

def main_handler(event, context):
  return start()
if __name__ == '__main__':
  start()
