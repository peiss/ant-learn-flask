import datetime
import os

import xlwt
from flask import Flask, render_template, request, send_from_directory
import json

from pyecharts.charts import Bar, Pie, Line

from pyecharts import options as opts
import db
from jinja2 import Markup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return hello_world2()


@app.route('/hello')
def hello_world2():
    data = "hello data"
    return render_template("hello.html", data=data)


@app.route("/user/<username>", methods=["GET", "POST"])
def get_user(username):
    return "hello %s" % username


@app.route('/data', methods=["POST", "GET"])
def test_data():
    # print(request.args)
    # print(request.args.get("a"), request.args.get("b"))
    # print(request.headers)
    # print(request.headers.get("User-Agent"))
    # print(request.data)
    # import json
    # print(json.loads(request.data))
    # print(request.cookies)
    # print(request.cookies.get("token"))
    print(request.form)
    print(request.form.get("username"), request.form.get("password"))
    return 'success'


@app.route("/use_template")
def use_template():
    datas = [(1, "name1"), (2, "name2"), (3, "name3")]
    title = "学生信息"
    return render_template("use_template.html", datas=datas, title=title)


def read_pvuv_data():
    """
    read pv uv data
    :return: list, ele: (pdate, pv, uv)
    """
    data = []
    with open("./data/pvuv.txt") as fin:
        is_first_line = True

        for line in fin:
            if is_first_line:
                is_first_line = False
                continue
            line = line[:-1]
            pdate, pv, uv = line.split("\t")
            data.append((pdate, pv, uv))
    return data


@app.route("/pvuv")
def pvuv():
    # read file
    data = read_pvuv_data()
    # return html
    return render_template("pvuv.html", data=data)


@app.route("/getjson")
def getjson():
    # read file
    data = read_pvuv_data()
    # return html
    return json.dumps(data)


@app.route("/show_add_user")
def show_add_user():
    return render_template("show_add_user.html")


@app.route("/do_add_user", methods=['POST'])
def do_add_user():
    print(request.form)
    name = request.form.get("name")
    sex = request.form.get("sex")
    age = request.form.get("age")
    email = request.form.get("email")
    sql = f"""
        insert into user (name, sex, age, email)
        values ('{name}', '{sex}', {age}, '{email}')
    """
    print(sql)
    db.insert_or_update_data(sql)
    return "success"


@app.route("/show_users")
def show_users():
    sql = "select id,name from user"
    datas = db.query_data(sql)
    return render_template("show_users.html", datas=datas)


@app.route("/show_user/<user_id>")
def show_user(user_id):
    sql = "select * from user where id=" + user_id
    datas = db.query_data(sql)
    user = datas[0]
    return render_template("show_user.html", user=user)


@app.route("/show_echarts")
def show_echarts():
    xdatas = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    ydatas = [5, 20, 36, 10, 10, 20]
    return render_template("show_echarts.html",
                           xdatas=Markup(json.dumps(xdatas)),
                           ydatas=json.dumps(ydatas))


@app.route("/show_pyecharts")
def show_pyecharts():
    bar = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    )
    return render_template("show_pyecharts.html",
                           bar_options=bar.dump_options())


def get_pie() -> Pie:
    sql = """
        select sex,count(1) as cnt from user group by sex
    """
    datas = db.query_data(sql)
    c = (
        Pie()
            .add("", [(data['sex'], data['cnt']) for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def get_bar() -> Bar:
    sql = """
            select sex,count(1) as cnt from user group by sex
        """
    datas = db.query_data(sql)
    c = (
        Bar()
            .add_xaxis([data['sex'] for data in datas])
            .add_yaxis("数量", [data['cnt'] for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


def get_line() -> Line:
    sql = """
                select pdate,pv,uv from pvuv
            """
    datas = db.query_data(sql)
    c = (
        Line()
            .add_xaxis([str(data['pdate']) for data in datas])
            .add_yaxis("pv", [data['pv'] for data in datas])
            .add_yaxis("uv", [data['uv'] for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
    )
    return c


@app.route("/show_myecharts")
def show_myecharts():
    pie = get_pie()
    bar = get_bar()
    line = get_line()
    return render_template("show_myecharts.html",
                           pie_options=pie.dump_options(),
                           bar_options=bar.dump_options(),
                           line_options=line.dump_options())


def generate_excel(data_dir, fname):
    fpath = os.path.join(data_dir, fname)
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("pvuv")
    for idx, name in enumerate(["日期", "pv", "uv"]):
        worksheet.write(0, idx, name)
    datas = db.query_data("select * from pvuv")
    for row, data in enumerate(datas):
        for col, kv in enumerate(data.items()):
            worksheet.write(row + 1, col, kv[1])
    workbook.save(fpath)


@app.route("/download_pvuv_excel")
def download_pvuv():
    data_dir = os.path.join(app.root_path, "downloads")
    now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"pvuv_{now_time}.xls"

    generate_excel(data_dir, fname)

    return send_from_directory(data_dir, fname, as_attachment=True)


if __name__ == '__main__':
    app.run()
