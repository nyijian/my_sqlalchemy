# Load Data from a list into the Table

#from sqlalchemy import Column, String, create_engine,MetaData,Table,select,or_,func,desc,case,cast,Float
# import pymysql
# import pandas as pd
# import matplotlib.pyplot as plt


# engine1 = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/m3800')
# print(engine1.table_names())
#
# connection = engine1.connect()





# engine = create_engine('sqlite:///census.sqlite')
# connection = engine.connect()
# # print(engine.table_names())
# metadata = MetaData()
# census = Table('census',metadata,autoload=True,autoload_with=engine)
# state_fact = Table('state_fact',metadata,autoload=True,autoload_with=engine)
# state_fact = Table('state_fact',metadata,autoload=True,autoload_with=engine)

#stmt = select([census])
#stmt = stmt.where(census.columns.state=='California')
#stmt = stmt.where(census.columns.state.startswith('New'))
#stmt = stmt.where(or_(census.columns.state=='California',census.columns.state=='New York'))
# stmt = select([census.columns.sex ,func.sum(census.columns.pop2008).label('pop2008_sum')])
# stmt =stmt.group_by(census.columns.sex )

# stmt = select([census.columns.age,(census.columns.pop2008 - census.columns.pop2000).label('pop_change')])
# stmt = stmt.group_by(census.columns.age)
# stmt = stmt.order_by(desc('pop_change'))
# stmt = stmt.limit(5)
# results = connection.execute(stmt).fetchall()
# print(results)


###Percentage Example
# stmt = select([
#     (func.sum(
#         case([
#             (census.columns.state == 'New York',
#              census.columns.pop2008)
#         ],else_=0))/ cast(func.sum(census.columns.pop2008),Float) *100).label('ny_percent')])
# results = connection.execute(stmt).fetchall()
# print(results)

####Relationships
#####Automatic joins
# stmt = select([census.columns.pop2008,state_fact.columns.abbreviation])
# results = connection.execute(stmt).fetchall()
# df = pd.DataFrame(results)
# df.columns = results[0].keys()
# print(df)

####Select_from Example  ???
# stmt = select([func.sum(census.columns.pop2000)])
# stmt = stmt.select_from(census.join(state_fact))
# stmt = stmt.where(state_fact.colums.circuit_court == '10')
# result = connection.execute(stmt).scalar()
# print(result)

####Joining Tables without predefined Relationship
# stmt = select([func.sum(census.columns.pop2000)])
# stmt = stmt.select_from(
#     census.join(state_fact,census.columns.state == state_fact.columns.name))
# stmt = stmt.where(state_fact.columns.census_division_name == 'East South Central')
# result = connection.execute(stmt).scalar()
# print(result)

####Working with Hierarchical Tables
#Using alias to handle same table joined queries
# engine = create_engine('sqlite:///employees.sqlite')
# connection = engine.connect()
# print(engine.table_names())
# metadata = MetaData()
# employees = Table('employees',metadata,autoload=True,autoload_with=engine)
# managers = employees.alias()
# stmt = select([managers.columns.name.label('manager'),
#                employees.columns.name.label('employee')])
# stmt = stmt.where(managers.columns.id == employees.columns.mgr)
#
# stmt = stmt.order_by(managers.columns.name)
# results = connection.execute(stmt).fetchall()
# for record in results:
#     print(record)

####Creating Tables with SQLAlchemy
#创建表
# from sqlalchemy import Table, Column, String, Integer, Float, Boolean,MetaData,create_engine
# # Define a new table with a name, count, amount, and valid column: data
# engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/m3800')
# connection = engine.connect()
# metadata = MetaData()
# data = Table('data', metadata,
#              Column('name', String(255), unique=True),
#              Column('count', Integer(), default=1),
#              Column('amount', Float()),
#              Column('valid', Boolean(), default=False))
# # Use the metadata to create the table
# metadata.create_all(engine)
# # Print table details
# # print(repr(data))
# print(repr(metadata.tables['data']))
##Inserting a single row with an insert() statement
#单行插入
from sqlalchemy import insert, select
# stmt = insert(data).values(name ='tom',count=1, amount=200, valid =True)
# results = connection.execute(stmt)
# print(results.rowcount)
# stmt = select([data]).where(data.columns.name == 'tom')
# print(connection.execute(stmt).first())
#多行插入
# values_list =[
#     {'name':'Anna1','count':1,'amount':100.00,'valid':True},
#     {'name':'Anna2','count':2,'amount':200.00,'valid':False}
# ]
# stmt = insert(data)
# results = connection.execute(stmt,values_list)
# print(results.rowcount)

####Loading a CSV into a Table
# from sqlalchemy import Table, Column, String, Integer, Float, Boolean,MetaData,create_engine,insert,select,update
# import csv
# csv_file = csv.reader(open('census.csv','r'))
# # Define a new table with a name, count, amount, and valid column: data
# engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/m3800')
# connection = engine.connect()
# metadata = MetaData()
# census_import = Table('census_import',metadata,
#                       Column('state',String(255)),
#                       Column('sex',String(4)),
#                       Column('age',Integer()),
#                       Column('pop2000',Integer()),
#                       Column('pop2008',Integer()))
# metadata.create_all(engine)
# stmt = insert(census_import)
# values_list = []
# total_rowcount= 0
# for idx, row in enumerate(csv_file):
#     data ={'state':row[0],'sex':row[1],'age':row[2],'pop2000':row[3],
#                     'pop2008':row[4]}
#     values_list.append(data)
#     if idx % 51 == 0:
#         results = connection.execute(stmt,values_list)
#         total_rowcount += results.rowcount
#         values_list =[]
# print(total_rowcount)
##Updating individual records
# census_import = Table('census_import',metadata,autoload=True,autoload_with=engine)
# select_stmt = select([census_import]).where(census_import.columns.sex == 'F')
# #print(connection.execute(select_stmt).fetchall())
# stmt = update(census_import).values(age=35)
# stmt = stmt.where(census_import.columns.sex=='F')
# results = connection.execute(stmt)
# print(results.rowcount)
# print(connection.execute(select_stmt).fetchall())
##Correlated Updates
# fips_stem = select([state_fact.columns.name])
# fips_stem = fips_stem.where(
#     state_fact.columns.fips_state == flat_census.columns.fips_code))
# update_stmt = update(flat_census).values(state_name=fips_stem)
# results = connection.execute(update_stmt)
# print(results.rowcount)


####Deleting all the records from a table
#清除记录
from sqlalchemy import Table,MetaData,create_engine,delete,select,func,and_
import pandas as pd
engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/m3800')
connection = engine.connect()
metadata = MetaData()
print(engine.table_names())
# data = Table('data',metadata,autoload=True,autoload_with=engine)
# stmt = delete(data)
# results = connection.execute(stmt)
# print(results.rowcount)
# stmt =select([data])
# print(connection.execute(stmt).fetchall())
##Deleting specific records
employee = Table('employee',metadata,autoload=True,autoload_with=engine)
# stmt = select([func.count(employee.columns.sex)]).where(
#     and_(employee.columns.sex=='m',employee.columns.agt==20))
# to_delete = connection.execute(stmt).scalar()
# stmt_del =delete(employee)
# stmt_det =stmt_del.where(
#     and_(employee.columns.sex=='m',employee.columns.agt==20))
# results = connection.execute(stmt_det)
# print(results.rowcount,to_delete)
##Deleting a Table Completely
employee.drop(engine)
print(employee.exists(engine))
# Drop all tables
metadata.drop_all(engine)
# Check to see if census exists
print(census.exists(engine))

































# df = pd.DataFrame(results)
# df.columns = results[0].keys()
#results = connection.execute(stmt).scalar()
# print(df)
# df.plot.barh()
# plt.show()

#results = connection.execute(stmt).fetchall()
# print(results[0].keys(),'\n', results[0])
# for result in results:
#     print(result.state,result.age)

# print(repr(census))
# stmt = "select * from census"
# result_proxy = connection.execute(stmt)
# result = result_proxy.fetchall()
# first_row = result[0]
# print(first_row)
# print(first_row.keys())
# print(first_row.state)

# stmt = select([census])
# results = connection.execute(stmt).fetchall()
# print(results[1:5])
