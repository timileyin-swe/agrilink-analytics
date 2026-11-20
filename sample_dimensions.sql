INSERT INTO suppliers VALUES ('S001','Sample Farm A','Kano'),('S002','Sample Farm B','Kano'),('S003','Sample Farm C','Kaduna') ON CONFLICT DO NOTHING;
INSERT INTO buyers VALUES ('B001','Sample Processor A','Kano'),('B002','Sample Buyer B','Abuja') ON CONFLICT DO NOTHING;
INSERT INTO produce VALUES ('P001','Tomato'),('P002','Pepper') ON CONFLICT DO NOTHING;
