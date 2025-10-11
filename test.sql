BEGIN;

-- ──────────────── USERS ────────────────
INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
VALUES
('customer1', 'Alice', 'Wong', 'customer1@example.com', 'hU;_*-b82ju7', FALSE, TRUE, FALSE, NULL, NOW()),
('staff1', 'Gina', 'Lee', 'staff1@example.com', 'hU;_*-b82ju7', TRUE, TRUE, FALSE, NULL, NOW())
ON CONFLICT (username) DO NOTHING;

-- ──────────────── SIZE ────────────────
INSERT INTO app_size (size, price)
VALUES ('M', 400.00)
ON CONFLICT DO NOTHING;

-- ──────────────── HAIR TYPE ────────────────
INSERT INTO app_hairtype (hair, price)
VALUES ('Normal', 50.00)
ON CONFLICT DO NOTHING;

-- ──────────────── SERVICE ────────────────
INSERT INTO app_service (service_name, duration, price, staff_id)
SELECT 'Full Grooming', 90, 600.00, u.id
FROM auth_user u WHERE u.username='staff1'
ON CONFLICT DO NOTHING;

-- ──────────────── PET ────────────────
INSERT INTO app_pet (owner_id, size_id, hair_type_id, pet_name, behavior_note)
SELECT u.id, s.id, h.id, 'Bella', 'Friendly small dog'
FROM auth_user u, app_size s, app_hairtype h
WHERE u.username='customer1' AND s.size='M' AND h.hair='Normal'
ON CONFLICT DO NOTHING;

-- ──────────────── APPOINTMENT ────────────────
INSERT INTO app_appointment (pet_id_id, created_at, appointment_time, finish_time, status)
SELECT p.id, NOW(), '2025-10-15 10:00:00+07', '2025-10-15 11:30:00+07', 'D'
FROM app_pet p
JOIN auth_user u ON u.id=p.owner_id
WHERE u.username='customer1' AND p.pet_name='Bella'
ON CONFLICT DO NOTHING;

-- ──────────────── M2M APPOINTMENT ↔ SERVICE ────────────────
INSERT INTO app_appointment_service (appointment_id, service_id)
SELECT a.id, s.id
FROM app_appointment a, app_service s, app_pet p, auth_user u
WHERE a.pet_id_id=p.id AND p.pet_name='Bella' AND u.id=p.owner_id AND u.username='customer1'
  AND s.service_name='Full Grooming'
ON CONFLICT DO NOTHING;

COMMIT;
