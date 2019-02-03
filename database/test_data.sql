
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS users
(
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    other_names VARCHAR(25) NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(10) NOT NULL UNIQUE,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    registered_on DATE DEFAULT CURRENT_TIMESTAMP,
    user_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

DO $$
BEGIN
     IF NOT EXISTS(SELECT 1 FROM pg_type WHERE typname ='incident_type') THEN

        CREATE TYPE incident_type AS ENUM
        ('red-flag','intervention');
    END IF;
    IF NOT EXISTS(SELECT 1 FROM pg_type WHERE typname ='incident_status') THEN

        CREATE TYPE incident_status AS ENUM
        ('Draft','Under Investigation','Resolved','Rejected');
    END IF;

    IF NOT EXISTS(SELECT 1 FROM pg_type WHERE typname ='geo_coordinates') THEN

        CREATE TYPE geo_coordinates AS
        (
            latitude DECIMAL(10,6),
            longitude DECIMAL(10,6)
        );
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS incidents
(
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    title VARCHAR(125) NOT NULL,
    comment TEXT NOT NULL,
    location geo_coordinates NULL,
    created_by uuid,
    created_on  DATE DEFAULT CURRENT_TIMESTAMP,
    status incident_status DEFAULT 'Draft',
    type incident_type NOT NULL,
    constraint fk_user_id
    foreign key (created_by)
    REFERENCES users (id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS incident_images(
    id SERIAL PRIMARY KEY,
    image_url VARCHAR(50),
    incident_id uuid,
    constraint fk_incident_id
    foreign key (incident_id)
    REFERENCES incidents (id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS incident_videos(
    id SERIAL PRIMARY KEY,
    video_url VARCHAR(50) DEFAULT '',
    incident_id uuid,
    constraint fk_incident_id
        foreign key (incident_id)
        REFERENCES incidents (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



CREATE OR REPLACE VIEW incident_view AS
SELECT id ,
       title ,
       comment ,
       location ,
       created_by ,
       user_name as owner ,
       created_on ,
       status ,
       type,
       COALESCE(videos,NULLIF('{}',videos)) as Videos,
       COALESCE(images,NULLIF('{}',images)) as Images
FROM
  (SELECT inc_tbl.id,
          inc_tbl.title,
          inc_tbl.comment,
          inc_tbl.location,
          inc_tbl.created_by,
          usr_tbl.user_name,
          inc_tbl.created_on,
          inc_tbl.status,
          inc_tbl.type
   FROM public.incidents inc_tbl
   LEFT JOIN public.users usr_tbl ON inc_tbl.created_by = usr_tbl.id) as A

LEFT JOIN
  (SELECT vids_tbl.incident_id as inc_vid_id,
          array_agg(vids_tbl.video_url) as videos
   from public.incident_videos vids_tbl
   group by vids_tbl.incident_id) AS videos_tbl on A.id = videos_tbl.inc_vid_id
LEFT JOIN
  (SELECT img_tbl.incident_id as inc_image_id,
          ARRAY_AGG(img_tbl.image_url) as images
   from incident_images img_tbl
   group by img_tbl.incident_id) AS Images_tbl on A.id = Images_tbl.inc_image_id;
