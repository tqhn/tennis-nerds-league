-- In this SQL file, write (and comment!) the schema of your database, including the CREATE TABLE, CREATE INDEX, CREATE VIEW, etc. statements that compose it

-- Players table
CREATE TABLE "players" (
  "id" INT,
  "name" TEXT NOT NULL,
  "skill_level" TEXT,
  "contact" TEXT,
  PRIMARY KEY ("id")
);

-- Rounds table
CREATE TABLE "rounds" (
  "id" INT,
  "name" TEXT NOT NULL,
  "start_date" DATE,
  "end_date" DATE,
  PRIMARY KEY ("id")
);

-- Boxes table
CREATE TABLE "boxes" (
  "id" INT,
  "box_name" NOT NULL CHECK("box_name" IN ('box A', 'box B', 'box C', 'box D')),
  PRIMARY KEY ("id")
);

-- Matches table
CREATE TABLE "matches" (
  "id" INT,
  "round_id" INT,
  "box_id" INT,
  "player1_id" INT,
  "player2_id" INT,
  "winner_id" INT,
  "player1_set1_games" TEXT,
  "player2_set1_games" TEXT,
  "player1_set2_games" TEXT,
  "player2_set2_games" TEXT,
  "player1_set3_games" TEXT,
  "player2_set3_games" TEXT,
  "played_on" DATE,
  FOREIGN KEY("round_id") REFERENCES rounds("id"),
  FOREIGN KEY("player1_id") REFERENCES players("id"),
  FOREIGN KEY("player2_id") REFERENCES players("id"),
  FOREIGN KEY("winner_id") REFERENCES players("id")
);



-- Box Assignment Table
CREATE TABLE "box_assignments" (
  "box_assignment_id" INT,
  "box_id" INT,
  "round_id" INT,
  "player_id" INT,
  PRIMARY KEY("box_assignment_id"),
  FOREIGN KEY("box_id") REFERENCES boxes("id"),
  FOREIGN KEY("round_id") REFERENCES rounds("id"),
  FOREIGN KEY("player_id") REFERENCES players("id")
);

-- Players Ranking table
CREATE TABLE "players_ranking" (
    "ranking_id" INT,
    "player_id" INT,
    "round_id" INT,
    "final_rank" INT,
    "matches_played" INT,
    "wins" INT,
    "losses" INT,
    "draws" INT,
    "points" INT,
    PRIMARY KEY ("ranking_id"),
    FOREIGN KEY("player_id") REFERENCES players("id"),
    FOREIGN KEY("round_id") REFERENCES rounds("id")
);
