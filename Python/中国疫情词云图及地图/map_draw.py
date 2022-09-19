from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker


class Draw_map():
    def get_colour(self,a,b,c):
        result = '#'+''.join(map((lambda x:"%02x"%x),(a,b,c)))
        return result.upper()
    def to_map_city(self):
        c = (
            Map()
            .add("商家A", [list(z) for z in zip(Faker.guangdong_city, Faker.values())], "广东")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Map-广东地图"), visualmap_opts=opts.VisualMapOpts()
            )
            .render("map_guangdong.html")
        )
    def to_map_china(self,area,variate,update_time):
        pieces = [
            {'max':99999999,'min':10001,'label':'>10001','color':'#8A0808'},
            {'max':9999,'min':1000,'label':'10000-9999','color':'#B40404'},
            {'max':999,'min':100,'label':'100-999','color':'#DF0101'},
            {'max':99,'min':10,'label':'10-99','color':'#F5A9A9'},
            {'max':9,'min':1,'label':'1-9','color':'#F5A9A9'},
            {'max':0,'min':0,'label':'0','color':'#FFFFFF'}
        ]
        c = (
            Map(init_opts=opts.InitOpts(width='1000px',height='880px'))
            .add("确诊人数", [list(z) for z in zip(area, variate)], "china")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情地图分布",
                                            subtitle="截止日期%s 中国疫情分布情况"%(update_time),
                                            pos_left='center',pos_top='30px'),
                visualmap_opts=opts.VisualMapOpts(max_=200,is_piecewise=True,pieces=pieces),
            )
            .render('中国疫情地图.html')
        )