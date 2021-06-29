CREATE TABLE IF NOT EXISTS guild(
    GuildID integer NOT NULL,
    Prefix text DEFAULT "bt!",
    PRIMARY KEY (GuildID)
);

