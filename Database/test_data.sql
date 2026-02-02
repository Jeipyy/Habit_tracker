INSERT INTO users (username, email, password_hash)
VALUES ('Juan', 'juan123@gmail.com', 'hello12345'); 

INSERT INTO habits (user_id, name, description, goal_quantity, frequency_period) 
VALUES (1, 'Learn SQL', 'Build my habit tracker project', 1, 'daily');

INSERT INTO logs (habit_id, is_completed) 
VALUES (1, TRUE);

INSERT INTO habits (user_id, name, description, goal_quantity, frequency_period) 
VALUES 
(1, 'Python', 'Programar 1 hora al dia', 1, 'daily'),
(1, 'Leer', 'Leer 10 paginas', 1, 'daily'),
(1, 'Agua', 'Beber 2 litros', 1, 'daily');