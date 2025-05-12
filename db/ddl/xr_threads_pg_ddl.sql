create schema if NOT EXISTS xr_threads;

CREATE table if not exists xr_threads.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name VARCHAR(100),
    bio TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);


CREATE table if not EXISTS xr_threads.blog_posts (
    post_id SERIAL PRIMARY KEY,
    author_id INT NOT NULL REFERENCES xr_threads.users(user_id),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE table if not exists xr_threads.comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL REFERENCES xr_threads.blog_posts(post_id) ON DELETE CASCADE,
    author_id INT NOT NULL REFERENCES xr_threads.users(user_id),
    parent_comment_id INT REFERENCES xr_threads.comments(comment_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);



-- 4. Tags table xr_threads.& Post-Tag Link Table

CREATE table if not exists xr_threads.tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE table if not exists xr_threads.post_tags (
    post_id INT NOT NULL REFERENCES xr_threads.blog_posts(post_id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES xr_threads.tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);


--5. PostMetadata table xr_threads.(for analytics later)

CREATE table if not exists xr_threads.post_metadata (
    post_id INT PRIMARY KEY REFERENCES xr_threads.blog_posts(post_id) ON DELETE CASCADE,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    last_viewed_at TIMESTAMPTZ,
    last_liked_at TIMESTAMPTZ
);



CREATE table if not exists xr_threads.engagements (
    engagement_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL REFERENCES xr_threads.blog_posts(post_id) ON DELETE CASCADE,
    user_id INT REFERENCES xr_threads.users(user_id),
    engagement_type VARCHAR(20) NOT NULL, -- e.g., 'view', 'like', 'share'
    engagement_time TIMESTAMPTZ DEFAULT NOW()
);
