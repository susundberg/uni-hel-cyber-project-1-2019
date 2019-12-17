from config import DATABASE
import subprocess
import sqlite3


if __name__=="__main__":
    
    subprocess.run( ["rm", "-f", DATABASE ] )
    conn = sqlite3.connect( DATABASE )
    conn.execute( "CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, level INTEGER  NOT NULL )")
    conn.execute( "CREATE TABLE comments (id INTEGER PRIMARY KEY, user_id INTEGER, comment TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id) )")
    conn.execute("INSERT INTO users (username,password,level) VALUES ('admin','p',9)")
    conn.commit()
    conn.close()
