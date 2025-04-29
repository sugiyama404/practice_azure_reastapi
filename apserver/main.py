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
        # Azure環境ではホスト名のみが提供されるため、必要に応じて完全なエンドポイントを構成
        db_host = os.environ.get('DB_HOST', 'mysql')
        # Azure MySQL Flexible ServerのFQDNの場合は.mysql.database.azure.comを追加
        if 'mysql-' in db_host and not db_host.endswith('.mysql.database.azure.com'):
            db_host = f"{db_host}.mysql.database.azure.com"

        logger.info(f"接続先データベース: {db_host}")

        connection = pymysql.connect(
            host=db_host,
            user=os.environ.get('DB_USER', 'goMySql1'),
            password=os.environ.get('DB_PASSWORD', 'goMySql1'),
            database=os.environ.get('DB_NAME', 'todoproject'),
            cursorclass=pymysql.cursors.DictCursor,
            # Azure MySQL Flexible Serverに接続する場合はSSL接続を使用
            ssl={'ssl': db_host.endswith('.mysql.database.azure.com')}
        )
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"MySQL接続エラー: {e}")
        raise
    except Exception as e:
        logger.error(f"データベース接続中に予期せぬエラーが発生: {e}")
        raise

def init_db():
    logger.info("データベースの初期化を確認中...")
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # todosテーブルが存在するか確認
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = 'todos'
            """, (os.environ.get('DB_NAME', 'todoproject'),))

            if cursor.fetchone()['COUNT(*)'] == 0:
                logger.info("todosテーブルが存在しません。テーブルを作成します。")
                # テーブルが存在しない場合は作成
                cursor.execute("""
                    CREATE TABLE todos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        content VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP NULL
                    )
                """)
                connection.commit()
                logger.info("todosテーブルの作成が完了しました。")
            else:
                logger.info("todosテーブルは既に存在します。")
    except Exception as e:
        logger.error(f"データベース初期化中にエラーが発生: {e}")
    finally:
        if connection:
            connection.close()

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
    init_db()  # アプリケーション起動時にデータベースの初期化を実行
    app.run(debug=True, host='0.0.0.0', port=8000)
