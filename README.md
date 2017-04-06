# garbage-truck
实验室考核作业二期报告（爬虫-数据库）
源码查看
https://github.com/wonjar/garbage-truck
功能描述
从http://www.juemei.com/mm/sfz 爬取图片。
爬虫爬取信息取包括：
图片文件、图片标题、图片所在网址、图片文件源地址；
图片文件首先爬取文件源地址，由爬虫框架内置下载器保存至本地。
入库信息包括：
自增id、图片标题、图片所在网页url、图片本地路径、图片文件（二进制存储）
设计思路
1.	items.py
标题、网页url、图片文件对象为任务要求项而创建，image_urls和image_paths为图片处理管道的依赖对象，前者被图片下载管道取出用于下载，后者存储下载成功的文件路径，也可辅助其他过程。
2.	dongying.py
爬虫的主体部分。首先分析网站页面，所需爬两种网页，以start_url为首的目录页和url格式略有不同的大图页。
目录页为瀑布流和分页，一开始我还担心瀑布流是用ajax异步加载的，结果一打开源码发现只是通过参数hiden，下滑加载只是个显示效果，好吧，被演了。定义parse()处理所有的目录页，将waterfall下不管隐藏没隐藏的其中所有指向大图页的herf提取出来，用urljoin合成完整链接用生成器加入处理大图页的parse_mm()的请求列表。提取下一页页码链接，传给自身请求列表。
Parse_mm()接受链接爬上大图页，并获取以下传给items：将当前页存入图片所在url一项；h1标题；图片src存入Image_urls，待图片下载管道使用。
3.	pipeline.py
处理爬虫得到的数据。在这里定义了三个类，作用如下：
MyImagesPipeline：图片下载，从image_urls取出下载链接，下载完毕后将本地相对路径保存到image_paths，文件数据在images里也有一份。
	Class A：连接数据库建立表mm的module，包括要入库的5个字段，考虑到文件大小其中image使用MEDIUMBLOB类型存储。
	DongyingPipeline：从item写入数据库，但图片文件是用本地文件二进制read进去的。
数据库配置
Root下建立spider为database，数据库所有编码统一设置为UTF-8。
调试报告
写代码过程中遇到过很多问题，不过还是一一解决了。
1.	为了让Css选择器正常确出结果，在scrapy shell里试表达式。
2.	为了确定joinurl默认参数的截取范围，查看文档中关于如何实现的部分，确定可直接使用。
3.	原本打算base64编码后存入LargeBinay类型，结果发现我调用的函数base60编码以后是字节流类型而不是字节类型，于是改用open(”…”,”rb”).read()不编码了直接读二进制，然后发现LargeBinary不够大，装不下高清大图（我爬这玩意不高清会让人想打人吧），查mysql支持的二进制里BLOB分大小号的，sqlalchemy里有对应的衔接。看了看最大一张图100kB+，用MEDIUMBLOB能装下，终于入库成功。
4.	编码问题。数据库的编码设置项实在是太多了。改了database是UTF-8，Sever是latin1没改过来就一直乱码，创建表单也需要加一个?charset=utf8不然默认latin1还是乱码，encode()完之后从str变成了byte还是乱码（一看python3不用encode()再decode()我就去掉了），全都改完以后不drop table重跑一遍还是乱码。总之编码问题上花费了很多时间。
运行效果
运行命令：进入项目文件夹后 scrapy crawl mm
因为代码里包含绝对路径下下来直接跑会不成功，涉及绝对路径的地方：
Pipeline.py：line 50
	image= open("/home/dongying/dongying/"+item["image_paths"][0], "rb").read())
后半截看不到的是full/…….jpg
Settings.py：line 17
IMAGES_STORE = '/home/dongying/dongying'
