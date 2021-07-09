import pymysql, re
from ModelNode import Node

class bd_data:
    def exist():
        data = False
        cur = bd.show_tables()
        for tabla in cur.fetchall():
            if(tabla[0] == 'data'):
                data = True
        return data
    
    def getData():
        cur = bd.exec_query("select * from data;")
        return cur
    
    def getColumnsNames():
        query = "select column_name from information_schema.columns where table_schema='TFG' and table_name='data';"
        return bd.exec_query(query)
    
    def getTypeColumn(column):
        query = f"SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'data' AND COLUMN_NAME = '{column}';"
        cur = bd.exec_query(query)
        tipo = cur.fetchall()[0][0]
        return tipo

    def getDataByAttributes(attributes):
        query = ''
        for item in attributes:
            if(item == attributes[0]):
                query = query + f'select {item}'
            else:
                query = query + f', {item}'
        query = query + f' from data;'
        cur = bd.exec_query(query)
        return cur.fetchall()

class bd_attributes:
    def create():
        bd.exec_query('create table attributes(attribute varchar(20), tipo varchar(20));')
        for attribute in bd_data.getColumnsNames():
            bd.exec_query(f"insert into attributes values ('{attribute[0]}', 'No sensible')")
    
    def exist():
        cur = bd.show_tables()
        attributes = False
        for tabla in cur.fetchall():
            if(tabla[0] == f'attributes'):
                attributes = True
        return attributes
    
    def clear():
        bd.exec_query('delete from attributes;')
    
    def insert(attribute, tipo):
        bd.exec_query(f"insert into attributes values ('{attribute}','{tipo}')")

    def getNonSensible():
        query = "select attribute from attributes where tipo = 'No sensible';"
        cur = bd.exec_query(query)
        data = cur.fetchall()
        attributes = []
        for i in range(len(data)):
            attributes.append(data[i][0])

        return attributes

    def getNonIdentificator():
        query = "select attribute from attributes where tipo = 'Sensible' or tipo = 'No sensible';"
        cur = bd.exec_query(query)
        data = cur.fetchall()
        attributes = []
        for i in range(len(data)):
            attributes.append(data[i][0])

        return attributes

    def getNameNonIdentificator(number):
        attributes = bd_attributes.getNonIdentificator()
        return attributes[number]

    def getTipo(attribute):
        cur = bd.exec_query(f"select tipo from attributes where attribute = '{attribute}';")
        return cur.fetchall()[0][0]

class bd_hierarchy:
    def getData(attribute):
        query = f'select * from hierarchy_{attribute}'
        cur = bd.exec_query(query)
        return cur.fetchall()
  
    def exist(attribute):
        cur = bd.show_tables()
        hierarchy = False
        for tabla in cur.fetchall():
            if(tabla[0] == f'hierarchy_{attribute}'):
                hierarchy = True
        return hierarchy
    
    def clear(attribute):
        query = f'delete from hierarchy_{attribute};'
        bd.exec_query(query)        
    
    def drop(attribute):
        query = f'drop table hierarchy_{attribute};'
        bd.exec_query(query)        
    
    def create(attribute, num_columns):
        tipo = bd_data.getTypeColumn(attribute)
        query = f'create table hierarchy_{attribute} ('
        for i in range(num_columns):
            if(i==0):
                query = query + f"level_{i} {tipo}" 
            else:
                query = query + f", level_{i} varchar(10)"           
        query = query + ');'
        bd.exec_query(query)
    
    def insert(attribute, row):
        pattern = re.compile("int")
        tipo = bd_data.getTypeColumn(attribute)

        query = f'insert into hierarchy_{attribute} values ('
        for j in range(len(row)):
            if (j == 0):
                if(pattern.search(tipo)): 
                    query = query + f'{row[j]}'
                else:
                    query = query + f"'{row[j]}'"
            else:
                query = query + f", '{row[j]}'"
        query = query + ');'
        bd.exec_query(query)  
    
    def levels(attribute):
        query = f"select count(*) from information_schema.columns where table_name='hierarchy_{attribute}';"
        cur = bd.exec_query(query)
        number = cur.fetchall()[0][0]
        return number-1 

    def getGeneralization(attribute, level_init, level_end, valor):
        query = ''
        if(type(valor)==str):
            query = f"select level_{level_end} from hierarchy_{attribute} where level_{level_init} = '{valor}';"
        else:
            query = f"select level_{level_end} from hierarchy_{attribute} where level_{level_init} = {valor};"
        cur = bd.exec_query(query)
        generalization = cur.fetchall()
        return generalization[0][0]

    def getLevel(attribute, value):
        levels = bd_hierarchy.levels(attribute)
        for level in range(levels+1):
            query = ''
            if(type(value)==str):
                query = f"select * from hierarchy_{attribute} where level_{level} = '{value}';"
            else: 
                query = f"select * from hierarchy_{attribute} where level_{level} = {value};"
            cur = bd.exec_query(query)
            if (cur.fetchall()):
                return level

class bd_nodes:
    def create(dimension, nodes, quasiidentifiers): 
        node_end = []
        attributes = []
        for i in range(dimension):
            attributes.append(quasiidentifiers[i])
        
        for attribute in attributes:
            level = bd_hierarchy.levels(attribute)
            node_end.append(level)

        query = f'create table nodes_{dimension} (id int(3)' 
        for i in range(dimension):
            query = query + f', dim{i} varchar(10), index{i} int(2)'
        query = query + f');'
        bd.exec_query(query)        

        id = 1
        for node in nodes:
            bd_nodes.insert(id, attributes, node)
            id = id + 1

    def exist(dimension):
        cur = bd.show_tables()
        nodes = False
        for tabla in cur.fetchall():
            if(tabla[0] == f'nodes_{dimension}'):
                nodes = True
        return nodes

    def drop(dimension):
        bd.exec_query(f'drop table nodes_{dimension}')

    def existNode(dimension, index):
        query = f'select count(*) from nodes_{dimension} where '
        for i in range(dimension):
            if(i==dimension-1):
                query = query + f'index{i} = {index[i]};'
            else:
                query = query + f'index{i} = {index[i]} and '

        cur = bd.exec_query(query)
        if(cur.fetchall()[0][0]==1):
            return True
        else:
            return False

    def insert(id, dim, index): 
        query = f'insert into nodes_{len(dim)} values ({id}'      
        for i in range(len(dim)):
            query = query + f", '{dim[i]}', {index[i]}"
        query = query + ');'
        bd.exec_query(query)

    def aumentar(node_init, node_end):
        l = len(node_init)-1
        while(l>=0):
            if(node_init[l] < node_end[l]):
                node_init[l] = node_init[l]+1  
                break        
            else:
                node_init[l] = 0
                l=l-1

        return node_init

    def getNodeFin(dimension):
        query = f'select count(*) from nodes_{dimension};'
        cur = bd.exec_query(query)
        id = cur.fetchall()[0][0]

        return bd_nodes.getNodePorId(id, dimension)

    def getNodePorId(id, dimension):
        query = ''
        for i in range(dimension):
            if (i==0):
                query = query + f'select index{i}'
            else:
                query = query + f', index{i}'
        query = query + f' from nodes_{dimension} where id={id}'

        cur = bd.exec_query(query)

        node = []
        for item in cur.fetchall()[0]:
            node.append(item)

        return node

    def getId(index):
        dimension = len(index)
        lon = dimension-1
        query = f'select id from nodes_{dimension} where '
        for i in range(lon):
            query = query + f'index{i} = {index[i]} and '
        query = query + f'index{lon} = {index[lon]};'

        cur = bd.exec_query(query)
        id = cur.fetchall()
        return id[0][0]

    def getIndex(dimension, id):
        query = f'select'
        for i in range(dimension):
            if(i==0):
                query = query + f' index{i}'
            else:
                query = query + f', index{i}'
        query = query + f' from nodes_{dimension} where id = {id};'

        cur = bd.exec_query(query)
        
        return list(cur.fetchall()[0])
    
    def getNodesConsecutivos(node_init, node_end): #values
        nodes = []
        node_cons = node_init.copy()
        l = len(node_init)-1
        while (l>=0):
            if(node_init[l]<node_end[l]):
                node_cons[l] = node_cons[l]+1
                nodes.append(node_cons)
                node_cons = node_init.copy()
            l = l-1

        return nodes

    def getData(dimension):
        query = ''
        for i in range(dimension):
            if(i==0):
                query = query + f'select index{i}'    
            else:
                query = query + f', index{i}'      
        query = query + f' from nodes_{dimension}'   

        cur = bd.exec_query(query)
        
        index = []
        for i in cur.fetchall():
            node = Node(list(i))
            index.append(node)

        return index

    def getIds(dimension):
        cur = bd.exec_query(f'select id from nodes_{dimension}')
        return cur.fetchall()

    def getRoots(dimension):
        cur = bd.exec_query(f'select distinct(start) from edges_{dimension} where start not in (select end from edges_{dimension});')
        
        roots=[]
        for id in cur.fetchall():
            root = bd_nodes.getNodePorId(id[0], dimension)
            roots.append(root)

        return roots

    def isRoot(index):
        dimension = len(index)
        roots = bd_nodes.getRoots(dimension)
        return(index in roots)

    def getFathers(node):
        dimension = node.getDimension()
        id = node.getId()
        id_fathers = bd_edges.getIdFathers(dimension, id)
        fathers = []
        for item in id_fathers:
            value = bd_nodes.getIndex(dimension, item[0])
            fathers.append(Node(value))

        return fathers
    
class bd_edges:
    def create(dimension):
        if(bd_edges.exist(dimension)==False):
            bd.exec_query(f'create table edges_{dimension} (start int(2), end int(2));')

        node_end = bd_nodes.getNodeFin(dimension)
        nodes = bd_nodes.getData(dimension)

        for node in nodes:
            id_init = node.getId()
            nodes_consecutivos = bd_nodes.getNodesConsecutivos(node.getValue(), node_end)

            for node_cons in nodes_consecutivos:
                id_end = bd_nodes.getId(node_cons)  

                if(bd_nodes.existNode(dimension, node.getValue()) and bd_nodes.existNode(dimension, node_cons)):
                    bd_edges.insert(dimension,id_init, id_end)

    def insert(dimension, start, end):
        bd.exec_query(f'insert into edges_{dimension} values ({start}, {end});')
    
    def exist(dimension):
        cur = bd.show_tables()
        edges = False
        for tabla in cur.fetchall():
            if(tabla[0] == f'edges_{dimension}'):
                edges = True
        return edges

    def drop(dimension):
        bd.exec_query(f'drop table edges_{dimension}')

    def getData(dimension):
        cur = bd.exec_query(f'select * from edges_{dimension}')
        return cur.fetchall()

    def getIdFathers(dimension, id):
        query = f'select start from edges_{dimension} where end = {id};'
        cur = bd.exec_query(query)
        return cur.fetchall()

class bd:
    def exec_query(query):  
        f = open("DBconnection.txt", "r")
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        line4 = f.readline()
        try:
            conn=pymysql.connect(
                host=line1.split('=')[1].split('\n')[0],
                user=line2.split('=')[1].split('\n')[0],
                passwd=line3.split('=')[1].split('\n')[0],
                database=line4.split('=')[1].split('\n')[0]
            )
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
            conn.close()
            return cur 

        except pymysql.Error as e:
            print("Error al conectarse a la bd ",e)

    def drop_tables():
        cur =bd.exec_query("SELECT CONCAT('drop table ',table_name,'; ') FROM information_schema.tables WHERE table_schema = 'TFG';")
        for comand in cur.fetchall():
            bd.exec_query(comand[0])

    def dropAlgorithmData():
        cur = bd.exec_query("SELECT CONCAT('drop table ',table_name,'; ') FROM information_schema.tables WHERE table_schema = 'TFG' and table_name != 'data' and table_name != 'attributes' and table_name not like 'hierarchy_%';")
        for comand in cur.fetchall():
            bd.exec_query(comand[0])

    def show_tables():
        return bd.exec_query('show tables;')