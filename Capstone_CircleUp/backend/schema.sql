-- =====================================================================
-- CircleUp — Database Schema (PostgreSQL)
-- =====================================================================
-- Full schema design: all 4 tables are created up front.
-- Week 1 wires endpoints for `users` and `activities`.
-- `participation_requests` endpoints land in Week 2.
-- `token_blacklist` supports server-side JWT logout from Day 1.
--
-- Design notes:
--   * Single user type — permissions are determined by activity.creator_id.
--   * activities.status is only ever written as 'open' or 'cancelled'.
--     'full' and 'completed' are derived lazily at read time.
--   * UNIQUE(activity_id, user_id) prevents duplicate participation requests.
-- =====================================================================

CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(120)  NOT NULL,
    email           VARCHAR(255)  NOT NULL,
    password_hash   VARCHAR(255)  NOT NULL,
    phone_number    VARCHAR(30)   NOT NULL,
    city            VARCHAR(120),
    bio             VARCHAR(1000),
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);


CREATE TABLE activities (
    id                  SERIAL PRIMARY KEY,
    creator_id          INTEGER       NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title               VARCHAR(200)  NOT NULL,
    description         VARCHAR(2000),
    category            VARCHAR(100)  NOT NULL,
    location            VARCHAR(200)  NOT NULL,
    date                DATE          NOT NULL,
    "time"              TIME          NOT NULL,
    max_participants    INTEGER       NOT NULL,
    status              VARCHAR(20)   NOT NULL DEFAULT 'open',
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ   NOT NULL DEFAULT now(),

    CONSTRAINT ck_max_participants_positive CHECK (max_participants > 0)
);
CREATE INDEX ix_activities_id ON activities (id);
CREATE INDEX ix_activities_creator_id ON activities (creator_id);
CREATE INDEX ix_activities_category ON activities (category);
CREATE INDEX ix_activities_location ON activities (location);
CREATE INDEX ix_activities_date ON activities (date);


CREATE TABLE participation_requests (
    id              SERIAL PRIMARY KEY,
    activity_id     INTEGER       NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    user_id         INTEGER       NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status          VARCHAR(20)   NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),

    CONSTRAINT uq_one_request_per_user_per_activity UNIQUE (activity_id, user_id)
);
CREATE INDEX ix_participation_requests_id ON participation_requests (id);
CREATE INDEX ix_participation_requests_activity_id ON participation_requests (activity_id);
CREATE INDEX ix_participation_requests_user_id ON participation_requests (user_id);


CREATE TABLE token_blacklist (
    id               SERIAL PRIMARY KEY,
    jti              VARCHAR(36)   NOT NULL,
    blacklisted_at   TIMESTAMPTZ   NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ix_token_blacklist_jti ON token_blacklist (jti);
CREATE INDEX ix_token_blacklist_id ON token_blacklist (id);