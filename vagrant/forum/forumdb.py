#
# Database access functions for the web forum.
#

import time
import psycopg2

## Database connection
DB = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
##    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
##    posts.sort(key=lambda row: row['time'], reverse=True)
##    return posts
    cursor = DB.cursor()
    cursor.execute("SELECT time, content FROM posts;")
    results = cursor.fetchall()
##    print ("Testing HERE--> ")
##    print (results)
    return results
    cursor.close()

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    cursor = DB.cursor()
    t = time.strftime('%c', time.localtime())
##    DB.append((t, content))
    sql = "INSERT INTO posts (content) VALUES (%s);"
    cursor.execute(sql, [content])
    DB.commit()
    cursor.close()


