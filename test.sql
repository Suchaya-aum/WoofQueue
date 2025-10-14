INSERT INTO app_size (size, price) VALUES
('S', 250.00),
('M', 300.00),
('L', 350.00),
('XL', 400.00),
('XXL', 450.00);

INSERT INTO app_hairtype (hair, price) VALUES
('Long Hair', 200.00),
('Hair Born', 150.00),
('Normal', 100.00);

-- INSERT INTO app_service (service_name, duration, price, staff_id) VALUES
-- ('Basic Bath & Dry', 45, 300.00, 2),
-- ('Full Grooming', 120, 600.00, 2),
-- ('Nail Trim', 15, 100.00, 3),
-- ('Ear Cleaning', 20, 150.00, 3),
-- ('Spa & Conditioning', 60, 450.00, 3);

INSERT INTO app_staff_profile (user_id, first_name, last_name, phone)
VALUES
    (1, 'Suchaya', 'Rattanapong', '0812345678'),
    (2, 'Sirawit', 'Chantip', '0898765432'),
    (3, 'Napas', 'Kittisak', '0861122334');
