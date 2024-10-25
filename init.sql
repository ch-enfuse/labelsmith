-- Create the class_labels table
CREATE TABLE IF NOT EXISTS class_labels (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) UNIQUE NOT NULL
);

-- Create the records table
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    predicted_label VARCHAR(50) NOT NULL,
    validation_status BOOLEAN,
    corrected_label VARCHAR(50),
    FOREIGN KEY (corrected_label) REFERENCES class_labels(label)
);

-- Insert sample data into class_labels
INSERT INTO class_labels (label) VALUES 
('Cat'),
('Dog'),
('Bird'),
('Fish');

-- Insert sample data into records
INSERT INTO records (image_url, predicted_label, validation_status, corrected_label) VALUES 
('https://example.com/image1.jpg', 'Cat', NULL, NULL),
('https://example.com/image2.jpg', 'Dog', NULL, NULL),
('https://example.com/image3.jpg', 'Bird', NULL, NULL),
('https://example.com/image4.jpg', 'Fish', NULL, NULL);
