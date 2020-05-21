from db import Sql
from datetime import datetime




def get_now_data(t):
    sql = Sql()
    ret = sql.execute(f"select id, alg0, alg1, alg2, alg3, alg4, alg5, alg6, alg7, alg8 from pt_{t} order by id desc limit 1")
    ret = ret[0][0]
    id = ret[0]
    data = dict(
        id=id,
        alg0=ret[1],
        alg1=ret[2],
        alg2=ret[3],
        alg3=ret[4],
        alg4=ret[5],
        alg5=ret[6],
        alg6=ret[7],
        alg7=ret[8],
        alg8=ret[9],
    )
    ret = sql.execute(f"select pub_time from pt where id < {id} order by id desc limit 1")
    try:
        t = ret[0][0][0]
        t = datetime.strptime(t, "%Y:%m:%d %H:%M").timestamp()
    except Exception as e:
        print(e)
        t = 20
    sql.close()
    return dict(t=t, data=data)

if __name__ == '__main__':
    get_now_data("big")



