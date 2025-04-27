from flask import Flask, jsonify, request
import os
import pymysql
import json
from datetime import datetime

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'goMySql1'),
        password=os.environ.get('DB_PASSWORD', 'goMySql1'),
        database=os.environ.get('DB_NAME', 'todoproject'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Helper to convert datetime objects to string in JSON responses
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
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            result = cursor.fetchone()
            if result:
                return jsonify(result)
            else:
                return jsonify({"error": "Todo not found"}), 404
    finally:
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

            # Get the newly created todo
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
            # Check if todo exists
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Todo not found"}), 404

            # Update todo
            sql = "UPDATE todos SET content = %s WHERE id = %s"
            cursor.execute(sql, (content, todo_id))
            connection.commit()

            # Get the updated todo
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
            # Check if todo exists
            sql = "SELECT * FROM todos WHERE id = %s AND deleted_at IS NULL"
            cursor.execute(sql, (todo_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Todo not found"}), 404

            # Soft delete by setting deleted_at
            sql = "UPDATE todos SET deleted_at = %s WHERE id = %s"
            cursor.execute(sql, (datetime.now(), todo_id))
            connection.commit()
            return "", 204
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
