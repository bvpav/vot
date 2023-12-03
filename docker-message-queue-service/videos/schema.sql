-- PostgreSQL schema

create table if not exists videos (
    id serial primary key,
    title text,
    description text,
    url text not null,
    file_url text,
    created_at timestamp not null default now()
)