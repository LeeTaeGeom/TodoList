from crypt import methods
import curses
from flask import Flask, redirect, url_for, request,render_template, session
import sqlite3
app = Flask(__name__)

# -------------- 회원가입, 로그인, 로그아웃

def insertUserDb(userId,userPwd):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        insert into User(userId,userPwd)
        values(?,?)
    """
    cursor.execute(sql,(userId,userPwd))
    conn.commit()
    conn.close()

def findUser(userId):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        select * from User where userId=? 
    """
    cursor.execute(sql,(userId,))
    user=cursor.fetchone()
    conn.close()
    return user


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup_submit',methods=['POST'])
def signup_submit():
    if request.method=='POST':
        userId=request.form['userid']
        userPwd=request.form['userpwd']
        # print(findUser(userId))
        if findUser(userId)==None:
            
            insertUserDb(userId,userPwd)
            return redirect(url_for('success',i=1))
        else:
            return redirect(url_for('alert',i=2))

    else:
        return "잘못된 접근입니다"

    

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login_submit',methods=['POST'])
def login_submit():
    
    if request.method=='POST':
        userId=request.form['userid']
        userPwd=request.form['userpwd']
        user=findUser(userId)
        
        if user!=None:
            if user[2] == userPwd:
                session['logFlag']=True
                session['userId']=userId
                return redirect(url_for('main'))
            else:
                return redirect(url_for('alert',i=3))

        else:
            return redirect(url_for('alert',i=1))
    else:
        return "잘못된 접근입니다"
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))


# ------------------ todolist CRUD
def insertInfo(title,content,public,writer,start,end):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        insert into TodoList(title,content,public,writer,start,end)
        values(?,?,?,?,?,?)
    """
    cursor.execute(sql,(title,content,public,writer,start,end))
    conn.commit()
    conn.close()

def updateInfo(id,title,content,public,writer,start,end):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        update TodoList set title=?, content=?, public=?, writer=?, start=?,end=?
        where idx=?;
    """
    cursor.execute(sql,(title,content,public,writer,start,end,id))
    conn.commit()
    conn.close()
    
def getList():
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    me=session['userId']
    show='공개'
    sql="""
        select * from TodoList where writer=? or public=? order by start;
    """
    cursor.execute(sql,(me,show))
    lists=cursor.fetchall()
    conn.close()
    return lists

def getOne(id):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        select * from TodoList where idx=? 
    """
    cursor.execute(sql,(id,))
    willupdate=cursor.fetchone()
    conn.close()
    return willupdate

@app.route('/createTodoList',methods=['POST'])
def createTodoList():
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']
        public=request.form['public']
        writer=session['userId']
        start=request.form['start']
        end=request.form['end']
        # print(writer)
        if start<end:
            insertInfo(title,content,public,writer,start,end)
            return redirect(url_for('list'))
        else:
            return redirect(url_for('alert',i=4))
            
    else:
        return "잘못된 접근입니다"   

@app.route('/list')
def list():
    todolists=getList()
    comments=getComment()
    # for i in comments:
    #     print(i)
    return render_template('showlist.html',lists=todolists,comments=comments)

@app.route('/updateForm/<int:id>')
def updateForm(id):
    thisOne=getOne(id)
   
    return render_template('updateForm.html',thisOne=thisOne)
    

@app.route('/updateTodoList/<int:id>',methods=["POST"])
def updateTodoList(id):
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']
        public=request.form['public']
        writer=session['userId']
        start=request.form['start']
        end=request.form['end']
        # print(writer)
        if start<end:
            updateInfo(id,title,content,public,writer,start,end)
            return redirect(url_for('list'))
        else:
            return redirect(url_for('alert',i=5))
 
    else:
        return "잘못된 접근입니다"   

@app.route('/deleteTodo/<int:id>')
def deleteTodo(id):
    
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        delete from TodoList where idx=? 
    """
    cursor.execute(sql,(id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list'))
# ------------------ comment

def commentInfo(todolist,comment,writer):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        insert into comment(todolist,comment,writer)
        values(?,?,?)
    """
    cursor.execute(sql,(todolist,comment,writer))
    conn.commit()
    conn.close()

def getComment():
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        select * from comment
    """
    cursor.execute(sql)
    comments=cursor.fetchall()
    conn.close()
    
    return comments
    
@app.route('/createComment/<int:id>',methods=['POST'])
def createComment(id):
    if request.method == 'POST':
        todolist=id
        comment=request.form['comment']
        writer=session['userId']
        commentInfo(todolist,comment,writer)
        return redirect(url_for('list'))
    else:
        return "잘못된 접근입니다"  
    
@app.route('/deleteComment/<int:ct_id>')
def deleteComment(ct_id):
    conn=sqlite3.connect('software.db')
    cursor=conn.cursor()
    sql="""
        delete from comment where idx=? 
    """
    cursor.execute(sql,(ct_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list'))

# ------------------ alert  & success
@app.route('/alert/<int:i>')
def alert(i):
    return render_template('alert.html',check=i)  

@app.route('/success/<int:i>')
def success(i):
    return render_template('success.html',check=i)  
    

# 세션생성시 시크릿키 있어야함(임의의 문자열)

if __name__ == '__main__':
    
    app.secret_key = 'software_engineering'
    app.run(debug = True)