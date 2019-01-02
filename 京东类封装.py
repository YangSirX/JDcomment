import json
import requests
import time
import pymysql
import pymysql.cursors


class JdData(object):

    def __init__(self):
        # 商品评论js连接
        self.comment_url = 'https://sclub.jd.com/comment/productPageComments.action'
        # for n in range(10):
        #     self.params = {
        #         'productId': '100000287113',
        #         'score': 0,
        #         'sortType': 5,
        #         'page': n,
        #         'pageSize': 10,
        #     }
        self.headers = {
            'cookie': '__jdu=2027411329; shshshfpa=dcf828bb-26c7-1bf9-eddb-aedf2ad269e4-1544405556; ipLoc-djd=1-72-2799-0; user-key=480788c1-08b9-4726-a0c2-08d1b15a1d64; cn=0; TrackID=1_iU3MgN5zcOymeBQup52W8YuGDpRTl-he3tzHPHbwMt8p6C75HHmP_SdMSMiGIDZLLWkvX9j1V7siRrdOxzisERvUxohfCKrBZV8wWtv0Co; pinId=d-_HP7UQyOCp6d_620FEBw; pin=xian1754998731; unick=xian1754998731; _tp=VLqiMCjfEa%2BhnAfGhTIyow%3D%3D; _pst=xian1754998731; PCSYCityID=412; mt_xid=V2_52007VwATUVtdUlodShFsDWYKG1BUW1RGH0kYXhliBRFVQVBXXRZVGQsDZwJBUFReBw9NeRpdBW4fElFBW1RLH0kSXwdsAxViX2hSahZKH1QDYQIaUF5dU1oZTxldDGUzEldbXw%3D%3D; __jda=122270672.2027411329.1543217935.1545901231.1545963760.10; __jdc=122270672; unpl=V2_ZzNtbRJVFkBwCxVceRkODWJWEl0RVEAQIAsSBH4YC1FiVBYOclRCFXwURldnGlUUZwIZX0NcQxVFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3oaWgBnAxBeSmdzEkU4dlB8HFsAYzMTbUNnAUEpDUBRexlbSGQCEVtHV0MXdgB2VUsa; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_a3dd42b931c94d11b224d2ea40fe4f5b|1545964209520; shshshfpb=lG3zx4p4DpzDv6wVfN%2F%2Fr5w%3D%3D; 3AB9D23F7A4B3C9B=NG4POBEIK3RJOOGB5IFUCY5CHKIGA5UIH55GA46GHQNYEESMNDPC6ATBEX4YRZA6WD2MELNXBV2MGPZPOVY5VVQP24; shshshfp=8f65a1cc69800eb93c7a187c9bde0ad7; _gcl_au=1.1.2070307030.1545964965; JSESSIONID=708185D649529CE7571DA0ED1C194A77.s1; shshshsID=e45242f98ac79b59ab110b123f10e911_8_1545965205325; __jdb=122270672.11.2027411329|10.1545963760',
            'referer': 'https://item.jd.com/100000287113.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',

        }
        self.conn = None
        self.cursor = None
        self.create_table()

    def get_html(self):
        # 获取评论源码并转换为json数据
        comment_resp = requests.get(url=self.comment_url, params=self.params, headers=self.headers)
        comment_str = comment_resp.text
        comment_dict = json.loads(comment_str)
        self.parse_html(comment_dict)

    def parse_html(self,comment_dict):
        # 从json中提取数据
        comments = comment_dict['comments']
        for comment in comments:
            # 商品id
            id = comment['id']
            # 颜色
            productColor = comment['productColor']
            # 类型
            productSize = comment['productSize']
            # 会员
            userLevelName = comment['userLevelName']
            # 评论内容
            # content = comment['content']
            # 评论时间
            creationTime = comment['creationTime']
            # 评分
            score = comment['score']
            # 昵称
            nickname = comment['nickname']
            # print(nickname)
            # print(score)
            # print(id)
            # 保存数据
            self.save_data(id,productColor,productSize,userLevelName, creationTime,score,nickname)

    def save_data(self,*args):
        # 插入数据
        self.connect_sql()
        sql = """insert into jd ( id, productColor, productSize, userLevelName, creationTime, score, nickname) VALUES (%s,"%s","%s","%s","%s",%s,"%s")"""%args
        self.cursor.execute(sql)
        self.close_sql()

    def connect_sql(self):
        # 连接数据库
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='jd',
            # charset='utf-8'
        )
        self.cursor = self.conn.cursor()

    def close_sql(self):
        #关闭数据库
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        # 创建表
        self.connect_sql()
        sql = 'CREATE TABLE IF NOT EXISTS jd(s_id int auto_increment primary key ,id bigint ,productColor text ,productSize text ,userLevelName text ,creationTime datetime,score int ,nickname text )'
        self.cursor.execute(sql)
        self.close_sql()

    def run(self):
        # 指定爬取前十页数据
        for n in range(31):
            print(f'正在获取第{n+1}页')
            self.params = {
                'productId': '100000287113',
                'score': 0,
                'sortType': 5,
                'page': n,
                'pageSize': 10,
            }
            self.get_html()
            time.sleep(1)
            # break


if __name__ == '__main__':
    jdrun = JdData()
    jdrun.run()
