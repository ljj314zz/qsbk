# coding:utf-8
#from random import choice
# 从代理ip网站上总共要爬取的ip页数。一般每页20条，小项目(20-30个代理ip即可完成的)可以设置为1-2页。
page_num = 10

# 对已经检测成功的ip测试轮次。
examine_round = 3

# 超时时间。
timeout = 3

# 数据库链接地址
host = '127.0.0.1'

# 数据库链接端口
port = 3306

# 数据库链接用户名
user = 'root'

# 数据库密码
passwd = '******'

# 数据库名
DB_NAME = 'proxies'

# 表名
TABLE_NAME = 'valid_ip'

# 数据库字符
charset = 'utf8'

# 1个代理ip最大容忍失败次数，超过则从db中删去。
USELESS_TIME = 4

# 1个代理ip最小容忍成功率
SUCCESS_RATE = 0.8

# 超时惩罚时间
TIME_OUT_PENALTY = 10

# 每隔多久检测一次
CHECK_TIME_INTERVAL = 24 * 3600

# 代理网址

# 进程数
process = 64
# 检查代理进程数
process_proxy = 8
# 检测代理网址
# url_text='https://www.baidu.com/'
url_text = 'https://www.qiushibaike.com/'

# 每次取多少条代理访问网页
get_ip_count = 80


UserAgents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12",
    "Opera/9.27 (Windows NT 5.2; U; zh-cn)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13",
    #"Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 ",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 ",
    "Mozilla/5.0 (Linux; U; Android 3.2; ja-jp; F-01D Build/F0001) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13 ",
    #"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; ja-jp) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7",
    #"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5 ",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9 ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
]
def headers():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
               'Host': 'www.qiushibaike.com',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               #'Cookie':'_xsrf=2|f96af927|87fbdb1a3659abc51883ca9fac193a18|1507259117; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_Source=www.google.com.hk/; callback_url=/new4/session%3Fsrc%3Dwx%26code%3D013qg51j2yqn1F0mLVZi2aEf1j2qg51l%26state%3D; ADEZ_ST=1026889-1-j8h4r25b; __cur_art_index=1505; ADEZ_ASD=1; ADEZ_PVC=1026761-29-j8g8j9o6|1026889-1-j8g6g9pp; __utmt=1; __utmt_account2=1; _ga=GA1.2.1379297726.1507259121; _gid=GA1.2.1052313806.1507259121; __utma=210674965.1379297726.1507259121.1507292983.1507297351.9; __utmb=210674965.6.10.1507297351; __utmc=210674965; __utmz=210674965.1507262591.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1507259120,1507262589,1507264423,1507278055; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1507298546',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return headers
# '''
#
#
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.8
# Cookie: _xsrf=2|f96af927|87fbdb1a3659abc51883ca9fac193a18|1507259117; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_Source=www.google.com.hk/; callback_url=/new4/session%3Fsrc%3Dwx%26code%3D013qg51j2yqn1F0mLVZi2aEf1j2qg51l%26state%3D; ADEZ_ST=1026889-1-j8h4r25b; __cur_art_index=1505; ADEZ_ASD=1; ADEZ_PVC=1026761-29-j8g8j9o6|1026889-1-j8g6g9pp; __utmt=1; __utmt_account2=1; _ga=GA1.2.1379297726.1507259121; _gid=GA1.2.1052313806.1507259121; __utma=210674965.1379297726.1507259121.1507292983.1507297351.9; __utmb=210674965.6.10.1507297351; __utmc=210674965; __utmz=210674965.1507262591.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1507259120,1507262589,1507264423,1507278055; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1507298546
# If-None-Match: "19cc560217ebffd6ed0a513de08419aa11c61766"
# '''

proxies = [
    "211.147.240.86:808",
    "210.26.54.43:808",
    "202.202.90.20:8080",
    "119.29.103.13:8888",
    "61.135.217.7:80",
    "111.13.2.131:80",
    "111.13.109.27:80",
    "114.215.150.13:3128",
    "111.62.251.130:8080"
]
