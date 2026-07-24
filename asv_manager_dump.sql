--
-- PostgreSQL database dump
--

\restrict ev7X6X4oRcAhxCA9AeKg5sFhXQHC3WbYBSCSaEY7ioqX3eEbmz4hjhZdBla7wH8

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departments (
    department_id bigint NOT NULL,
    name character varying(100) NOT NULL,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: departments_department_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.departments_department_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: departments_department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.departments_department_id_seq OWNED BY public.departments.department_id;


--
-- Name: facilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facilities (
    facility_id bigint NOT NULL,
    name character varying(150) NOT NULL,
    address character varying(250),
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: facilities_facility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.facilities_facility_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: facilities_facility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.facilities_facility_id_seq OWNED BY public.facilities.facility_id;


--
-- Name: games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.games (
    game_id bigint NOT NULL,
    season_id bigint NOT NULL,
    team_id bigint NOT NULL,
    place_id bigint,
    round_number integer,
    game_date date NOT NULL,
    start_time time without time zone,
    end_time time without time zone,
    opponent character varying(150) NOT NULL,
    home_away character varying(20) NOT NULL,
    game_type character varying(50) DEFAULT 'Meisterschaftsspiel'::character varying NOT NULL,
    status character varying(30) DEFAULT 'aktiv'::character varying NOT NULL,
    notes text,
    source_file character varying(250),
    source_sheet character varying(100),
    source_row integer,
    source_key character varying(150),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_game_home_away CHECK (((home_away)::text = ANY ((ARRAY['Heim'::character varying, 'Auswärts'::character varying, 'Neutral'::character varying])::text[])))
);


--
-- Name: games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.games ALTER COLUMN game_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.games_game_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: import_batches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.import_batches (
    import_batch_id bigint NOT NULL,
    import_type character varying(50) NOT NULL,
    source_file character varying(250) NOT NULL,
    started_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    finished_at timestamp without time zone,
    rows_read integer DEFAULT 0 NOT NULL,
    rows_created integer DEFAULT 0 NOT NULL,
    rows_updated integer DEFAULT 0 NOT NULL,
    rows_skipped integer DEFAULT 0 NOT NULL,
    rows_failed integer DEFAULT 0 NOT NULL,
    status character varying(30) DEFAULT 'gestartet'::character varying NOT NULL,
    report text
);


--
-- Name: import_batches_import_batch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.import_batches ALTER COLUMN import_batch_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.import_batches_import_batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: memberships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memberships (
    membership_id bigint NOT NULL,
    person_id bigint NOT NULL,
    season_id bigint NOT NULL,
    status character varying(30) DEFAULT 'aktiv'::character varying NOT NULL,
    joined_on date,
    left_on date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: memberships_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.memberships ALTER COLUMN membership_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.memberships_membership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: persons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.persons (
    person_id bigint NOT NULL,
    external_member_id integer,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    birth_date date,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    gender character varying(20),
    mobile character varying(50),
    email character varying(255),
    player_pass_number character varying(100),
    entry_date date,
    exit_date date,
    status character varying(30),
    note text
);


--
-- Name: persons_person_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.persons ALTER COLUMN person_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.persons_person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: places; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.places (
    place_id bigint NOT NULL,
    name character varying(150) NOT NULL,
    address character varying(250),
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    facility_id bigint,
    training_zones integer DEFAULT 1 NOT NULL
);


--
-- Name: places_place_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.places ALTER COLUMN place_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.places_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: seasons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.seasons (
    season_id bigint NOT NULL,
    name character varying(20) NOT NULL,
    start_date date,
    end_date date,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: seasons_season_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.seasons ALTER COLUMN season_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.seasons_season_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: team_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_members (
    team_member_id bigint NOT NULL,
    team_id bigint NOT NULL,
    person_id bigint NOT NULL,
    role character varying(30) DEFAULT 'Spieler'::character varying NOT NULL,
    valid_from date,
    valid_until date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: team_members_team_member_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.team_members ALTER COLUMN team_member_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.team_members_team_member_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    team_id bigint NOT NULL,
    season_id bigint NOT NULL,
    name character varying(50) NOT NULL,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: teams_team_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.teams ALTER COLUMN team_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.teams_team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: departments department_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments ALTER COLUMN department_id SET DEFAULT nextval('public.departments_department_id_seq'::regclass);


--
-- Name: facilities facility_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities ALTER COLUMN facility_id SET DEFAULT nextval('public.facilities_facility_id_seq'::regclass);


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.departments (department_id, name, active, created_at, updated_at) FROM stdin;
1	Nachwuchs	t	2026-07-22 13:43:59.522416	2026-07-22 13:43:59.522416
2	Kampfmannschaft	t	2026-07-22 13:43:59.522416	2026-07-22 13:43:59.522416
3	Frauen	t	2026-07-22 13:43:59.522416	2026-07-22 13:43:59.522416
4	Hauptplatz	t	2026-07-23 08:22:08.648436	2026-07-23 08:22:08.648436
5	Trainingsplatz	t	2026-07-23 08:22:33.464577	2026-07-23 08:22:33.464577
6	Kleiner Platz	f	2026-07-23 08:28:33.30545	2026-07-23 08:32:29.49041
\.


--
-- Data for Name: facilities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.facilities (facility_id, name, address, active, created_at, updated_at) FROM stdin;
1	Sportplatz Neufeld	Fürsorgeheimgasse 4, 2491 Neufeld an der Leitha	t	2026-07-23 12:29:40.625861	2026-07-23 14:05:50.712862
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.games (game_id, season_id, team_id, place_id, round_number, game_date, start_time, end_time, opponent, home_away, game_type, status, notes, source_file, source_sheet, source_row, source_key, created_at, updated_at) FROM stdin;
2	1	1	1	1	2026-09-05	10:00:00	11:30:00	TESTGEGNER	Heim	Testspiel	Aktiv	Testeintrag für GameRepository	test_game_insert.py	TEST	1	TEST-U10-2026-09-05-1000	2026-07-23 19:14:26.078757	2026-07-23 19:14:26.078757
140	1	3	\N	\N	2026-06-26	16:00:00	17:30:00	SK Rapid Wien	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	2	1|U15|2026-06-26 00:00:00|16:00:00|SK Rapid Wien	2026-07-23 20:21:46.466384	2026-07-23 20:21:46.466384
141	1	4	\N	\N	2026-06-26	18:00:00	19:45:00	SK Rapid Wien	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	3	1|U16|2026-06-26 00:00:00|18:00:00|SK Rapid Wien	2026-07-23 20:21:47.141743	2026-07-23 20:21:47.141743
142	1	5	\N	\N	2026-07-10	19:00:00	20:45:00	Neudörfl	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	4	1|KM|2026-07-10 00:00:00|19:00:00|Neudörfl	2026-07-23 20:21:47.144881	2026-07-23 20:21:47.144881
143	1	5	\N	\N	2026-07-17	19:00:00	20:45:00	Rohrbach	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	5	1|KM|2026-07-17 00:00:00|19:00:00|Rohrbach	2026-07-23 20:21:47.148238	2026-07-23 20:21:47.148238
144	1	5	\N	\N	2026-07-24	19:30:00	21:15:00	Sommerein	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	6	1|KM|2026-07-24 00:00:00|19:30:00|Sommerein	2026-07-23 20:21:47.151618	2026-07-23 20:21:47.151618
145	1	6	\N	\N	2026-07-31	17:00:00	18:45:00	Admira Wiener Neustadt	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	7	1|U23|2026-07-31 00:00:00|17:00:00|Admira Wiener Neustadt	2026-07-23 20:21:47.155212	2026-07-23 20:21:47.155212
146	1	5	\N	\N	2026-08-01	17:30:00	19:15:00	Kittsee	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	8	1|KM|2026-08-01 00:00:00|17:30:00|Kittsee	2026-07-23 20:21:47.158549	2026-07-23 20:21:47.158549
147	1	4	\N	\N	2026-08-02	10:30:00	12:15:00	Theresienfeld	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	9	1|U16|2026-08-02 00:00:00|10:30:00|Theresienfeld	2026-07-23 20:21:47.161999	2026-07-23 20:21:47.161999
148	1	5	\N	\N	2026-08-07	19:00:00	20:45:00	Bad Fischau	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	10	1|KM|2026-08-07 00:00:00|19:00:00|Bad Fischau	2026-07-23 20:21:47.165499	2026-07-23 20:21:47.165499
149	1	4	\N	\N	2026-08-09	11:00:00	12:45:00	Wiener Neudorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	11	1|U16|2026-08-09 00:00:00|11:00:00|Wiener Neudorf	2026-07-23 20:21:47.168647	2026-07-23 20:21:47.168647
150	1	2	\N	\N	2026-08-09	15:00:00	16:30:00	Vienna U13	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	12	1|U14|2026-08-09 00:00:00|15:00:00|Vienna U13	2026-07-23 20:21:47.172573	2026-07-23 20:21:47.172573
151	1	5	\N	\N	2026-07-14	19:30:00	21:15:00	Pöttsching	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	13	1|KM|2026-07-14 00:00:00|19:30:00|Pöttsching	2026-07-23 20:21:47.176133	2026-07-23 20:21:47.176133
152	1	4	\N	\N	2026-08-23	10:00:00	11:45:00	Laxenburg	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	14	1|U16|2026-08-23 00:00:00|10:00:00|Laxenburg	2026-07-23 20:21:47.179527	2026-07-23 20:21:47.179527
153	1	4	\N	\N	2026-08-26	10:00:00	11:45:00	Traiskirchen	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	15	1|U16|2026-08-26 00:00:00|10:00:00|Traiskirchen	2026-07-23 20:21:47.182658	2026-07-23 20:21:47.182658
154	1	4	\N	\N	2026-08-30	10:30:00	12:15:00	SPG Theresienfeld	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	16	1|U16|2026-08-30 00:00:00|10:30:00|SPG Theresienfeld	2026-07-23 20:21:47.186129	2026-07-23 20:21:47.186129
155	1	5	\N	\N	2027-02-27	12:00:00	13:45:00	Bad Erlach	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	17	1|KM|2027-02-27 00:00:00|12:00:00|Bad Erlach	2026-07-23 20:21:47.189229	2026-07-23 20:21:47.189229
156	1	5	\N	\N	2026-08-16	17:30:00	19:15:00	Kittsee	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	18	1|KM|2026-08-16 00:00:00|17:30:00|Kittsee	2026-07-23 20:21:47.192751	2026-07-23 20:21:47.192751
157	1	5	\N	\N	2026-08-21	20:00:00	21:45:00	Deutsch Jahrndorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	19	1|KM|2026-08-21 00:00:00|20:00:00|Deutsch Jahrndorf	2026-07-23 20:21:47.196097	2026-07-23 20:21:47.196097
158	1	5	\N	\N	2026-08-29	18:00:00	19:45:00	Tadten	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	20	1|KM|2026-08-29 00:00:00|18:00:00|Tadten	2026-07-23 20:21:47.199213	2026-07-23 20:21:47.199213
159	1	5	\N	\N	2026-09-05	16:30:00	18:15:00	Mönchhof	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	21	1|KM|2026-09-05 00:00:00|16:30:00|Mönchhof	2026-07-23 20:21:47.202298	2026-07-23 20:21:47.202298
160	1	5	\N	\N	2026-09-11	19:30:00	21:15:00	Winden	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	22	1|KM|2026-09-11 00:00:00|19:30:00|Winden	2026-07-23 20:21:47.205751	2026-07-23 20:21:47.205751
161	1	5	\N	\N	2026-09-19	16:00:00	17:45:00	Gattendorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	23	1|KM|2026-09-19 00:00:00|16:00:00|Gattendorf	2026-07-23 20:21:47.209203	2026-07-23 20:21:47.209203
162	1	5	\N	\N	2026-09-26	18:00:00	19:45:00	Wallern	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	24	1|KM|2026-09-26 00:00:00|18:00:00|Wallern	2026-07-23 20:21:47.212462	2026-07-23 20:21:47.212462
163	1	5	\N	\N	2026-10-02	19:00:00	20:45:00	Siegendorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	25	1|KM|2026-10-02 00:00:00|19:00:00|Siegendorf	2026-07-23 20:21:47.215563	2026-07-23 20:21:47.215563
164	1	5	\N	\N	2026-10-09	19:30:00	21:15:00	Wimpassing	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	26	1|KM|2026-10-09 00:00:00|19:30:00|Wimpassing	2026-07-23 20:21:47.219936	2026-07-23 20:21:47.219936
165	1	5	\N	\N	2026-10-16	19:30:00	21:15:00	Hornstein	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	27	1|KM|2026-10-16 00:00:00|19:30:00|Hornstein	2026-07-23 20:21:47.22354	2026-07-23 20:21:47.22354
166	1	5	\N	\N	2026-10-24	17:00:00	18:45:00	Gols	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	28	1|KM|2026-10-24 00:00:00|17:00:00|Gols	2026-07-23 20:21:47.226992	2026-07-23 20:21:47.226992
167	1	5	\N	\N	2026-10-31	18:00:00	19:45:00	Illmitz	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	29	1|KM|2026-10-31 00:00:00|18:00:00|Illmitz	2026-07-23 20:21:47.230065	2026-07-23 20:21:47.230065
168	1	5	\N	\N	2026-11-07	16:30:00	18:15:00	Andau	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	30	1|KM|2026-11-07 00:00:00|16:30:00|Andau	2026-07-23 20:21:47.23321	2026-07-23 20:21:47.23321
169	1	6	\N	\N	2026-08-16	15:30:00	17:15:00	Kittsee	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	31	1|U23|2026-08-16 00:00:00|15:30:00|Kittsee	2026-07-23 20:21:47.237065	2026-07-23 20:21:47.237065
170	1	6	\N	\N	2026-08-21	18:00:00	19:45:00	Deutsch Jahrndorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	32	1|U23|2026-08-21 00:00:00|18:00:00|Deutsch Jahrndorf	2026-07-23 20:21:47.241252	2026-07-23 20:21:47.241252
171	1	6	\N	\N	2026-08-29	16:00:00	17:45:00	Tadten	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	33	1|U23|2026-08-29 00:00:00|16:00:00|Tadten	2026-07-23 20:21:47.244877	2026-07-23 20:21:47.244877
172	1	6	\N	\N	2026-09-05	14:30:00	16:15:00	Mönchhof	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	34	1|U23|2026-09-05 00:00:00|14:30:00|Mönchhof	2026-07-23 20:21:47.248207	2026-07-23 20:21:47.248207
173	1	6	\N	\N	2026-09-11	17:30:00	19:15:00	Winden	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	35	1|U23|2026-09-11 00:00:00|17:30:00|Winden	2026-07-23 20:21:47.251535	2026-07-23 20:21:47.251535
174	1	6	\N	\N	2026-09-19	14:00:00	15:45:00	Gattendorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	36	1|U23|2026-09-19 00:00:00|14:00:00|Gattendorf	2026-07-23 20:21:47.255109	2026-07-23 20:21:47.255109
175	1	6	\N	\N	2026-09-26	16:00:00	17:45:00	Wallern	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	37	1|U23|2026-09-26 00:00:00|16:00:00|Wallern	2026-07-23 20:21:47.258628	2026-07-23 20:21:47.258628
176	1	6	\N	\N	2026-10-03	17:00:00	18:45:00	Siegendorf	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	38	1|U23|2026-10-03 00:00:00|17:00:00|Siegendorf	2026-07-23 20:21:47.262443	2026-07-23 20:21:47.262443
177	1	6	\N	\N	2026-10-09	17:30:00	19:15:00	Wimpassing	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	39	1|U23|2026-10-09 00:00:00|17:30:00|Wimpassing	2026-07-23 20:21:47.265606	2026-07-23 20:21:47.265606
178	1	6	\N	\N	2026-10-16	17:30:00	19:15:00	Hornstein	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	40	1|U23|2026-10-16 00:00:00|17:30:00|Hornstein	2026-07-23 20:21:47.268774	2026-07-23 20:21:47.268774
179	1	6	\N	\N	2026-10-24	15:00:00	16:45:00	Gols	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	41	1|U23|2026-10-24 00:00:00|15:00:00|Gols	2026-07-23 20:21:47.27291	2026-07-23 20:21:47.27291
180	1	6	\N	\N	2026-10-31	16:00:00	17:45:00	Illmitz	Auswärts	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	42	1|U23|2026-10-31 00:00:00|16:00:00|Illmitz	2026-07-23 20:21:47.276421	2026-07-23 20:21:47.276421
181	1	6	\N	\N	2026-11-07	14:30:00	16:15:00	Andau	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	43	1|U23|2026-11-07 00:00:00|14:30:00|Andau	2026-07-23 20:21:47.279863	2026-07-23 20:21:47.279863
182	1	4	\N	\N	2026-01-01	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	44	1|U16|2026-01-01 00:00:00|00:00:00|0	2026-07-23 20:21:47.28298	2026-07-23 20:21:47.28298
183	1	4	\N	\N	2026-01-02	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	45	1|U16|2026-01-02 00:00:00|00:00:00|0	2026-07-23 20:21:47.286046	2026-07-23 20:21:47.286046
184	1	4	\N	\N	2026-01-03	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	46	1|U16|2026-01-03 00:00:00|00:00:00|0	2026-07-23 20:21:47.288662	2026-07-23 20:21:47.288662
185	1	4	\N	\N	2026-01-04	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	47	1|U16|2026-01-04 00:00:00|00:00:00|0	2026-07-23 20:21:47.291623	2026-07-23 20:21:47.291623
186	1	4	\N	\N	2026-01-05	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	48	1|U16|2026-01-05 00:00:00|00:00:00|0	2026-07-23 20:21:47.294712	2026-07-23 20:21:47.294712
187	1	4	\N	\N	2026-01-06	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	49	1|U16|2026-01-06 00:00:00|00:00:00|0	2026-07-23 20:21:47.297512	2026-07-23 20:21:47.297512
188	1	4	\N	\N	2026-01-07	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	50	1|U16|2026-01-07 00:00:00|00:00:00|0	2026-07-23 20:21:47.300365	2026-07-23 20:21:47.300365
189	1	4	\N	\N	2026-01-08	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	51	1|U16|2026-01-08 00:00:00|00:00:00|0	2026-07-23 20:21:47.304425	2026-07-23 20:21:47.304425
190	1	4	\N	\N	2026-01-09	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	52	1|U16|2026-01-09 00:00:00|00:00:00|0	2026-07-23 20:21:47.307513	2026-07-23 20:21:47.307513
191	1	4	\N	\N	2026-01-10	00:00:00	01:45:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	53	1|U16|2026-01-10 00:00:00|00:00:00|0	2026-07-23 20:21:47.310594	2026-07-23 20:21:47.310594
192	1	2	\N	\N	2026-01-11	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	54	1|U14|2026-01-11 00:00:00|00:00:00|0	2026-07-23 20:21:47.31337	2026-07-23 20:21:47.31337
193	1	2	\N	\N	2026-01-12	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	55	1|U14|2026-01-12 00:00:00|00:00:00|0	2026-07-23 20:21:47.316101	2026-07-23 20:21:47.316101
194	1	2	\N	\N	2026-01-13	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	56	1|U14|2026-01-13 00:00:00|00:00:00|0	2026-07-23 20:21:47.320153	2026-07-23 20:21:47.320153
195	1	2	\N	\N	2026-01-14	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	57	1|U14|2026-01-14 00:00:00|00:00:00|0	2026-07-23 20:21:47.32328	2026-07-23 20:21:47.32328
196	1	2	\N	\N	2026-01-15	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	58	1|U14|2026-01-15 00:00:00|00:00:00|0	2026-07-23 20:21:47.326283	2026-07-23 20:21:47.326283
197	1	2	\N	\N	2026-01-16	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	59	1|U14|2026-01-16 00:00:00|00:00:00|0	2026-07-23 20:21:47.329019	2026-07-23 20:21:47.329019
198	1	2	\N	\N	2026-01-17	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	60	1|U14|2026-01-17 00:00:00|00:00:00|0	2026-07-23 20:21:47.331952	2026-07-23 20:21:47.331952
199	1	2	\N	\N	2026-01-18	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	61	1|U14|2026-01-18 00:00:00|00:00:00|0	2026-07-23 20:21:47.335081	2026-07-23 20:21:47.335081
200	1	2	\N	\N	2026-01-19	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	62	1|U14|2026-01-19 00:00:00|00:00:00|0	2026-07-23 20:21:47.338185	2026-07-23 20:21:47.338185
201	1	2	\N	\N	2026-01-20	00:00:00	01:30:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	63	1|U14|2026-01-20 00:00:00|00:00:00|0	2026-07-23 20:21:47.34157	2026-07-23 20:21:47.34157
202	1	7	\N	\N	2026-01-21	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	64	1|U12_1|2026-01-21 00:00:00|00:00:00|0	2026-07-23 20:21:47.344574	2026-07-23 20:21:47.344574
203	1	7	\N	\N	2026-01-22	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	65	1|U12_1|2026-01-22 00:00:00|00:00:00|0	2026-07-23 20:21:47.347532	2026-07-23 20:21:47.347532
204	1	7	\N	\N	2026-01-23	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	66	1|U12_1|2026-01-23 00:00:00|00:00:00|0	2026-07-23 20:21:47.350299	2026-07-23 20:21:47.350299
205	1	7	\N	\N	2026-01-24	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	67	1|U12_1|2026-01-24 00:00:00|00:00:00|0	2026-07-23 20:21:47.353502	2026-07-23 20:21:47.353502
206	1	7	\N	\N	2026-01-25	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	68	1|U12_1|2026-01-25 00:00:00|00:00:00|0	2026-07-23 20:21:47.357082	2026-07-23 20:21:47.357082
207	1	7	\N	\N	2026-01-26	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	69	1|U12_1|2026-01-26 00:00:00|00:00:00|0	2026-07-23 20:21:47.360223	2026-07-23 20:21:47.360223
208	1	7	\N	\N	2026-01-27	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	70	1|U12_1|2026-01-27 00:00:00|00:00:00|0	2026-07-23 20:21:47.363146	2026-07-23 20:21:47.363146
209	1	7	\N	\N	2026-01-28	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	71	1|U12_1|2026-01-28 00:00:00|00:00:00|0	2026-07-23 20:21:47.365951	2026-07-23 20:21:47.365951
210	1	7	\N	\N	2026-01-29	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	72	1|U12_1|2026-01-29 00:00:00|00:00:00|0	2026-07-23 20:21:47.36908	2026-07-23 20:21:47.36908
211	1	7	\N	\N	2026-01-30	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	73	1|U12_1|2026-01-30 00:00:00|00:00:00|0	2026-07-23 20:21:47.373206	2026-07-23 20:21:47.373206
212	1	8	\N	\N	2026-01-31	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	74	1|U12_2|2026-01-31 00:00:00|00:00:00|0	2026-07-23 20:21:47.376422	2026-07-23 20:21:47.376422
213	1	8	\N	\N	2026-02-01	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	75	1|U12_2|2026-02-01 00:00:00|00:00:00|0	2026-07-23 20:21:47.379523	2026-07-23 20:21:47.379523
214	1	8	\N	\N	2026-02-02	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	76	1|U12_2|2026-02-02 00:00:00|00:00:00|0	2026-07-23 20:21:47.382533	2026-07-23 20:21:47.382533
215	1	8	\N	\N	2026-02-03	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	77	1|U12_2|2026-02-03 00:00:00|00:00:00|0	2026-07-23 20:21:47.385356	2026-07-23 20:21:47.385356
216	1	8	\N	\N	2026-02-04	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	78	1|U12_2|2026-02-04 00:00:00|00:00:00|0	2026-07-23 20:21:47.389077	2026-07-23 20:21:47.389077
217	1	8	\N	\N	2026-02-05	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	79	1|U12_2|2026-02-05 00:00:00|00:00:00|0	2026-07-23 20:21:47.392369	2026-07-23 20:21:47.392369
218	1	8	\N	\N	2026-02-06	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	80	1|U12_2|2026-02-06 00:00:00|00:00:00|0	2026-07-23 20:21:47.395398	2026-07-23 20:21:47.395398
219	1	8	\N	\N	2026-02-07	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	81	1|U12_2|2026-02-07 00:00:00|00:00:00|0	2026-07-23 20:21:47.398187	2026-07-23 20:21:47.398187
220	1	8	\N	\N	2026-02-08	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	82	1|U12_2|2026-02-08 00:00:00|00:00:00|0	2026-07-23 20:21:47.401011	2026-07-23 20:21:47.401011
221	1	8	\N	\N	2026-02-09	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	83	1|U12_2|2026-02-09 00:00:00|00:00:00|0	2026-07-23 20:21:47.404498	2026-07-23 20:21:47.404498
222	1	9	\N	\N	2026-02-10	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	84	1|U11|2026-02-10 00:00:00|00:00:00|0	2026-07-23 20:21:47.407588	2026-07-23 20:21:47.407588
223	1	9	\N	\N	2026-02-11	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	85	1|U11|2026-02-11 00:00:00|00:00:00|0	2026-07-23 20:21:47.410606	2026-07-23 20:21:47.410606
224	1	9	\N	\N	2026-02-12	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	86	1|U11|2026-02-12 00:00:00|00:00:00|0	2026-07-23 20:21:47.413394	2026-07-23 20:21:47.413394
225	1	9	\N	\N	2026-02-13	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	87	1|U11|2026-02-13 00:00:00|00:00:00|0	2026-07-23 20:21:47.416316	2026-07-23 20:21:47.416316
226	1	9	\N	\N	2026-02-14	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	88	1|U11|2026-02-14 00:00:00|00:00:00|0	2026-07-23 20:21:47.420523	2026-07-23 20:21:47.420523
227	1	9	\N	\N	2026-02-15	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	89	1|U11|2026-02-15 00:00:00|00:00:00|0	2026-07-23 20:21:47.423623	2026-07-23 20:21:47.423623
228	1	9	\N	\N	2026-02-16	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	90	1|U11|2026-02-16 00:00:00|00:00:00|0	2026-07-23 20:21:47.426713	2026-07-23 20:21:47.426713
229	1	9	\N	\N	2026-02-17	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	91	1|U11|2026-02-17 00:00:00|00:00:00|0	2026-07-23 20:21:47.429541	2026-07-23 20:21:47.429541
230	1	9	\N	\N	2026-02-18	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	92	1|U11|2026-02-18 00:00:00|00:00:00|0	2026-07-23 20:21:47.43237	2026-07-23 20:21:47.43237
231	1	9	\N	\N	2026-02-19	00:00:00	01:10:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	93	1|U11|2026-02-19 00:00:00|00:00:00|0	2026-07-23 20:21:47.435265	2026-07-23 20:21:47.435265
232	1	1	\N	\N	2026-10-17	09:30:00	12:00:00	Heimturnier	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	94	1|U10|2026-10-17 00:00:00|09:30:00|Heimturnier	2026-07-23 20:21:47.43841	2026-07-23 20:21:47.43841
233	1	1	\N	\N	2026-02-21	00:00:00	01:03:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	95	1|U10|2026-02-21 00:00:00|00:00:00|0	2026-07-23 20:21:47.441917	2026-07-23 20:21:47.441917
234	1	1	\N	\N	2026-02-22	00:00:00	01:03:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	96	1|U10|2026-02-22 00:00:00|00:00:00|0	2026-07-23 20:21:47.444911	2026-07-23 20:21:47.444911
235	1	1	\N	\N	2026-02-23	00:00:00	01:03:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	97	1|U10|2026-02-23 00:00:00|00:00:00|0	2026-07-23 20:21:47.447992	2026-07-23 20:21:47.447992
236	1	1	\N	\N	2026-02-24	00:00:00	01:03:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	98	1|U10|2026-02-24 00:00:00|00:00:00|0	2026-07-23 20:21:47.450824	2026-07-23 20:21:47.450824
237	1	10	\N	\N	2026-02-25	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	99	1|U9|2026-02-25 00:00:00|00:00:00|0	2026-07-23 20:21:47.454225	2026-07-23 20:21:47.454225
238	1	10	\N	\N	2026-02-26	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	100	1|U9|2026-02-26 00:00:00|00:00:00|0	2026-07-23 20:21:47.457421	2026-07-23 20:21:47.457421
239	1	10	\N	\N	2026-02-27	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	101	1|U9|2026-02-27 00:00:00|00:00:00|0	2026-07-23 20:21:47.460472	2026-07-23 20:21:47.460472
240	1	10	\N	\N	2026-02-28	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	102	1|U9|2026-02-28 00:00:00|00:00:00|0	2026-07-23 20:21:47.46354	2026-07-23 20:21:47.46354
241	1	10	\N	\N	2026-03-01	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	103	1|U9|2026-03-01 00:00:00|00:00:00|0	2026-07-23 20:21:47.466294	2026-07-23 20:21:47.466294
242	1	10	\N	\N	2026-03-02	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	104	1|U9|2026-03-02 00:00:00|00:00:00|0	2026-07-23 20:21:47.469447	2026-07-23 20:21:47.469447
243	1	10	\N	\N	2026-03-03	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	105	1|U9|2026-03-03 00:00:00|00:00:00|0	2026-07-23 20:21:47.472152	2026-07-23 20:21:47.472152
244	1	10	\N	\N	2026-03-04	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	106	1|U9|2026-03-04 00:00:00|00:00:00|0	2026-07-23 20:21:47.475369	2026-07-23 20:21:47.475369
245	1	10	\N	\N	2026-03-05	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	107	1|U9|2026-03-05 00:00:00|00:00:00|0	2026-07-23 20:21:47.478482	2026-07-23 20:21:47.478482
246	1	10	\N	\N	2026-03-06	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	108	1|U9|2026-03-06 00:00:00|00:00:00|0	2026-07-23 20:21:47.481534	2026-07-23 20:21:47.481534
247	1	11	\N	\N	2026-10-17	09:30:00	12:00:00	Heimturnier	Heim	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	109	1|U8|2026-10-17 00:00:00|09:30:00|Heimturnier	2026-07-23 20:21:47.484315	2026-07-23 20:21:47.484315
248	1	11	\N	\N	2026-03-08	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	110	1|U8|2026-03-08 00:00:00|00:00:00|0	2026-07-23 20:21:47.488894	2026-07-23 20:21:47.488894
249	1	11	\N	\N	2026-03-09	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	111	1|U8|2026-03-09 00:00:00|00:00:00|0	2026-07-23 20:21:47.491988	2026-07-23 20:21:47.491988
250	1	11	\N	\N	2026-03-10	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	112	1|U8|2026-03-10 00:00:00|00:00:00|0	2026-07-23 20:21:47.495154	2026-07-23 20:21:47.495154
251	1	11	\N	\N	2026-03-11	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	113	1|U8|2026-03-11 00:00:00|00:00:00|0	2026-07-23 20:21:47.497932	2026-07-23 20:21:47.497932
252	1	12	\N	\N	2026-10-17	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	114	1|U7|2026-10-17 00:00:00|00:00:00|0	2026-07-23 20:21:47.500819	2026-07-23 20:21:47.500819
253	1	12	\N	\N	2026-03-13	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	115	1|U7|2026-03-13 00:00:00|00:00:00|0	2026-07-23 20:21:47.504816	2026-07-23 20:21:47.504816
254	1	12	\N	\N	2026-03-14	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	116	1|U7|2026-03-14 00:00:00|00:00:00|0	2026-07-23 20:21:47.507711	2026-07-23 20:21:47.507711
255	1	12	\N	\N	2026-03-15	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	117	1|U7|2026-03-15 00:00:00|00:00:00|0	2026-07-23 20:21:47.510894	2026-07-23 20:21:47.510894
256	1	12	\N	\N	2026-03-16	00:00:00	03:00:00	0	Neutral	Spiel	aktiv		Terminefussball_2026_Herbst.xlsx	ICS2	118	1|U7|2026-03-16 00:00:00|00:00:00|0	2026-07-23 20:21:47.513799	2026-07-23 20:21:47.513799
\.


--
-- Data for Name: import_batches; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.import_batches (import_batch_id, import_type, source_file, started_at, finished_at, rows_read, rows_created, rows_updated, rows_skipped, rows_failed, status, report) FROM stdin;
\.


--
-- Data for Name: memberships; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.memberships (membership_id, person_id, season_id, status, joined_on, left_on, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.persons (person_id, external_member_id, first_name, last_name, birth_date, active, created_at, updated_at, gender, mobile, email, player_pass_number, entry_date, exit_date, status, note) FROM stdin;
127	\N	Test	Tester	2010-01-01	f	2026-07-22 08:34:54.931744	2026-07-22 09:48:24.412426	Männlich		test@tester.at		2026-07-22	9999-12-31	Archiviert	
128	127	Test2	Tester23	2009-01-01	f	2026-07-22 08:53:19.869651	2026-07-22 09:48:01.531353	Männlich				2026-07-22	2026-07-22	Archiviert	
1	1	Klara	Eitler	2020-02-26	t	2026-07-21 15:10:43.6176	2026-07-21 15:10:43.6176	\N	\N	\N	\N	\N	\N	\N	\N
2	2	Sophie	Schuster	2016-08-23	t	2026-07-21 15:10:43.62834	2026-07-21 15:10:43.62834	\N	\N	\N	\N	\N	\N	\N	\N
3	3	Lea	Joszt	2018-01-08	t	2026-07-21 15:10:43.630112	2026-07-21 15:10:43.630112	\N	\N	\N	\N	\N	\N	\N	\N
4	4	Anna	Joszt	2020-10-14	t	2026-07-21 15:10:43.631807	2026-07-21 15:10:43.631807	\N	\N	\N	\N	\N	\N	\N	\N
5	5	Mila	Randjelovic	2019-03-02	t	2026-07-21 15:10:43.633538	2026-07-21 15:10:43.633538	\N	\N	\N	\N	\N	\N	\N	\N
6	6	Mila	Peck	2015-04-25	t	2026-07-21 15:10:43.635223	2026-07-21 15:10:43.635223	\N	\N	\N	\N	\N	\N	\N	\N
7	7	Marlena	Markovits	2016-06-27	t	2026-07-21 15:10:43.637041	2026-07-21 15:10:43.637041	\N	\N	\N	\N	\N	\N	\N	\N
8	8	Samara	Pietreszuk	2016-04-09	t	2026-07-21 15:10:43.638733	2026-07-21 15:10:43.638733	\N	\N	\N	\N	\N	\N	\N	\N
9	9	Elena	Schwarz	2016-05-10	t	2026-07-21 15:10:43.640422	2026-07-21 15:10:43.640422	\N	\N	\N	\N	\N	\N	\N	\N
10	10	Lisa	Menschhorn	2016-07-22	t	2026-07-21 15:10:43.642017	2026-07-21 15:10:43.642017	\N	\N	\N	\N	\N	\N	\N	\N
11	11	Vanessa	Klingler	2016-06-27	t	2026-07-21 15:10:43.643714	2026-07-21 15:10:43.643714	\N	\N	\N	\N	\N	\N	\N	\N
12	12	Eleanor	Rac	2018-06-25	t	2026-07-21 15:10:43.645385	2026-07-21 15:10:43.645385	\N	\N	\N	\N	\N	\N	\N	\N
13	13	Johanna	Goge	2017-12-20	t	2026-07-21 15:10:43.647072	2026-07-21 15:10:43.647072	\N	\N	\N	\N	\N	\N	\N	\N
14	14	Hannah	Kaufmann	2015-03-11	t	2026-07-21 15:10:43.648715	2026-07-21 15:10:43.648715	\N	\N	\N	\N	\N	\N	\N	\N
15	15	Nora	Ehold	2018-02-15	t	2026-07-21 15:10:43.650372	2026-07-21 15:10:43.650372	\N	\N	\N	\N	\N	\N	\N	\N
16	16	Kristin	Peykoska	2018-07-18	t	2026-07-21 15:10:43.652079	2026-07-21 15:10:43.652079	\N	\N	\N	\N	\N	\N	\N	\N
17	17	Felicitas	Brosche	2016-04-01	t	2026-07-21 15:10:43.653941	2026-07-21 15:10:43.653941	\N	\N	\N	\N	\N	\N	\N	\N
18	18	Miriam	Schlögl	2017-03-21	t	2026-07-21 15:10:43.655188	2026-07-21 15:10:43.655188	\N	\N	\N	\N	\N	\N	\N	\N
19	19	Mia	Weiss	2015-08-31	t	2026-07-21 15:10:43.656509	2026-07-21 15:10:43.656509	\N	\N	\N	\N	\N	\N	\N	\N
20	20	Simone	Galos-Buchinger	2018-11-19	t	2026-07-21 15:10:43.657787	2026-07-21 15:10:43.657787	\N	\N	\N	\N	\N	\N	\N	\N
21	21	Mina	Dörfl	2018-10-11	t	2026-07-21 15:10:43.659376	2026-07-21 15:10:43.659376	\N	\N	\N	\N	\N	\N	\N	\N
22	22	Pia	Gamse	2017-03-01	t	2026-07-21 15:10:43.661086	2026-07-21 15:10:43.661086	\N	\N	\N	\N	\N	\N	\N	\N
23	23	Olivia	Casar	2016-07-12	t	2026-07-21 15:10:43.662994	2026-07-21 15:10:43.662994	\N	\N	\N	\N	\N	\N	\N	\N
24	24	Selina	Lichtenwörther	2015-09-09	t	2026-07-21 15:10:43.664721	2026-07-21 15:10:43.664721	\N	\N	\N	\N	\N	\N	\N	\N
25	25	Luis Maell	Bas	\N	t	2026-07-21 15:10:43.666422	2026-07-21 15:10:43.666422	\N	\N	\N	\N	\N	\N	\N	\N
26	26	Martin	Sator	2021-12-11	t	2026-07-21 15:10:43.668086	2026-07-21 15:10:43.668086	\N	\N	\N	\N	\N	\N	\N	\N
27	27	Timo	Valenta	2020-09-02	t	2026-07-21 15:10:43.669774	2026-07-21 15:10:43.669774	\N	\N	\N	\N	\N	\N	\N	\N
28	28	Ben	Schlögl	2021-02-24	t	2026-07-21 15:10:43.671537	2026-07-21 15:10:43.671537	\N	\N	\N	\N	\N	\N	\N	\N
29	29	Filip	Knezevic	2021-03-25	t	2026-07-21 15:10:43.673236	2026-07-21 15:10:43.673236	\N	\N	\N	\N	\N	\N	\N	\N
30	30	Paul	Eder-Leitgeb	2021-04-24	t	2026-07-21 15:10:43.674926	2026-07-21 15:10:43.674926	\N	\N	\N	\N	\N	\N	\N	\N
31	31	Mijat	Randjelovic	2021-06-24	t	2026-07-21 15:10:43.676608	2026-07-21 15:10:43.676608	\N	\N	\N	\N	\N	\N	\N	\N
32	32	Noah	Dratva	2021-07-15	t	2026-07-21 15:10:43.678307	2026-07-21 15:10:43.678307	\N	\N	\N	\N	\N	\N	\N	\N
33	33	Frederic	Pichler	2022-09-12	t	2026-07-21 15:10:43.679991	2026-07-21 15:10:43.679991	\N	\N	\N	\N	\N	\N	\N	\N
34	34	Vincent	Rac	2020-12-29	t	2026-07-21 15:10:43.681789	2026-07-21 15:10:43.681789	\N	\N	\N	\N	\N	\N	\N	\N
35	35	Timo	Kovotatschnik	2020-09-02	t	2026-07-21 15:10:43.683447	2026-07-21 15:10:43.683447	\N	\N	\N	\N	\N	\N	\N	\N
36	36	Ben	Innthaler	2020-12-22	t	2026-07-21 15:10:43.685189	2026-07-21 15:10:43.685189	\N	\N	\N	\N	\N	\N	\N	\N
37	37	Julian	Novosze	2020-10-08	t	2026-07-21 15:10:43.68702	2026-07-21 15:10:43.68702	\N	\N	\N	\N	\N	\N	\N	\N
38	38	Arthur	Schuster	2020-07-07	t	2026-07-21 15:10:43.688725	2026-07-21 15:10:43.688725	\N	\N	\N	\N	\N	\N	\N	\N
39	39	Alexander	Zax	2020-06-29	t	2026-07-21 15:10:43.690402	2026-07-21 15:10:43.690402	\N	\N	\N	\N	\N	\N	\N	\N
40	40	Niklas	Joszt	2020-04-26	t	2026-07-21 15:10:43.692075	2026-07-21 15:10:43.692075	\N	\N	\N	\N	\N	\N	\N	\N
41	41	Jakob	Ehold	2020-10-14	t	2026-07-21 15:10:43.693767	2026-07-21 15:10:43.693767	\N	\N	\N	\N	\N	\N	\N	\N
42	42	Paul	Strobl	2020-11-29	t	2026-07-21 15:10:43.69541	2026-07-21 15:10:43.69541	\N	\N	\N	\N	\N	\N	\N	\N
43	43	Leon	Huber	2019-11-25	t	2026-07-21 15:10:43.697101	2026-07-21 15:10:43.697101	\N	\N	\N	\N	\N	\N	\N	\N
44	44	Leon	Habeler	2019-11-14	t	2026-07-21 15:10:43.698894	2026-07-21 15:10:43.698894	\N	\N	\N	\N	\N	\N	\N	\N
45	45	Benjamin	Pratl	2019-10-16	t	2026-07-21 15:10:43.700705	2026-07-21 15:10:43.700705	\N	\N	\N	\N	\N	\N	\N	\N
46	46	Alp Ömer	Akay	2019-10-11	t	2026-07-21 15:10:43.702524	2026-07-21 15:10:43.702524	\N	\N	\N	\N	\N	\N	\N	\N
47	47	Levi	Koca-Gröber	2019-03-31	t	2026-07-21 15:10:43.704282	2026-07-21 15:10:43.704282	\N	\N	\N	\N	\N	\N	\N	\N
48	48	Luka	Cvetkovic	2019-02-24	t	2026-07-21 15:10:43.706075	2026-07-21 15:10:43.706075	\N	\N	\N	\N	\N	\N	\N	\N
49	49	Rayan	Ghanem	2019-07-17	t	2026-07-21 15:10:43.707735	2026-07-21 15:10:43.707735	\N	\N	\N	\N	\N	\N	\N	\N
50	50	Finn	Schwarz	2018-11-26	t	2026-07-21 15:10:43.709416	2026-07-21 15:10:43.709416	\N	\N	\N	\N	\N	\N	\N	\N
51	51	Ilyas Nuri	Özdemir	2018-02-21	t	2026-07-21 15:10:43.710944	2026-07-21 15:10:43.710944	\N	\N	\N	\N	\N	\N	\N	\N
52	52	Leon	Schopf	2018-05-17	t	2026-07-21 15:10:43.712661	2026-07-21 15:10:43.712661	\N	\N	\N	\N	\N	\N	\N	\N
53	53	Adrian	Lang	2018-07-07	t	2026-07-21 15:10:43.714324	2026-07-21 15:10:43.714324	\N	\N	\N	\N	\N	\N	\N	\N
54	54	Manuel	Frass	2017-11-15	t	2026-07-21 15:10:43.716018	2026-07-21 15:10:43.716018	\N	\N	\N	\N	\N	\N	\N	\N
55	55	Nils	Eitler	2018-03-25	t	2026-07-21 15:10:43.717706	2026-07-21 15:10:43.717706	\N	\N	\N	\N	\N	\N	\N	\N
56	56	Sascha	Ciocheltca	2018-06-22	t	2026-07-21 15:10:43.719391	2026-07-21 15:10:43.719391	\N	\N	\N	\N	\N	\N	\N	\N
57	57	Adrian	Thiel	2018-07-07	t	2026-07-21 15:10:43.721153	2026-07-21 15:10:43.721153	\N	\N	\N	\N	\N	\N	\N	\N
58	58	Lina	Heinrich	2018-01-04	t	2026-07-21 15:10:43.722832	2026-07-21 15:10:43.722832	\N	\N	\N	\N	\N	\N	\N	\N
59	59	Darius	Goga	2017-11-16	t	2026-07-21 15:10:43.724496	2026-07-21 15:10:43.724496	\N	\N	\N	\N	\N	\N	\N	\N
60	60	Karl	Horwath	2018-10-23	t	2026-07-21 15:10:43.72609	2026-07-21 15:10:43.72609	\N	\N	\N	\N	\N	\N	\N	\N
61	61	Valentin	Hofbauer	2018-03-16	t	2026-07-21 15:10:43.727805	2026-07-21 15:10:43.727805	\N	\N	\N	\N	\N	\N	\N	\N
62	62	Julian	Putric	2017-02-28	t	2026-07-21 15:10:43.729474	2026-07-21 15:10:43.729474	\N	\N	\N	\N	\N	\N	\N	\N
63	63	david	Mircionia	2017-02-16	t	2026-07-21 15:10:43.731249	2026-07-21 15:10:43.731249	\N	\N	\N	\N	\N	\N	\N	\N
64	64	Filip	Kozicic	2017-09-13	t	2026-07-21 15:10:43.733159	2026-07-21 15:10:43.733159	\N	\N	\N	\N	\N	\N	\N	\N
65	65	Petar	Marincic	2017-10-11	t	2026-07-21 15:10:43.735	2026-07-21 15:10:43.735	\N	\N	\N	\N	\N	\N	\N	\N
66	66	Luca	Brandl	2017-08-07	t	2026-07-21 15:10:43.736979	2026-07-21 15:10:43.736979	\N	\N	\N	\N	\N	\N	\N	\N
67	67	Güney Asaf	Özgün	2017-10-27	t	2026-07-21 15:10:43.738757	2026-07-21 15:10:43.738757	\N	\N	\N	\N	\N	\N	\N	\N
68	68	Kilian	Bernegger	2016-09-27	t	2026-07-21 15:10:43.74043	2026-07-21 15:10:43.74043	\N	\N	\N	\N	\N	\N	\N	\N
69	69	Dominik	König	2016-11-30	t	2026-07-21 15:10:43.741868	2026-07-21 15:10:43.741868	\N	\N	\N	\N	\N	\N	\N	\N
70	70	Selina	Sevelda	2016-04-13	t	2026-07-21 15:10:43.7435	2026-07-21 15:10:43.7435	\N	\N	\N	\N	\N	\N	\N	\N
71	71	Kilian	Frania	2017-03-16	t	2026-07-21 15:10:43.745174	2026-07-21 15:10:43.745174	\N	\N	\N	\N	\N	\N	\N	\N
72	72	Paul	Gruber	2016-10-22	t	2026-07-21 15:10:43.746909	2026-07-21 15:10:43.746909	\N	\N	\N	\N	\N	\N	\N	\N
73	73	Luca	Lichtenwörther	2017-03-31	t	2026-07-21 15:10:43.748578	2026-07-21 15:10:43.748578	\N	\N	\N	\N	\N	\N	\N	\N
74	74	Marc	Forsthuber	2016-12-12	t	2026-07-21 15:10:43.750281	2026-07-21 15:10:43.750281	\N	\N	\N	\N	\N	\N	\N	\N
75	75	Filip	Makivic	2016-11-17	t	2026-07-21 15:10:43.751938	2026-07-21 15:10:43.751938	\N	\N	\N	\N	\N	\N	\N	\N
76	76	Moritz	Valenta	2016-10-26	t	2026-07-21 15:10:43.753653	2026-07-21 15:10:43.753653	\N	\N	\N	\N	\N	\N	\N	\N
77	77	Marko	Petreski	2016-06-15	t	2026-07-21 15:10:43.755408	2026-07-21 15:10:43.755408	\N	\N	\N	\N	\N	\N	\N	\N
78	78	Kuzey	Özgün	2015-09-12	t	2026-07-21 15:10:43.757082	2026-07-21 15:10:43.757082	\N	\N	\N	\N	\N	\N	\N	\N
79	79	Zsombor	Ambrus	2015-12-18	t	2026-07-21 15:10:43.758752	2026-07-21 15:10:43.758752	\N	\N	\N	\N	\N	\N	\N	\N
80	80	David	Magler	2016-08-31	t	2026-07-21 15:10:43.760478	2026-07-21 15:10:43.760478	\N	\N	\N	\N	\N	\N	\N	\N
81	81	Felix	Krautschneider	2015-09-16	t	2026-07-21 15:10:43.762194	2026-07-21 15:10:43.762194	\N	\N	\N	\N	\N	\N	\N	\N
82	82	Noah	Heinrich	2015-07-09	t	2026-07-21 15:10:43.763865	2026-07-21 15:10:43.763865	\N	\N	\N	\N	\N	\N	\N	\N
84	84	Finn	Leser	2015-08-19	t	2026-07-21 15:10:43.767549	2026-07-21 15:10:43.767549	\N	\N	\N	\N	\N	\N	\N	\N
85	85	Alexander	Luzija	2014-11-15	t	2026-07-21 15:10:43.769349	2026-07-21 15:10:43.769349	\N	\N	\N	\N	\N	\N	\N	\N
86	86	Luca	Innthaler	2014-10-27	t	2026-07-21 15:10:43.771157	2026-07-21 15:10:43.771157	\N	\N	\N	\N	\N	\N	\N	\N
87	87	Niklas	Archam	2015-08-28	t	2026-07-21 15:10:43.772843	2026-07-21 15:10:43.772843	\N	\N	\N	\N	\N	\N	\N	\N
88	88	Fabio	Hackl	2014-11-13	t	2026-07-21 15:10:43.774519	2026-07-21 15:10:43.774519	\N	\N	\N	\N	\N	\N	\N	\N
89	89	Jakov	Marinčić	2015-05-30	t	2026-07-21 15:10:43.776198	2026-07-21 15:10:43.776198	\N	\N	\N	\N	\N	\N	\N	\N
90	90	Denis	Creciunesc	2015-06-10	t	2026-07-21 15:10:43.777872	2026-07-21 15:10:43.777872	\N	\N	\N	\N	\N	\N	\N	\N
91	91	Maximilian	Markovits	2014-04-22	t	2026-07-21 15:10:43.779539	2026-07-21 15:10:43.779539	\N	\N	\N	\N	\N	\N	\N	\N
92	92	Danin	Emurli	2014-08-07	t	2026-07-21 15:10:43.781219	2026-07-21 15:10:43.781219	\N	\N	\N	\N	\N	\N	\N	\N
93	93	Taha	Özmen	2014-06-26	t	2026-07-21 15:10:43.783161	2026-07-21 15:10:43.783161	\N	\N	\N	\N	\N	\N	\N	\N
94	94	Emilio	Rieder	2014-02-06	t	2026-07-21 15:10:43.784974	2026-07-21 15:10:43.784974	\N	\N	\N	\N	\N	\N	\N	\N
96	96	Utku	Cavush	2013-07-18	t	2026-07-21 15:10:43.788266	2026-07-21 15:10:43.788266	\N	\N	\N	\N	\N	\N	\N	\N
97	97	Leon	Innthaler	2013-04-20	t	2026-07-21 15:10:43.789947	2026-07-21 15:10:43.789947	\N	\N	\N	\N	\N	\N	\N	\N
98	98	Marcel de Jesus	Kain Fernandez	2013-05-17	t	2026-07-21 15:10:43.791626	2026-07-21 15:10:43.791626	\N	\N	\N	\N	\N	\N	\N	\N
99	99	Yannik Maximilian	Petsch	2012-12-20	t	2026-07-21 15:10:43.793297	2026-07-21 15:10:43.793297	\N	\N	\N	\N	\N	\N	\N	\N
100	100	Benjamin	Biermaier	2012-12-20	t	2026-07-21 15:10:43.795767	2026-07-21 15:10:43.795767	\N	\N	\N	\N	\N	\N	\N	\N
101	101	Philip	Hornbeck	2013-06-20	t	2026-07-21 15:10:43.797449	2026-07-21 15:10:43.797449	\N	\N	\N	\N	\N	\N	\N	\N
102	102	Lucas	Jambrich	2013-03-26	t	2026-07-21 15:10:43.799132	2026-07-21 15:10:43.799132	\N	\N	\N	\N	\N	\N	\N	\N
103	103	Julian	Lampel	2012-04-08	t	2026-07-21 15:10:43.800822	2026-07-21 15:10:43.800822	\N	\N	\N	\N	\N	\N	\N	\N
104	104	Leon	Hackl	2012-02-23	t	2026-07-21 15:10:43.802504	2026-07-21 15:10:43.802504	\N	\N	\N	\N	\N	\N	\N	\N
105	105	Sebastian	Sevelda	2012-01-20	t	2026-07-21 15:10:43.804169	2026-07-21 15:10:43.804169	\N	\N	\N	\N	\N	\N	\N	\N
106	106	Florian	Stadler	2012-04-24	t	2026-07-21 15:10:43.805863	2026-07-21 15:10:43.805863	\N	\N	\N	\N	\N	\N	\N	\N
107	107	Jovan	Cvetanovic	2012-06-11	t	2026-07-21 15:10:43.807533	2026-07-21 15:10:43.807533	\N	\N	\N	\N	\N	\N	\N	\N
108	108	Elias	Stanek	2012-02-10	t	2026-07-21 15:10:43.809275	2026-07-21 15:10:43.809275	\N	\N	\N	\N	\N	\N	\N	\N
109	109	Livio	Korp	2011-12-12	t	2026-07-21 15:10:43.81102	2026-07-21 15:10:43.81102	\N	\N	\N	\N	\N	\N	\N	\N
110	110	Sinan	Demirdas	2012-07-26	t	2026-07-21 15:10:43.812658	2026-07-21 15:10:43.812658	\N	\N	\N	\N	\N	\N	\N	\N
111	111	Lorenz Emil	Wimmer	2012-05-12	t	2026-07-21 15:10:43.814237	2026-07-21 15:10:43.814237	\N	\N	\N	\N	\N	\N	\N	\N
112	112	Maximilian	Zehetner	2011-09-23	t	2026-07-21 15:10:43.815944	2026-07-21 15:10:43.815944	\N	\N	\N	\N	\N	\N	\N	\N
113	113	Maximilian	Moos	2011-09-05	t	2026-07-21 15:10:43.817631	2026-07-21 15:10:43.817631	\N	\N	\N	\N	\N	\N	\N	\N
114	114	Felix	Gruber	2011-08-02	t	2026-07-21 15:10:43.819345	2026-07-21 15:10:43.819345	\N	\N	\N	\N	\N	\N	\N	\N
115	115	Dominic	Oberhofer	2011-12-06	t	2026-07-21 15:10:43.821255	2026-07-21 15:10:43.821255	\N	\N	\N	\N	\N	\N	\N	\N
116	116	Jamie	Böhm	2011-02-01	t	2026-07-21 15:10:43.822972	2026-07-21 15:10:43.822972	\N	\N	\N	\N	\N	\N	\N	\N
117	117	Tarik	Pasic	2011-02-12	t	2026-07-21 15:10:43.82466	2026-07-21 15:10:43.82466	\N	\N	\N	\N	\N	\N	\N	\N
118	118	Ceri	Yakup	2011-01-14	t	2026-07-21 15:10:43.82639	2026-07-21 15:10:43.82639	\N	\N	\N	\N	\N	\N	\N	\N
119	119	Lenny	Cerny	2011-07-18	t	2026-07-21 15:10:43.827957	2026-07-21 15:10:43.827957	\N	\N	\N	\N	\N	\N	\N	\N
120	120	Leon	Babic	2011-03-30	t	2026-07-21 15:10:43.829624	2026-07-21 15:10:43.829624	\N	\N	\N	\N	\N	\N	\N	\N
121	121	Maximilian	Pajak	2010-12-31	t	2026-07-21 15:10:43.831344	2026-07-21 15:10:43.831344	\N	\N	\N	\N	\N	\N	\N	\N
122	122	Elias	Mateyka	2010-11-08	t	2026-07-21 15:10:43.833003	2026-07-21 15:10:43.833003	\N	\N	\N	\N	\N	\N	\N	\N
123	123	Luz	Fischlein	2010-12-12	t	2026-07-21 15:10:43.8347	2026-07-21 15:10:43.8347	\N	\N	\N	\N	\N	\N	\N	\N
124	124	Noah	Kriegel	2011-02-13	t	2026-07-21 15:10:43.836386	2026-07-21 15:10:43.836386	\N	\N	\N	\N	\N	\N	\N	\N
125	125	Jakob	Pammer	2011-01-05	t	2026-07-21 15:10:43.838155	2026-07-21 15:10:43.838155	\N	\N	\N	\N	\N	\N	\N	\N
126	126	Dimitri	Cojan	2011-02-11	t	2026-07-21 15:10:43.839819	2026-07-21 15:10:43.839819	\N	\N	\N	\N	\N	\N	\N	\N
129	128	Tester	Test	2008-01-01	t	2026-07-22 09:50:06.048371	2026-07-22 09:50:06.048371	Männlich				2026-07-22	9999-12-31	Aktiv	
95	95	Niklas	Berger	2012-12-31	t	2026-07-21 15:10:43.786641	2026-07-23 07:50:45.640551				123456	2026-07-23	2026-07-23	\N	\N
83	83	Kilian	Artner	2015-08-29	t	2026-07-21 15:10:43.765693	2026-07-23 07:51:48.726741				987654321	2026-07-23	2026-07-23	\N	\N
\.


--
-- Data for Name: places; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.places (place_id, name, address, active, created_at, updated_at, facility_id, training_zones) FROM stdin;
1	Hauptplatz		t	2026-07-23 14:26:17.706835	2026-07-23 14:43:06.081787	1	2
\.


--
-- Data for Name: seasons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.seasons (season_id, name, start_date, end_date, active, created_at) FROM stdin;
1	2026/27	2026-07-01	2027-06-30	t	2026-07-21 13:26:49.478312
\.


--
-- Data for Name: team_members; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.team_members (team_member_id, team_id, person_id, role, valid_from, valid_until, created_at) FROM stdin;
1	1	95	Spieler	2026-07-22	\N	2026-07-22 15:00:29.364784
2	1	68	Spieler	2026-07-22	2026-07-22	2026-07-22 15:02:42.088039
3	1	68	Trainer	2026-07-23	2026-07-23	2026-07-23 06:50:46.09884
4	1	83	Trainer	2026-07-23	\N	2026-07-23 07:51:20.230402
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.teams (team_id, season_id, name, active, created_at, updated_at) FROM stdin;
1	1	U10	t	2026-07-21 16:09:29.839875	2026-07-21 17:02:11.9155
2	1	U14	t	2026-07-22 13:45:52.282843	2026-07-22 13:45:52.282843
3	1	U15	t	2026-07-23 20:14:52.083668	2026-07-23 20:14:52.083668
4	1	U16	t	2026-07-23 20:14:52.731193	2026-07-23 20:14:52.731193
5	1	KM	t	2026-07-23 20:14:52.734956	2026-07-23 20:14:52.734956
6	1	U23	t	2026-07-23 20:14:52.746287	2026-07-23 20:14:52.746287
7	1	U12_1	t	2026-07-23 20:14:52.881891	2026-07-23 20:14:52.881891
8	1	U12_2	t	2026-07-23 20:14:52.928374	2026-07-23 20:14:52.928374
9	1	U11	t	2026-07-23 20:14:52.956955	2026-07-23 20:14:52.956955
10	1	U9	t	2026-07-23 20:14:52.983021	2026-07-23 20:14:52.983021
11	1	U8	t	2026-07-23 20:14:53.019618	2026-07-23 20:14:53.019618
12	1	U7	t	2026-07-23 20:14:53.032242	2026-07-23 20:14:53.032242
13	1	Camp	t	2026-07-23 20:14:53.047697	2026-07-23 20:14:53.047697
14	1	GGG	t	2026-07-23 20:14:53.080914	2026-07-23 20:14:53.080914
15	1	Hallenturnie	t	2026-07-23 20:14:53.085998	2026-07-23 20:14:53.085998
16	1	Weihnachtsfeier	t	2026-07-23 20:14:53.096577	2026-07-23 20:14:53.096577
17	1	Fest ASV Neufeld	t	2026-07-23 20:14:53.110509	2026-07-23 20:14:53.110509
\.


--
-- Name: departments_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departments_department_id_seq', 6, true);


--
-- Name: facilities_facility_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.facilities_facility_id_seq', 1, true);


--
-- Name: games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.games_game_id_seq', 256, true);


--
-- Name: import_batches_import_batch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.import_batches_import_batch_id_seq', 1, false);


--
-- Name: memberships_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.memberships_membership_id_seq', 1, false);


--
-- Name: persons_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.persons_person_id_seq', 129, true);


--
-- Name: places_place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.places_place_id_seq', 1, true);


--
-- Name: seasons_season_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.seasons_season_id_seq', 1, true);


--
-- Name: team_members_team_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.team_members_team_member_id_seq', 4, true);


--
-- Name: teams_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.teams_team_id_seq', 17, true);


--
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (department_id);


--
-- Name: facilities facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_pkey PRIMARY KEY (facility_id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_id);


--
-- Name: import_batches import_batches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.import_batches
    ADD CONSTRAINT import_batches_pkey PRIMARY KEY (import_batch_id);


--
-- Name: memberships memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_pkey PRIMARY KEY (membership_id);


--
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (person_id);


--
-- Name: places places_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_name_key UNIQUE (name);


--
-- Name: places places_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_pkey PRIMARY KEY (place_id);


--
-- Name: seasons seasons_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seasons
    ADD CONSTRAINT seasons_name_key UNIQUE (name);


--
-- Name: seasons seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seasons
    ADD CONSTRAINT seasons_pkey PRIMARY KEY (season_id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (team_member_id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);


--
-- Name: games uq_game_source; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT uq_game_source UNIQUE (source_key);


--
-- Name: memberships uq_membership_person_season; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT uq_membership_person_season UNIQUE (person_id, season_id);


--
-- Name: persons uq_person_identity; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT uq_person_identity UNIQUE (first_name, last_name, birth_date);


--
-- Name: team_members uq_team_member; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT uq_team_member UNIQUE (team_id, person_id, role);


--
-- Name: teams uq_team_season; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT uq_team_season UNIQUE (season_id, name);


--
-- Name: idx_games_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_games_date ON public.games USING btree (game_date);


--
-- Name: idx_games_team; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_games_team ON public.games USING btree (team_id);


--
-- Name: idx_memberships_season; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_memberships_season ON public.memberships USING btree (season_id);


--
-- Name: idx_persons_birth_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_persons_birth_date ON public.persons USING btree (birth_date);


--
-- Name: idx_persons_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_persons_name ON public.persons USING btree (last_name, first_name);


--
-- Name: places fk_places_facility; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT fk_places_facility FOREIGN KEY (facility_id) REFERENCES public.facilities(facility_id);


--
-- Name: games games_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_place_id_fkey FOREIGN KEY (place_id) REFERENCES public.places(place_id) ON DELETE SET NULL;


--
-- Name: games games_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(season_id) ON DELETE RESTRICT;


--
-- Name: games games_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id) ON DELETE RESTRICT;


--
-- Name: memberships memberships_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


--
-- Name: memberships memberships_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(season_id) ON DELETE RESTRICT;


--
-- Name: team_members team_members_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


--
-- Name: team_members team_members_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(team_id) ON DELETE CASCADE;


--
-- Name: teams teams_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_season_id_fkey FOREIGN KEY (season_id) REFERENCES public.seasons(season_id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict ev7X6X4oRcAhxCA9AeKg5sFhXQHC3WbYBSCSaEY7ioqX3eEbmz4hjhZdBla7wH8

