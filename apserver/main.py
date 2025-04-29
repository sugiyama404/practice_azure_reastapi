from flask import Flask, jsonify, request
import os
import pymysql
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.environ.get('DB_HOST', 'db'),
            user=os.environ.get('DB_USER', 'goMySql1'),
            password=os.environ.get('DB_PASSWORD', 'goMySql1'),
            database=os.environ.get('DB_NAME', 'todoproject'),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"MySQL接続エラー: {e}")
        raise
    except Exception as e:
        logger.error(f"データベース接続中に予期せぬエラーが発生: {e}")
        raise

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@app.route('/')
def health_check():
    return jsonify({"status": "Flask is running!"})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM todos WHERE deleted_at IS NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            result = cursor.fetchone()
            if result:
                return jsonify(result)
            else:
                logger.info(f"Todo with id {todo_id} not found")
                return jsonify({"error": "Todo not found"}), 404
    except pymysql.MySQLError as e:
        logger.error(f"Database error in get_todo: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_todo: {e}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/todos', methods=['POST'])
def create_todo():
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Content is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO todos (content) VALUES (%s)"
            cursor.execute(sql, (content,))
            connection.commit()

            new_id = cursor.lastrowid
            sql = "SELECT * FROM todos WHERE id = %s"
            cursor.execute(sql, (new_id,))
            result = cursor.fetchone()
            return jsonify(result), 201
    finally:
        connection.close()

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Content is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Todo not found"}), 404

            sql = "UPDATE todos SET content = %s WHERE id = %s"
            cursor.execute(sql, (content, todo_id))
            connection.commit()

            sql = "SELECT * FROM todos WHERE id = %s"
            cursor.execute(sql, (todo_id,))
            result = cursor.fetchone()
            return jsonify(result)
    finally:
        connection.close()

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Todo not found"}), 404

            sql = "UPDATE todos SET deleted_at = %s WHERE id = %s"
            cursor.execute(sql, (datetime.now(), todo_id))
            connection.commit()
            return jsonify({"message": f"deleted todo with id {todo_id}"}), 201
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
