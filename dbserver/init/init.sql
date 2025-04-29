DROP TABLE IF EXISTS todos;

CREATE TABLE todos
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT DEFAULT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at datetime DEFAULT NULL
);

INSERT INTO todos (content) VALUES ("Nagaoka");
INSERT INTO todos (content) VALUES ("Tanaka");
INSERT INTO todos (content) VALUES ("Yamamoto");
INSERT INTO todos (content) VALUES ("Kawasaki");
INSERT INTO todos (content) VALUES ("Kudo");
