from flask import Flask
from flask import request, jsonify, render_template
from db import Sql
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/now/<t>")
def big(t):
    sql = Sql()
    ret = sql.execute(
        f"select id, alg0, alg1, alg2, alg3, alg4, alg5, alg6, alg7, alg8 from fenxi_{t} order by id desc limit 1")

    ret = ret[0][0]
    data = dict(id=ret[0], alg0=ret[1], alg1=ret[2], alg2=ret[3], alg3=ret[4], alg4=ret[5], alg5=ret[6], alg6=ret[7],
                alg7=ret[8], alg8=ret[9])
    id = int(data.get("id", 0)) - 1
    t = sql.execute("select pub_time from fenxi where id = {}".format(id))
    sql.close()
    try:
        t = t[0][0][0]
        t = datetime.strptime(str(datetime.today().year) + "-" + t, "%Y-%m-%d %H:%M").timestamp()
    except Exception as e:
        print(e)
        t = 20
    data = {
        "t": t,
        "data": data
    }
    return jsonify(data)


@app.route("/history/<t>/<num>")
def history(t, num):
    if not num.isdigit():
        num = 10
    s = f"""
    select a.id, a.pub_time, a.result, b.alg1, b.res1, b.alg2, b.res2,b.alg3, b.res3, b.alg4, b.res4,b.alg5, b.res5, b.alg6, b.res6,b.alg7, b.res7, b.alg8, b.res8, b.alg0, b.res0, b.pet1,  b.gain1, b.pet2, b.gain2, b.pet3, b.gain3, b.pet4, b.gain4
    from fenxi a 
    left join fenxi_{t} b 
    on a.id = b.id 
    where a.result != '' and b.res0 != "" and b.gain1 is not null and b.gain2 is not null and b.gain3 is not null and b.gain4 is not null
    order by a.id desc
    limit {num}
    """
    sql = Sql()
    ret = sql.execute(s)
    sql.close()
    ret = ret[0]
    num = len(ret)
    res = []
    rate = [0] * 9
    pet1, pet2, pet3, gain1, gain2, gain3, pet4, gain4 = 0, 0, 0, 0, 0, 0, 0, 0
    for r in ret:
        # print(r)
        try:
            res.append(dict(id=r[0],
                            pub_time=r[1],
                            result=r[2],
                            alg1=(r[3], r[4]),
                            alg2=(r[5], r[6]),
                            alg3=(r[7], r[8]),
                            alg4=(r[9], r[10]),
                            alg5=(r[11], r[12]),
                            alg6=(r[13], r[14]),
                            alg7=(r[15], r[16]),
                            alg8=(r[17], r[18]),
                            alg0=(r[19], r[20]),
                            pet1=r[21],
                            gain1=r[22],
                            pet2=r[23],
                            gain2=r[24],
                            pet3=r[25],
                            gain3=r[26],
                            pet4=r[27],
                            gain4=r[28]
                            ))
            # print("*******", r[21])
            # print(r)
            pet1 += int(r[21])
            gain1 += int(float(r[22]))
            pet2 += int(r[23])
            gain2 += int(float(r[24]))
            pet3 += int(r[25])
            gain3 += int(float(r[26]))
            pet4 += int(r[27])
            gain4 += int(float(r[28]))
        except Exception as e:
            print(e)
            continue
    for d in res:
        # 计算正确率
        for j, i in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 0], 0):
            if d.get("alg" + str(i))[1] == "对":
                rate[j] += 1

    rate = [str(round(i / num * 100, 2)) + "%" for i in rate]
    rate.insert(-1, "     ")
    rate.extend([pet1, gain1, pet2, gain2, pet3, gain3, pet4, gain4])
    return jsonify({"data": res, "rate": rate})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
