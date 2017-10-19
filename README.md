# 糗事百科全站爬虫

之前看到有人写糗事百科的爬虫，就爬了几个页面，感觉太少，一个专业的段子手怎么能忍；
本文中使用多进程加多线程，段子用户id保存至redis数据库，用户数据及段子内容存储至mongodb；
本人自己的代理池前段时间没了，这里用的是阿布云代理（阿布云账号一小时一块钱），说的是每秒支持并行5个代理，其实没有这么多，买了三个账号连续爬一天，总共爬到30多万个用户数据，段子200多万个

程序大概的结构是：

1. 用户id：程序开始打开糗事百科历史网页，从中爬取用户id放入redis，正常爬取的时候保存本用户关注人放入redis，同时也会按照一定概率打开糗事百科历史网页，保存用户id；
2. 用户内容：从redis数据库0中取出一个用户id爬取内容，爬取成功则将用户id保存至redis数据库1中；
爬取时会首先读取当前用户总共段子的页面数，之后依次爬取
3. 保存的内容包括网页上可以看到的所有用户信息及相关段子
4. 程序中有单进程与多进程的选择，如果只买一个账号的话，还是用单进程吧，如果自己有代理池，那就可以随意玩了
 
