CREATE TABLE dbo.boxes (
  id INT IDENTITY(1, 1) PRIMARY KEY,
  box_name VARCHAR(50) NOT NULL UNIQUE,
  points_weight DECIMAL(5, 2) NULL
);
CREATE TABLE dbo.Players (
  PlayerID INT IDENTITY(1, 1) PRIMARY KEY,
  FirstName VARCHAR(50) NULL,
  LastName VARCHAR(50) NULL,
  SkillLevel INT NULL,
  Email VARCHAR(255) NULL,
  Phone_number VARCHAR(255) NULL,
  PasswordHash NVARCHAR(255) NULL,
  ResetToken NVARCHAR(255) NULL,
  ResetTokenExpiry DATETIME NULL
);
CREATE TABLE dbo.rounds (
  id INT IDENTITY(1, 1) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  signup_close_date DATE NULL,
  PrizeDescription NVARCHAR(500) NULL,
  SponsorID INT NULL,
  CONSTRAINT FK_Rounds_Sponsor FOREIGN KEY (SponsorID) REFERENCES dbo.Sponsors(SponsorID)
);
CREATE TABLE dbo.box_assignments (
  box_assignment_id INT IDENTITY(1, 1) PRIMARY KEY,
  round_id INT NOT NULL,
  box_id INT NOT NULL,
  player_id INT NOT NULL,
  CONSTRAINT UQ_Round_Player UNIQUE (round_id, player_id),
  FOREIGN KEY (round_id) REFERENCES dbo.rounds(id),
  FOREIGN KEY (box_id) REFERENCES dbo.boxes(id),
  FOREIGN KEY (player_id) REFERENCES dbo.Players(PlayerID)
);
CREATE TABLE dbo.matches (
  id INT IDENTITY(1, 1) PRIMARY KEY,
  round_id INT NOT NULL,
  box_id INT NOT NULL,
  player1_id INT NOT NULL,
  player2_id INT NOT NULL,
  winner_id INT NULL,
  is_draw BIT DEFAULT 0,
  player1_set1_games INT NULL,
  player2_set1_games INT NULL,
  player1_set2_games INT NULL,
  player2_set2_games INT NULL,
  player1_set3_games INT NULL,
  player2_set3_games INT NULL,
  played_on DATE NULL,
  Comments_Match_Summary NVARCHAR(MAX) NULL,
  -- Logic Constraints
  CHECK (player1_id <> player2_id),
  CHECK (
    winner_id IS NULL
    OR winner_id = player1_id
    OR winner_id = player2_id
  ),
  FOREIGN KEY (round_id) REFERENCES dbo.rounds(id),
  FOREIGN KEY (box_id) REFERENCES dbo.boxes(id),
  FOREIGN KEY (player1_id) REFERENCES dbo.Players(PlayerID),
  FOREIGN KEY (player2_id) REFERENCES dbo.Players(PlayerID),
  FOREIGN KEY (winner_id) REFERENCES dbo.Players(PlayerID)
);
CREATE TABLE dbo.players_ranking (
  ranking_id INT IDENTITY(1, 1) PRIMARY KEY,
  round_id INT NOT NULL,
  player_id INT NOT NULL,
  final_rank INT NULL,
  matches_played INT DEFAULT 0,
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  draws INT DEFAULT 0,
  points INT DEFAULT 0,
  CONSTRAINT UQ_Round_Player_Ranking UNIQUE (round_id, player_id),
  FOREIGN KEY (round_id) REFERENCES dbo.rounds(id),
  FOREIGN KEY (player_id) REFERENCES dbo.Players(PlayerID)
);
GO CREATE VIEW dbo.vw_CurrentStandings AS WITH CurrentRound AS (
    SELECT TOP 1 id AS RoundID,
      name AS RoundName,
      start_date,
      end_date
    FROM dbo.rounds
    WHERE start_date <= GETDATE()
    ORDER BY start_date DESC,
      id DESC
  ),
  PlayerMatchResults AS (
    SELECT CR.RoundID,
      CR.RoundName,
      B.id AS BoxID,
      B.box_name AS BoxName,
      P.PlayerID,
      P.FirstName + ' ' + P.LastName AS PlayerName,
      SUM(
        CASE
          WHEN M.winner_id = P.PlayerID THEN 1
          ELSE 0
        END
      ) AS Wins,
      SUM(
        CASE
          WHEN M.played_on IS NOT NULL
          AND M.winner_id <> P.PlayerID
          AND M.is_draw = 0 THEN 1
          ELSE 0
        END
      ) AS Losses,
      SUM(
        CASE
          WHEN M.is_draw = 1 THEN 1
          ELSE 0
        END
      ) AS Draws,
      COUNT(M.id) AS MatchesPlayed,
      SUM(
        CASE
          WHEN M.winner_id = P.PlayerID THEN 3
          WHEN M.is_draw = 1 THEN 1
          WHEN M.played_on IS NOT NULL THEN 1
          ELSE 0
        END
      ) AS Points
    FROM CurrentRound CR
      JOIN dbo.matches M ON CR.RoundID = M.round_id
      JOIN dbo.players P ON M.player1_id = P.PlayerID
      OR M.player2_id = P.PlayerID
      JOIN dbo.boxes B ON M.box_id = B.id
    WHERE M.played_on IS NOT NULL
    GROUP BY CR.RoundID,
      CR.RoundName,
      B.id,
      B.box_name,
      P.PlayerID,
      P.FirstName,
      P.LastName
  )
SELECT RoundName,
  BoxName,
  PlayerName,
  MatchesPlayed,
  Wins,
  Losses,
  Draws,
  Points,
  ROW_NUMBER() OVER (
    PARTITION BY BoxID
    ORDER BY Points DESC,
      Wins DESC,
      PlayerName ASC
  ) AS RankInBox
FROM PlayerMatchResults;
GO CREATE VIEW dbo.active_hours_summary AS
SELECT 'Social Sessions' AS activity_type,
  SUM(player_count * 150) AS total_minutes,
  SUM(player_count * 150) / 60.0 AS total_hours
FROM dbo.social_sessions
UNION ALL
SELECT 'Formal Matches' AS activity_type,
  COUNT(id) * 2 * 120,
  (COUNT(id) * 2 * 120) / 60.0
FROM dbo.matches
WHERE played_on IS NOT NULL;
GO