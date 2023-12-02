-- init.sql

-- Créez la table mytable
CREATE TABLE mytable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT
);

-- Ajoutez des données à la table mytable
INSERT INTO mytable (name, age) VALUES
    ('John Doe', 30),
    ('Jane Doe', 25),
    ('Bob Smith', 40);
