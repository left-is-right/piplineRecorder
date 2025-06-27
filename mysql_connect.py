# Author: GouHaoliang
# Date: 2025/5/27
# Time: 14:11

import pymysql
from sqlalchemy import create_engine, text, insert, Table, MetaData
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import Session
from sql_statement import CREATE_TABLES, SQL_QUERIES
import pandas as pd


def database_exists(host, user, password, database):

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # 检测数据库是否存在
    cursor.execute(f"SHOW DATABASES LIKE '{database}'")
    result = cursor.fetchone()

    if not result:
        # 创建数据库
        try:
            cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        finally:
            cursor.close()
            conn.close()
        print(f"✅ 数据库 '{database}' 创建成功")
    else:
        cursor.close()
        conn.close()
        print(f"⏩ 数据库 '{database}' 已存在")


class MysqlConnect:

    def __init__(self, user, password, database='pipline_recorder', host='localhost'):

        database_exists(host, user, password, database)

        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:3306/{database}",
            pool_size=10,  # 常驻连接数（默认5）[1,3](@ref)
            max_overflow=5,  # 允许临时创建的连接数（默认10）[1,5](@ref)
            pool_recycle=3600,  # 连接重置周期（秒），防数据库超时断开[3,5](@ref)
            pool_timeout=30,  # 获取连接的超时时间（秒）[3,7](@ref)
            pool_pre_ping=True,  # 使用前自动检查连接有效性（生产环境推荐）[5,7](@ref)
            echo=True
        )
        print(self.engine.pool.status())
        print("连接成功！")

    def close(self):
        self.engine.dispose()

    def select_sql(self, sql):
        print(sql)
        res = pd.read_sql_query(sql, self.engine)
        return res

    def update_end_time_sql(self, end_time):
        stmt = text("UPDATE shift_pos_emp_info SET end_time = :end_time WHERE end_time = '9999-12-31 00:00:00'; ")
        with Session(self.engine) as session:
            session.execute(stmt, {"end_time": end_time})
            session.commit()

    def create_table(self, table_name):
        with self.engine.connect() as conn:
            conn.execute(text(CREATE_TABLES[table_name]))

    def import_data(self, data, table_name='shift_pos_emp_info'):

        with self.engine.connect() as conn:
            conn.execute(text(CREATE_TABLES[table_name]))
            conn.commit()
            data.to_sql(
                name=table_name,
                con=conn,
                if_exists='append',  # 自动选择创建或追加
                index=False,  # 不写入索引列
                chunksize=500  # 分块写入提升性能
            )

    def insert_op(self, pos_no, emp_name, shift, impurity_rate, unit_price, op_time, table_name='operation_track_record'):
        # 2. 定义表结构（通过元数据反射）
        metadata = MetaData()
        # 反射加载现有表结构（无需手动定义列）
        try:
            operations_table = Table(table_name, metadata, autoload_with=self.engine)
        except NoSuchTableError:
            self.create_table(table_name)
            operations_table = Table(table_name, metadata, autoload_with=self.engine)

        # 3. 准备单条插入数据
        data = {
            "pos_no": pos_no,
            "emp_name": emp_name,
            "shift": shift,
            "impurity_rate": impurity_rate,
            "unit_price": unit_price,
            "op_time": op_time  # 需符合数据库DateTime格式
        }

        # 4. 构建并执行insert语句
        with self.engine.connect() as conn:
            stmt = insert(operations_table).values(**data)
            result = conn.execute(stmt)
            conn.commit()  # 显式提交事务

        print(f"插入成功，影响行数: {result.rowcount}")

    def select_shift_change_stats(self, shift, start_time, end_time):
        sql = SQL_QUERIES['emp_stats']
        sql = sql.format(shift=shift,
                         start_time=start_time,
                         end_time=end_time)

        return self.select_sql(sql)

    def select_today_stats(self, stats_date):
        sql = SQL_QUERIES['day_stats']
        sql = sql.format(stats_date=stats_date)

        return self.select_sql(sql)

    def select_his_stats(self, start_date, end_date):
        sql = SQL_QUERIES['shift_stats']
        sql = sql.format(start_date=start_date,
                         end_date=end_date
                         )

        return self.select_sql(sql)

    def select_his_detail(self, pos_no, start_date, end_date):
        sql = SQL_QUERIES['pos_op_record']
        sql = sql.format(pos_no=pos_no,
                         start_date=start_date,
                         end_date=end_date
                         )

        return self.select_sql(sql)


if __name__ == '__main__':
    user = 'root'
    password = '123456'
    conn = MysqlConnect(user, password)
    # table_name = 'shift_pos_emp_info'
    # data = pd.read_excel("员工班次输入样表.xlsx")
    # data['pos_no'] = data['工位编号']
    # data['emp_name'] = data['姓名']
    # data['shift'] = data['班次']
    # data = data[['pos_no', 'emp_name', 'shift']]
    # conn.import_data(data, table_name)

    table_name = 'operation_track_record'
    pos = 2
    name = '张三'
    shift = '甲班'
    rate = 0.15
    from datetime import datetime
    # 获取当前时间（精确到微秒）
    current_time = datetime.now()
    # 格式化为标准时间字符串（YYYY-MM-DD HH:MM:SS）
    op_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    conn.update_end_time_sql(op_time)
    # conn.insert_op(pos, name, shift, rate, op_time, table_name)
    start_time = '2025-06-17 00:00:00'
    end_time = '2025-06-18 00:00:00'
    end_date = "2025年6月18日"
    res = conn.select_shift_change_stats('乙班', start_time, end_time)
    print(res)
    print(len(res))
    from excel_writer import shift_change_stats_writer
    shift_change_stats_writer(res, end_date, '乙班')
