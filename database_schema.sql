-- =====================================================
-- REAL ESTATE APPLICATION DATABASE SCHEMA
-- =====================================================
-- This file contains all CREATE TABLE statements with
-- primary keys, foreign keys, and composite constraints
-- =====================================================

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
-- Purpose: Store user accounts (buyers, sellers, admins)
-- Primary Key: id
-- Foreign Keys: None
-- Composite Keys: None
-- Unique Constraints: email
-- =====================================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    phone VARCHAR(50),
    city VARCHAR(100),
    bio TEXT,
    avatar VARCHAR(255),

    -- Indexes for performance
    INDEX idx_users_email (email),
    INDEX idx_users_id (id)
);

-- =====================================================
-- 2. PROPERTIES TABLE
-- =====================================================
-- Purpose: Store property listings
-- Primary Key: id
-- Foreign Keys: owner_id -> users(id)
-- Composite Keys: None
-- =====================================================

CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL,
    image_path VARCHAR(255),

    -- Foreign Key Constraint
    CONSTRAINT fk_property_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Indexes for performance
    INDEX idx_properties_id (id),
    INDEX idx_properties_owner_id (owner_id)
);

-- =====================================================
-- 3. FAVORITES TABLE
-- =====================================================
-- Purpose: Store user's favorite properties
-- Primary Key: id
-- Foreign Keys: user_id -> users(id), property_id -> properties(id)
-- Composite Keys: UNIQUE(user_id, property_id)
-- =====================================================

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,

    -- Foreign Key Constraints
    CONSTRAINT fk_favorite_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_favorite_property
        FOREIGN KEY (property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Composite Unique Constraint
    -- Ensures one user can't favorite the same property twice
    CONSTRAINT uq_user_property
        UNIQUE (user_id, property_id),

    -- Indexes for performance
    INDEX idx_favorites_id (id),
    INDEX idx_favorites_user_id (user_id),
    INDEX idx_favorites_property_id (property_id)
);

-- =====================================================
-- 4. REVIEWS TABLE
-- =====================================================
-- Purpose: Store property reviews from users
-- Primary Key: id
-- Foreign Keys: property_id -> properties(id), user_id -> users(id)
-- Composite Keys: UNIQUE(user_id, property_id)
-- =====================================================

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,

    -- Foreign Key Constraints
    CONSTRAINT fk_review_property
        FOREIGN KEY (property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Composite Unique Constraint
    -- Ensures one user can only review a property once
    CONSTRAINT uq_user_review
        UNIQUE (user_id, property_id),

    -- Indexes for performance
    INDEX idx_reviews_id (id),
    INDEX idx_reviews_property_id (property_id),
    INDEX idx_reviews_user_id (user_id)
);

-- =====================================================
-- 5. INQUIRIES TABLE
-- =====================================================
-- Purpose: Store buyer inquiries about properties
-- Primary Key: id
-- Foreign Keys: property_id -> properties(id), buyer_id -> users(id)
-- Composite Keys: None
-- =====================================================

CREATE TABLE inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    buyer_name VARCHAR(255) NOT NULL,
    buyer_email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'replied', 'closed')),
    reply TEXT,

    -- Foreign Key Constraints
    CONSTRAINT fk_inquiry_property
        FOREIGN KEY (property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_inquiry_buyer
        FOREIGN KEY (buyer_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Indexes for performance
    INDEX idx_inquiries_id (id),
    INDEX idx_inquiries_property_id (property_id),
    INDEX idx_inquiries_buyer_id (buyer_id),
    INDEX idx_inquiries_status (status)
);

-- =====================================================
-- 6. APPOINTMENTS TABLE
-- =====================================================
-- Purpose: Store property viewing appointments
-- Primary Key: id
-- Foreign Keys: property_id -> properties(id), user_id -> users(id)
-- Composite Keys: None
-- =====================================================

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    visit_date VARCHAR(20) NOT NULL,  -- Format: "2026-06-15"
    visit_time VARCHAR(20) NOT NULL,  -- Format: "10:00 AM"
    note TEXT,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),

    -- Foreign Key Constraints
    CONSTRAINT fk_appointment_property
        FOREIGN KEY (property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_appointment_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Indexes for performance
    INDEX idx_appointments_id (id),
    INDEX idx_appointments_property_id (property_id),
    INDEX idx_appointments_user_id (user_id),
    INDEX idx_appointments_status (status),
    INDEX idx_appointments_date (visit_date)
);

-- =====================================================
-- SUMMARY OF DATABASE RELATIONSHIPS
-- =====================================================

/*
TABLE STRUCTURE SUMMARY:

1. USERS (Central table - no dependencies)
   - PK: id
   - UK: email

2. PROPERTIES (Depends on USERS)
   - PK: id
   - FK: owner_id -> users(id)

3. FAVORITES (Junction table - many-to-many relationship)
   - PK: id
   - FK: user_id -> users(id)
   - FK: property_id -> properties(id)
   - COMPOSITE UK: (user_id, property_id)

4. REVIEWS (Junction table with additional data)
   - PK: id
   - FK: property_id -> properties(id)
   - FK: user_id -> users(id)
   - COMPOSITE UK: (user_id, property_id)

5. INQUIRIES (Transactional table)
   - PK: id
   - FK: property_id -> properties(id)
   - FK: buyer_id -> users(id)

6. APPOINTMENTS (Transactional table)
   - PK: id
   - FK: property_id -> properties(id)
   - FK: user_id -> users(id)

RELATIONSHIP DIAGRAM:
                    users
                      |
                      | (1:N)
                      |
                  properties
                 /    |    \
        (N:M)   /     |     \   (1:N)
               /      |      \
         favorites  reviews  inquiries
                             appointments
*/
