# Author: GouHaoliang
# Date: 2025/6/10
# Time: 15:31


CREATE_TABLES = {
    "shift_pos_emp_info": """
    CREATE TABLE if not exists `shift_pos_emp_info` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
      `pos_no` int(11) NOT NULL COMMENT '工位编号',
      `emp_name` varchar(255) NOT NULL COMMENT '员工姓名',
      `shift` varchar(255) NOT NULL COMMENT '员工班次',
      `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工班次位置表';
    """,

    "operation_track_record": """
    CREATE TABLE if not exists `operation_track_record` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
      `pos_no` int(11) NOT NULL COMMENT '工位编号',
      `emp_name` varchar(255) NOT NULL COMMENT '员工姓名',
      `impurity_rate` decimal(4,3) NOT NULL COMMENT '扣杂率',
      `op_time` datetime NOT NULL COMMENT '操作时间',
      `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生产线操作记录表';
    """
}

SQL_QUERIES = {
    # 检查是否已经完成班次结算
    "check_status": """select * from shift_pos_emp_info where end_time = '9999-12-31 00:00:00'; """,

    # 表格1：操作统计表(输入的price要求为数值类型）
    "emp_stats": """
    select 
        pos_no, emp_name,
        count(1) as bucket_num, 
        avg(impurity_rate) as avg_rate,
        unit_price,
        sum(unit_price * (1 - impurity_rate)) as amount,
        '' as note
    from operation_track_record
    where op_time >= '{start_time}'
    and op_time <= '{end_time}'
    and shift = '{shift}'
    group by pos_no, emp_name, unit_price
    order by pos_no;
    """,

    # 表格2：单个工位的操作记录
    "pos_op_record": """
    select
        op_time,
        impurity_rate,
        '' as note
    from operation_track_record 
    where pos_no = '{pos_no}' 
    and date(op_time) >= '{start_date}'
    and date(op_time) < '{end_date}'
    order by op_time; 
    """,

    # 表格3：班次统计表
    "shift_stats": """
    select 
        shift,
        concat(min(op_time), '-', max(op_time)) as time_range,
        count(1) as bucket_num,
        avg(impurity_rate) as avg_rate,
        avg(unit_price) as avg_price,
        sum(unit_price * (1 - impurity_rate)) as amount,
        '' as note
    from operation_track_record
    where date(op_time) >= '{start_date}'
    and date(op_time) < '{end_date}'
    group by shift;
    """,

    # 表格4：单日统计表
    "day_stats": """
    select 
        shift,
        concat(min(op_time), '-', max(op_time)) as time_range,
        count(1) as bucket_num,
        avg(impurity_rate) as avg_rate,
        unit_price,
        sum(unit_price * (1 - impurity_rate)) as amount,
        '' as note
    from operation_track_record
    where date(op_time) = '{stats_date}'
    group by shift, unit_price;
    """
}

