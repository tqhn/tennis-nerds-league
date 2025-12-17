CREATE TABLE dbo.box_assignments (
  box_assignment_id INTEGER PRIMARY KEY IDENTITY(1, 1),
  round_id INTEGER NOT NULL,
  box_id INTEGER NOT NULL,
  player_id INTEGER NOT NULL,
  -- Optionally, you could add a column to indicate the order of players within a box if needed for display
  -- order_in_box INTEGER,
  FOREIGN KEY (round_id) REFERENCES dbo.rounds(id),
  FOREIGN KEY (box_id) REFERENCES dbo.boxes(id),
  FOREIGN KEY (player_id) REFERENCES dbo.players(PlayerID),
  -- A player should only be in one box per round
  UNIQUE (round_id, player_id)
);
CREATE TABLE dbo.matches (
  id INTEGER PRIMARY KEY IDENTITY(1, 1),
  round_id INTEGER NOT NULL,
  box_id INTEGER NOT NULL,
  player1_id INTEGER NOT NULL,
  player2_id INTEGER NOT NULL,
  winner_id INTEGER,
  -- NULL if draw or not played yet
  is_draw BIT DEFAULT 0,
  -- 1 for true (draw), 0 for false
  player1_set1_games INTEGER,
  player2_set1_games INTEGER,
  player1_set2_games INTEGER,
  player2_set2_games INTEGER,
  player1_set3_games INTEGER,
  player2_set3_games INTEGER,
  played_on DATE,
  -- Date the match was played
  FOREIGN KEY (round_id) REFERENCES dbo.rounds(id),
  FOREIGN KEY (box_id) REFERENCES dbo.boxes(id),
  FOREIGN KEY (player1_id) REFERENCES dbo.players(PlayerID),
  FOREIGN KEY (player2_id) REFERENCES dbo.players(PlayerID),
  FOREIGN KEY (winner_id) REFERENCES dbo.players(PlayerID),
  -- Ensure player1 and player2 are different
  CHECK (player1_id <> player2_id),
  -- winner_id must be either player1_id or player2_id if not a draw
  CHECK (
    winner_id IS NULL
    OR winner_id = player1_id
    OR winner_id = player2_id
  )
);