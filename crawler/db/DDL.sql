--
-- File generated with SQLiteStudio v3.1.1 on 周四 3月 8 22:13:06 2018
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Goods
CREATE TABLE Goods (Id INTEGER PRIMARY KEY, Name TEXT, ShopId TEXT NOT NULL REFERENCES Shops (ShopId), GoodId TEXT NOT NULL UNIQUE, CreationDate DATETIME, MainPic TEXT, active BOOLEAN DEFAULT (0));

-- Table: Records
CREATE TABLE Records (Id INTEGER PRIMARY KEY, date DATE NOT NULL, GoodId TEXT NOT NULL REFERENCES Goods (GoodId), sales_30 integer, fav_cnt integer, view_cnt integer, review_cnt integer, UNIQUE (date, GoodId));

-- Table: Shops
CREATE TABLE Shops (Id INTEGER PRIMARY KEY, Name TEXT, Link TEXT, ShopId TEXT NOT NULL UNIQUE, CreationDate DATETIME DEFAULT (datetime('now', 'localtime')), active BOOLEAN DEFAULT (0));

-- Index: Goods_idx
CREATE INDEX Goods_idx ON Goods (Id, ShopId, GoodId, active);

-- Index: Records_idx
CREATE INDEX Records_idx ON Records (Id, date, GoodId);

-- Index: Shops_idx
CREATE INDEX Shops_idx ON Shops (Id, Name, ShopId);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
