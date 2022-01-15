import sqlite3

conn=sqlite3.connect('software.db')
cursor=conn.cursor()
sql1="""
    create table User(
        idx integer primary key autoincrement,
        userId text not null,
        userPwd text not null );
    """
sql2="""
    create table TodoList(
        idx integer primary key autoincrement,
        title text not null,
        content text not null,
        public text not null,
        writer text not null,
        start text not null,
        end text not null,
        FOREIGN KEY (writer)
            REFERENCES User (userId) 
            ON DELETE CASCADE
        );
    """
sql3="""
    create table comment(
        idx integer primary key autoincrement,
        todolist interger not null,
        comment text not null,
        writer text not null,
        FOREIGN KEY (todolist)
            REFERENCES TodoList (idx) 
            ON DELETE CASCADE,
        FOREIGN KEY (writer)
            REFERENCES User (userId) 
            ON DELETE CASCADE);
    """
cursor.execute(sql1)
cursor.execute(sql2)
cursor.execute(sql3)

conn.close()