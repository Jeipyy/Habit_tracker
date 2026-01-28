INSERT INTO users (username, email, password_hash)
VALUES ('Juan', 'juan123@gmail.com', 'hello12345'); 

-- Y este insert funcionará porque el user_id 1 vuelve a existir
INSERT INTO habits (user_id, name, description, goal_quantity, frequency_period) 
VALUES (1, 'Learn SQL', 'Build my habit tracker project', 1, 'daily');

INSERT INTO logs (habit_id, is_completed) 
VALUES (1, TRUE);