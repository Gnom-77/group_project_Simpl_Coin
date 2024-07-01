CREATE TABLE Employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    full_name TEXT, 
    role VARCHAR(100) NOT NULL,
    simpl_coin_count INT NOT NULL,
	chat_id VARCHAR(50)
);

CREATE TABLE conditions_for_receiving (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	technical_name TEXT
);

CREATE TABLE order_status (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE merch (
	id SERIAL PRIMARY KEY,
	name VARCHAR(150) NOT NULL,
	price INT NOT NULL,
	amount INT,
	technical_name TEXT
);


CREATE TABLE add_coins (
	id SERIAL PRIMARY KEY,
	employees_id INT NOT NULL,
	applicant_id INT NOT NULL,
	conditions_for_receiving_id INT NOT NULL,
	order_status_id INT NOT NULL,
	link TEXT,
	hr_comments TEXT,
	hr_id INT, 
	date DATE DEFAULT CURRENT_DATE,	

	FOREIGN KEY (employees_id) REFERENCES employees(id),
	FOREIGN KEY (applicant_id) REFERENCES employees(id),
	FOREIGN KEY (conditions_for_receiving_id) REFERENCES conditions_for_receiving(id),
	FOREIGN KEY (order_status_id) REFERENCES order_status(id),
	FOREIGN KEY (hr_id) REFERENCES employees(id)
);

CREATE TABLE buying_merch (
	id SERIAL PRIMARY KEY,
	employees_id INT NOT NULL,
	order_status_id INT NOT NULL,
	merch_id INT NOT NULL,
	hr_comments TEXT,
	hr_id INT,
	date DATE DEFAULT CURRENT_DATE,
	
	FOREIGN KEY (employees_id) REFERENCES employees(id),
	FOREIGN KEY (order_status_id) REFERENCES order_status(id),
	FOREIGN KEY (merch_id) REFERENCES merch(id),
	FOREIGN KEY (hr_id) REFERENCES employees(id)
	
);

INSERT INTO merch VALUES (1,'Набор наклеек Simpl', 1, 15, 'sticker');
INSERT INTO merch VALUES (2,'Значок', 1, 20, 'pin');
INSERT INTO merch VALUES (3,'Кружка', 4, 5, 'cup');
INSERT INTO merch VALUES (4,'Шапка', 4, 2, 'hat');
INSERT INTO merch VALUES (5,'Подставка под кружку', 4, 8, 'cupstand');
INSERT INTO merch VALUES (6,'Бейсболка/кепка', 4, 2, 'cap');
INSERT INTO merch VALUES (7,'Многофункциональная бандана', 4, 12, 'bandana');
INSERT INTO merch VALUES (8,'Рюкзак', 8, 2, 'backpack');
INSERT INTO merch VALUES (9,'Бутылка для воды', 8, 4, 'bottle');
INSERT INTO merch VALUES (10,'Футболка', 10, 2, 'tshirt');
INSERT INTO merch VALUES (11,'Powerbank', 12, 1, 'powerbank');
INSERT INTO merch VALUES (12,'Толстовка', 20, 1, 'hoody');


INSERT INTO conditions_for_receiving VALUES(1, 'Реализация улучшений работы команды 1-3 коина', 'improvements');
INSERT INTO conditions_for_receiving VALUES(2, 'Оптимизация работы направления и задач отдела 1-3 коина', 'optimization');
INSERT INTO conditions_for_receiving VALUES(3, 'Организация тимбилдингов 1-3 коина', 'team_building');
INSERT INTO conditions_for_receiving VALUES(4, 'Предложение идей для улучшения работы команды (только принятые идеи) 1-3 коина', 'offers');
INSERT INTO conditions_for_receiving VALUES(5, 'Работа наставником с практикантами 2 коина', 'trainee_one');
INSERT INTO conditions_for_receiving VALUES(6, 'Работа со стажером 10 коинов', 'trainee_two');
INSERT INTO conditions_for_receiving VALUES(7, 'Выступление с докладом на внешних конференциях с упоминанием компании, либо бренда 20 коинов', 'external');
INSERT INTO conditions_for_receiving VALUES(8, 'Доклад на внутренних митапах 10 коинов', 'internal');
INSERT INTO conditions_for_receiving VALUES(9, 'Получение сертификата об образовании с затраченным временем более 20 часов, 1 коин за 8 часов', 'certificate');
INSERT INTO conditions_for_receiving VALUES(10, 'Реализация идей по улучшению работы отдела 1-10, 1 коин за 3 сниппета', 'ideas');
INSERT INTO conditions_for_receiving VALUES(11, 'Статья на внешнем ресурсе с упоминанием компании/бренда 1 коинов за 2500', 'article');
INSERT INTO conditions_for_receiving VALUES(12, 'Интервью, комментарии (неопубликованный комментарий) 1 коин', 'interview_one');
INSERT INTO conditions_for_receiving VALUES(13, 'Интервью, комментарии (СМИ 2 эшелона) 3 коина', 'interview_two');
INSERT INTO conditions_for_receiving VALUES(14, 'Интервью, комментарии (СМИ 1 эшелона) 5 коинов', 'interview_three');
INSERT INTO conditions_for_receiving VALUES(15, 'Организация проведения обучений 1 коин за 5 участников', 'education');
INSERT INTO conditions_for_receiving VALUES(16, 'Организация мероприятия с участием сотрудников компании. 1 коин за 10 участников', 'events');
INSERT INTO conditions_for_receiving VALUES(17, 'Получение призового места на хакатоне 20 коинов', 'prize');


INSERT INTO order_status VALUES(1, 'Готов к выдаче');
INSERT INTO order_status VALUES(2, 'Обробатывается');
INSERT INTO order_status VALUES(3, 'Отклонён');
INSERT INTO order_status VALUES(4, 'Начислено');
INSERT INTO order_status VALUES(5, 'Получен');





