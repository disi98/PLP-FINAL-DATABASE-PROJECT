CREATE DATABASE blog_cms;

USE blog_cms;

 
-- DROP existing objects if they exist
DROP TRIGGER IF EXISTS trg_user_id;
DROP TRIGGER IF EXISTS trg_author_id;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS hashtag;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS category;
DROP SEQUENCE IF EXISTS user_id_seq;
DROP SEQUENCE IF EXISTS author_id_seq;

-- 1) Create sequences for user and author IDs
CREATE SEQUENCE user_id_seq
  START WITH 1
  INCREMENT BY 1;
CREATE SEQUENCE author_id_seq
  START WITH 1
  INCREMENT BY 1;

-- 2) user table
CREATE TABLE `user` (
  id          VARCHAR(10)   NOT NULL UNIQUE,
  username    VARCHAR(15)   NOT NULL,
  firstName   VARCHAR(50)   NOT NULL,
  secondName  VARCHAR(50),
  otherName   VARCHAR(50),
  PRIMARY KEY (username)
) ENGINE=InnoDB
  COMMENT = 'Users with generated IDs user_01, user_02, ...';

-- Trigger to fill in user.id before insert
DELIMITER $$
CREATE TRIGGER trg_user_id
BEFORE INSERT ON `user`
FOR EACH ROW
BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN
    SET NEW.id = CONCAT(
      'user_',
      LPAD(nextval(user_id_seq), 2, '0')
    );
  END IF;
END$$
DELIMITER ;

-- 3) author table
CREATE TABLE author (
  id          VARCHAR(12)   NOT NULL UNIQUE,
  username    VARCHAR(15)   NOT NULL,
  `user`      VARCHAR(15)   NOT NULL,
  firstName   VARCHAR(50)   NOT NULL,
  secondName  VARCHAR(50),
  otherName   VARCHAR(50),
  nickName    VARCHAR(50),
  PRIMARY KEY (username),
  CONSTRAINT fk_author_user
    FOREIGN KEY (`user`)
    REFERENCES `user`(username)
    ON DELETE CASCADE
) ENGINE=InnoDB
  COMMENT = 'Authors linked to users with IDs author_01, author_02, ...';

-- Trigger to fill in author.id before insert
DELIMITER $$
CREATE TRIGGER trg_author_id
BEFORE INSERT ON author
FOR EACH ROW
BEGIN
  IF NEW.id IS NULL OR NEW.id = '' THEN
    SET NEW.id = CONCAT(
      'author_',
      LPAD(nextval(author_id_seq), 2, '0')
    );
  END IF;
END$$
DELIMITER ;

-- 4) category table
CREATE TABLE category (
  name        VARCHAR(50)   NOT NULL,
  PRIMARY KEY (name)
) ENGINE=InnoDB
  COMMENT = 'Post categories';

-- 5) hashtag table
CREATE TABLE hashtag (
  id          INT           NOT NULL AUTO_INCREMENT,
  name        VARCHAR(20)   NOT NULL,
  category    VARCHAR(50)   NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_hashtag_category
    FOREIGN KEY (category)
    REFERENCES category(name)
    ON DELETE RESTRICT
) ENGINE=InnoDB
  COMMENT = 'Hashtags assigned to categories';

-- 6) post table (fixed: ON DELETE RESTRICT to match NOT NULL)
CREATE TABLE post (
  id          INT           NOT NULL AUTO_INCREMENT,
  author      VARCHAR(15)   NOT NULL,
  category    VARCHAR(50)   NOT NULL,
  created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title       VARCHAR(200)  NOT NULL,
  body        TEXT,
  status      TINYINT(1)    NOT NULL DEFAULT 0,  -- 0 = draft, 1 = publish
  PRIMARY KEY (id),
  CONSTRAINT fk_post_author
    FOREIGN KEY (author)
    REFERENCES author(username)
    ON DELETE RESTRICT,
  CONSTRAINT fk_post_category
    FOREIGN KEY (category)
    REFERENCES category(name)
    ON DELETE RESTRICT
) ENGINE=InnoDB
  COMMENT = 'Posts with timestamp, title, body and draft/publish flag';



-- 7) Seed users
INSERT INTO `user` (username, firstName, secondName, otherName) VALUES
  ('alice',  'Alice',  'Anderson', NULL),
  ('bob',    'Bob',    NULL,        'Robertson'),
  ('carol',  'Carol',  'Clark',     'Marie');

-- 8) Seed authors (linked to users)
INSERT INTO author (username, `user`, firstName, secondName, otherName, nickName) VALUES
  ('auth_jdoe',   'alice', 'John',   'Doe',    NULL,    'jdoe'),
  ('auth_asmith', 'alice', 'Anna',   'Smith',  'L.',    NULL),
  ('auth_bjones', 'bob',   'Bill',   'Jones',  NULL,    'bj'),
  ('auth_ckent',  'carol', 'Clark',  'Kent',   NULL,    'super'),
  ('auth_lewis',  'bob',   'Lewis',  NULL,      'X.',    'lex');

-- 9) Seed categories
INSERT INTO category (name) VALUES
  ('technology'),
  ('agriculture'),
  ('education'),
  ('politics'),
  ('economics');

-- 10) Seed hashtags
INSERT INTO hashtag (name, category) VALUES
  -- technology
  ('AI',            'technology'),
  ('IoT',           'technology'),
  -- agriculture
  ('SmartFarming',  'agriculture'),
  ('AgriTech',      'agriculture'),
  -- education
  ('EdTech',        'education'),
  ('STEM',          'education'),
  -- politics
  ('Policy',        'politics'),
  ('Elections',     'politics'),
  -- economics
  ('MacroEcon',     'economics'),
  ('MicroEcon',     'economics');

-- 11) Seed posts (2 per category)
INSERT INTO post (author, category, title, body, status) VALUES
  -- technology
  ('auth_jdoe',   'technology', 'The Rise of AI',             'Exploring how AI is transforming industries today.',                 1),
  ('auth_asmith', 'technology', 'IoT in Modern Homes',        'A guide to connecting devices securely in your smart home.',         0),
  -- agriculture
  ('auth_bjones', 'agriculture','Precision Agriculture 101',  'An introduction to drones and sensors on the farm.',                 1),
  ('auth_lewis',  'agriculture','Vertical Farming Advances',  'How vertical farms are reshaping urban food production.',            0),
  -- education
  ('auth_ckent',  'education', 'Top 5 EdTech Platforms',     'Reviewing leading platforms that enhance remote learning.',         1),
  ('auth_jdoe',   'education', 'STEM Curriculum Trends',     'New approaches to teaching science and engineering in schools.',     0),
  -- politics
  ('auth_bjones', 'politics',  'Understanding Policy Making','An overview of how bills become law in different countries.',         1),
  ('auth_asmith', 'politics',  'Election Forecasts 2025',     'Analyzing polling data and predictive models for upcoming elections.',0),
  -- economics
  ('auth_ckent',  'economics','Global Macro Outlook',       'Assessing economic indicators for global growth trends.',           1),
  ('auth_lewis',  'economics','Intro to Microeconomics',    'Key concepts: supply, demand, and market equilibrium.',               0);
