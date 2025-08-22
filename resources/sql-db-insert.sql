INSERT INTO public.users(
	full_name, email, phone, password_hash, role, created_at)
	VALUES 
	('Alice Johnson', 'alice.johnson@example.com', '0211234567', 'password_1', 'Manager', NOW()),
('Bob Smith', 'bob.smith@example.com', '0212345678', 'password_1', 'Manager', NOW()),
('Charlie Brown', 'charlie.brown@example.com', '0213456789', 'password_1', 'Manager', NOW()),
('Dana White', 'dana.white@example.com', '0214567890', 'password_1', 'Manager', NOW()),
('Eli Green', 'eli.green@example.com', '0215678901', 'password_1', 'Manager', NOW());