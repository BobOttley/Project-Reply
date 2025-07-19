--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Postgres.app)
-- Dumped by pg_dump version 17.5 (Postgres.app)

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
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    id integer NOT NULL,
    name character varying(128),
    email character varying(128) NOT NULL,
    phone character varying(32),
    child_name character varying(128),
    admissions_stage character varying(64) DEFAULT 'Enquiry'::character varying,
    notes text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_id_seq OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: children; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.children (
    id integer NOT NULL,
    parent_id integer NOT NULL,
    name character varying NOT NULL,
    dob timestamp without time zone,
    year_group character varying,
    interests text,
    account_number character varying,
    customer_id character varying
);


ALTER TABLE public.children OWNER TO postgres;

--
-- Name: children_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.children_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.children_id_seq OWNER TO postgres;

--
-- Name: children_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.children_id_seq OWNED BY public.children.id;


--
-- Name: emails; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emails (
    id integer NOT NULL,
    unique_id character varying NOT NULL,
    user_id character varying,
    thread_id character varying,
    subject character varying,
    from_address character varying,
    to_address character varying,
    body text,
    status character varying,
    date_received timestamp without time zone,
    dismissed_by character varying,
    dismissed_at timestamp without time zone,
    processed_by character varying,
    processed_at timestamp without time zone,
    direction character varying,
    customer_id character varying
);


ALTER TABLE public.emails OWNER TO postgres;

--
-- Name: emails_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.emails_id_seq OWNER TO postgres;

--
-- Name: emails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emails_id_seq OWNED BY public.emails.id;


--
-- Name: enquiries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enquiries (
    id integer NOT NULL,
    parent_id integer NOT NULL,
    child_id integer,
    enquiry_date timestamp without time zone,
    source character varying,
    raw_text text,
    pipeline_stage_id integer,
    customer_id character varying
);


ALTER TABLE public.enquiries OWNER TO postgres;

--
-- Name: enquiries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enquiries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enquiries_id_seq OWNER TO postgres;

--
-- Name: enquiries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enquiries_id_seq OWNED BY public.enquiries.id;


--
-- Name: parents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parents (
    id integer NOT NULL,
    name character varying,
    email character varying NOT NULL,
    phone character varying,
    account_number character varying,
    customer_id character varying
);


ALTER TABLE public.parents OWNER TO postgres;

--
-- Name: parents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parents_id_seq OWNER TO postgres;

--
-- Name: parents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parents_id_seq OWNED BY public.parents.id;


--
-- Name: pipeline_stages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pipeline_stages (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.pipeline_stages OWNER TO postgres;

--
-- Name: pipeline_stages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pipeline_stages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pipeline_stages_id_seq OWNER TO postgres;

--
-- Name: pipeline_stages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pipeline_stages_id_seq OWNED BY public.pipeline_stages.id;


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: children id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.children ALTER COLUMN id SET DEFAULT nextval('public.children_id_seq'::regclass);


--
-- Name: emails id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails ALTER COLUMN id SET DEFAULT nextval('public.emails_id_seq'::regclass);


--
-- Name: enquiries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enquiries ALTER COLUMN id SET DEFAULT nextval('public.enquiries_id_seq'::regclass);


--
-- Name: parents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parents ALTER COLUMN id SET DEFAULT nextval('public.parents_id_seq'::regclass);


--
-- Name: pipeline_stages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pipeline_stages ALTER COLUMN id SET DEFAULT nextval('public.pipeline_stages_id_seq'::regclass);


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (id, name, email, phone, child_name, admissions_stage, notes, created_at, updated_at) FROM stdin;
1	Test Parent	parent@example.com	\N	Alice	Enquiry	\N	2025-07-19 08:35:27.767421	2025-07-19 08:35:27.767421
\.


--
-- Data for Name: children; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.children (id, parent_id, name, dob, year_group, interests, account_number, customer_id) FROM stdin;
1	1	Sophie	\N	Year 5	\N	C-20250719-001	\N
2	2		\N	Year 9	\N	C-20250719-002	\N
\.


--
-- Data for Name: emails; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emails (id, unique_id, user_id, thread_id, subject, from_address, to_address, body, status, date_received, dismissed_by, dismissed_at, processed_by, processed_at, direction, customer_id) FROM stdin;
1	<36943F07-BBB3-4F96-B80B-FE85A85B7983@cognitivetasking.com>	\N	\N	Test Email 	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_192816517]\r\n	unprocessed	2025-07-16 15:11:36	\N	\N	\N	\N	\N	LOCAL-TEST
2	<66C6ED3E-72B7-4BD8-ADCC-C3245A5766A3@cognitivetasking.com>	\N	\N	Test 2 	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	I love all of this coding\r\n\r\n[signature_13046388]\r\n	unprocessed	2025-07-16 15:25:51	\N	\N	\N	\N	\N	LOCAL-TEST
3	<C7F467D3-99E1-44C0-8AFE-44F30DB9BCBF@cognitivetasking.com>	\N	\N	Test 3	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	Hello\r\n\r\n[signature_3581357949]\r\n	unprocessed	2025-07-16 16:53:29	\N	\N	\N	\N	\N	LOCAL-TEST
4	<09E595B4-29CE-4462-82C4-74108D8638F9@cognitivetasking.com>	\N	\N	Test 4	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_562157042]\r\n	unprocessed	2025-07-16 16:53:39	\N	\N	\N	\N	\N	LOCAL-TEST
5	<C0BC1AE7-6576-44EE-A033-D912CCE8B7E4@cognitivetasking.com>	\N	\N	Tets 5	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_37170654]\r\n	unprocessed	2025-07-16 16:54:02	\N	\N	\N	\N	\N	LOCAL-TEST
6	<34E95D6C-A5FA-468D-BC18-50E372CBF8F5@cognitivetasking.com>	\N	\N	Interested in Learning More About Your School  pgsql Copy Edit 	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	Hello,\r\n\r\nI’ve heard great things about your school and would love to learn more. My son is currently in Year 4 and we’re considering options for Year 5 entry in September.\r\n\r\nCould you please let me know if you have any upcoming open days? Also, do you offer any taster sessions?\r\n\r\nThanks so much,\r\nJulia Henderson\r\n\r\n\r\n	unprocessed	2025-07-16 17:36:49	\N	\N	\N	\N	\N	LOCAL-TEST
7	<171CAF33-9E80-4065-977A-FE203718EE59@cognitivetasking.com>	\N	\N	Questions About Fees and Scholarships	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	Hi there,\r\n\r\nWe’re looking into schools for our daughter and are trying to understand the fee structure. Could you send me details of termly fees for Year 7, as well as any scholarship or bursary opportunities?\r\n\r\nBest,\r\nTom Sinclair\r\n\r\n\r\n	unprocessed	2025-07-16 17:37:16	\N	\N	\N	\N	\N	LOCAL-TEST
8	<E742444E-EE83-4D4A-B37B-C7B439446F96@cognitivetasking.com>	\N	\N	Support for Children with Learning Differences	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	Dear Admissions,\r\n\r\nI’m exploring school options for my son who has mild dyslexia and ADHD. We’re particularly looking for schools that have strong pastoral support and experience in helping pupils with learning differences thrive.\r\n\r\nWould you be able to provide some insight into how your school approaches this?\r\n\r\nKind regards,\r\nAnita Rayner\r\n\r\n\r\n	unprocessed	2025-07-16 17:37:42	\N	\N	\N	\N	\N	LOCAL-TEST
9	<8523AD95-7A96-469B-B5A5-BF16DEE7F803@cognitivetasking.com>	\N	\N	Open Day & Admissions Process	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	Open Day & Admissions Process\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 09:32\r\nSubject: Admissions Enquiry for Year 7\r\nDear Admissions Team,\r\nI am interested in applying for my daughter, Isabella, to join Year 7 in September 2026. Could you please send me more information about the admissions process and any upcoming open days?\r\nMany thanks,\r\nEmma Williams\r\n________________________________\r\nFrom: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nTo: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nDate: Mon, 15 Jul 2025, 11:03\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Mrs Williams,\r\nThank you for your enquiry regarding Year 7 entry for Isabella.\r\nOur admissions process is detailed on our website, but in summary, it includes an online application, an entrance assessment, and an informal interview. The key dates for 2026 entry will be published in September, but applications typically open in early October.\r\nWe would also be delighted to welcome you to our next Open Morning on Saturday 21st September 2025. You can register your interest here.\r\nPlease let us know if you have any further questions.\r\nBest wishes,\r\nAlex Mason\r\nAdmissions Officer\r\n________________________________\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 13:15\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Alex,\r\nThank you so much for your helpful reply. I have registered for the Open Morning and look forward to meeting the team in September.\r\nBest regards,\r\nEmma\r\n\r\n[signature_2516224571]\r\n	unprocessed	2025-07-17 06:53:16	\N	\N	\N	\N	\N	LOCAL-TEST
10	<509A8A5B-3DB5-4A02-AE55-AC7F56446DFC@cognitivetasking.com>	\N	\N	Scholarships & Fee Assistance	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Wed, 10 Jul 2025, 16:22\r\nSubject: Enquiry About Scholarships and Fees\r\nHello,\r\nI am enquiring about academic scholarships for entry into Year 9 for my son, Samuel. Do you offer scholarships, and if so, what is the application process? I would also appreciate a copy of your current fee schedule.\r\nKind regards,\r\nSimon Phillips\r\n________________________________\r\nFrom: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nTo: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nDate: Wed, 10 Jul 2025, 17:45\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Mr Phillips,\r\nThank you for contacting us regarding scholarships and fees.\r\nWe do offer academic scholarships for Year 9 entry. The application process involves submitting a scholarship application form by 30th November 2025, followed by an assessment day in January.\r\nOur current fee schedule is attached and also available on our website.\r\nPlease let me know if you require any further information.\r\nBest wishes,\r\nJess Ottley-Woodd\r\nDirector of Admissions\r\n________________________________\r\nFrom: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Thu, 11 Jul 2025, 08:30\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Jess,\r\nMany thanks for your prompt response and for sending the fee schedule. I’ll review the scholarship information with Samuel and be in touch if we have any questions.\r\nBest regards,\r\nSimon\r\n\r\n\r\n[signature_939487133]\r\n	unprocessed	2025-07-17 06:53:55	\N	\N	\N	\N	\N	LOCAL-TEST
16	<F08A77E5-8288-427E-8B31-AB14040AE178@cognitivetasking.com>	\N	\N	FWD: Re: Arrange a School Tour	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Thu, 10 Jul 2025, 09:10\r\nSubject: Arrange a School Tour\r\nHello,\r\nI’d like to book a tour for my daughter, Sophie (applying for Year 5). Are tours available this month?\r\nThank you,\r\nLisa Franks\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\r\nDate: Thu, 10 Jul 2025, 10:30\r\nSubject: Re: Arrange a School Tour\r\nDear Lisa,\r\nYes, we are running tours every Wednesday and Friday at 10am throughout July. Would you like to join this Friday or next week?\r\nKind regards,\r\nNick Foster\r\nAdmissions\r\n________________________________\r\nFrom: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Thu, 10 Jul 2025, 11:12\r\nSubject: Re: Arrange a School Tour\r\nThis Friday would be perfect—thank you. See you then!\r\nLisa\r\n\r\n\r\n[signature_590730159]\r\n	unprocessed	2025-07-18 17:01:22	\N	\N	\N	\N	\N	LOCAL-TEST
11	<6739C7E2-2634-41A6-8350-957CBF9FE92B@cognitivetasking.com>	\N	\N	Special Educational Needs Support	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: claire.roberts@icloud.com<mailto:claire.roberts@icloud.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Fri, 12 Jul 2025, 10:09\r\nSubject: SEN Provision for New Students\r\nHi there,\r\nI’m considering your school for my daughter, Mia, who has mild dyslexia. Could you please tell me more about the SEN provision available and how support is offered in class?\r\nThank you,\r\nClaire Roberts\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: claire.roberts@icloud.com<mailto:claire.roberts@icloud.com>\r\nDate: Fri, 12 Jul 2025, 12:05\r\nSubject: Re: SEN Provision for New Students\r\nDear Claire,\r\nThank you for your email and for considering The Waverly School for Mia.\r\nWe have a dedicated Learning Support team who work closely with class teachers to ensure that pupils with dyslexia and other learning differences receive tailored support. This includes small group interventions, specialist teaching, and regular progress reviews.\r\nIf you would like to discuss Mia’s needs in more detail, we can arrange a meeting with our SENCO at your convenience.\r\nBest wishes,\r\nSarah Milner\r\nAdmissions\r\n________________________________\r\nFrom: claire.roberts@icloud.com<mailto:claire.roberts@icloud.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Fri, 12 Jul 2025, 13:47\r\nSubject: Re: SEN Provision for New Students\r\nDear Sarah,\r\nThank you very much for the information. I would appreciate a meeting with the SENCO—please could you let me know some available times next week?\r\nBest,\r\nClaire\r\n\r\n\r\n[signature_1759358782]\r\n	unprocessed	2025-07-17 06:54:31	\N	\N	\N	\N	\N	LOCAL-TEST
12	<BA0FF449-5704-444A-87C4-B93D7AF3656A@cognitivetasking.com>	\N	\N	FW: Scholarships & Fee Assistance	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_1046170371]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 18:43\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: FW: Scholarships & Fee Assistance\r\n\r\n\r\n\r\n[signature_1386025136]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Scholarships & Fee Assistance\r\n\r\nFrom: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Wed, 10 Jul 2025, 16:22\r\nSubject: Enquiry About Scholarships and Fees\r\nHello,\r\nI am enquiring about academic scholarships for entry into Year 9 for my son, Samuel. Do you offer scholarships, and if so, what is the application process? I would also appreciate a copy of your current fee schedule.\r\nKind regards,\r\nSimon Phillips\r\n________________________________\r\nFrom: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nTo: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nDate: Wed, 10 Jul 2025, 17:45\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Mr Phillips,\r\nThank you for contacting us regarding scholarships and fees.\r\nWe do offer academic scholarships for Year 9 entry. The application process involves submitting a scholarship application form by 30th November 2025, followed by an assessment day in January.\r\nOur current fee schedule is attached and also available on our website.\r\nPlease let me know if you require any further information.\r\nBest wishes,\r\nJess Ottley-Woodd\r\nDirector of Admissions\r\n________________________________\r\nFrom: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Thu, 11 Jul 2025, 08:30\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Jess,\r\nMany thanks for your prompt response and for sending the fee schedule. I’ll review the scholarship information with Samuel and be in touch if we have any questions.\r\nBest regards,\r\nSimon\r\n\r\n\r\n[signature_939487133]\r\n	unprocessed	2025-07-18 12:28:04	\N	\N	\N	\N	\N	LOCAL-TEST
13	<26E8E2C6-C118-45AE-869C-D0047E2E9E59@cognitivetasking.com>	\N	\N	FW: Open Day & Admissions Process	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_3929753594]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 18:43\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: FW: Open Day & Admissions Process\r\n\r\n\r\n\r\n[signature_3453825193]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Open Day & Admissions Process\r\n\r\nOpen Day & Admissions Process\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 09:32\r\nSubject: Admissions Enquiry for Year 7\r\nDear Admissions Team,\r\nI am interested in applying for my daughter, Isabella, to join Year 7 in September 2026. Could you please send me more information about the admissions process and any upcoming open days?\r\nMany thanks,\r\nEmma Williams\r\n________________________________\r\nFrom: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nTo: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nDate: Mon, 15 Jul 2025, 11:03\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Mrs Williams,\r\nThank you for your enquiry regarding Year 7 entry for Isabella.\r\nOur admissions process is detailed on our website, but in summary, it includes an online application, an entrance assessment, and an informal interview. The key dates for 2026 entry will be published in September, but applications typically open in early October.\r\nWe would also be delighted to welcome you to our next Open Morning on Saturday 21st September 2025. You can register your interest here.\r\nPlease let us know if you have any further questions.\r\nBest wishes,\r\nAlex Mason\r\nAdmissions Officer\r\n________________________________\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 13:15\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Alex,\r\nThank you so much for your helpful reply. I have registered for the Open Morning and look forward to meeting the team in September.\r\nBest regards,\r\nEmma\r\n\r\n[signature_2516224571]\r\n	unprocessed	2025-07-18 12:28:16	\N	\N	\N	\N	\N	LOCAL-TEST
14	<49FC4483-8644-4FC9-833E-4661E8CD89A1@cognitivetasking.com>	\N	\N	FW: Open Day & Admissions Process	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_1124716029]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 18:43\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: FW: Open Day & Admissions Process\r\n\r\n\r\n\r\n[signature_46925412]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Open Day & Admissions Process\r\n\r\nOpen Day & Admissions Process\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 09:32\r\nSubject: Admissions Enquiry for Year 7\r\nDear Admissions Team,\r\nI am interested in applying for my daughter, Isabella, to join Year 7 in September 2026. Could you please send me more information about the admissions process and any upcoming open days?\r\nMany thanks,\r\nEmma Williams\r\n________________________________\r\nFrom: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nTo: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nDate: Mon, 15 Jul 2025, 11:03\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Mrs Williams,\r\nThank you for your enquiry regarding Year 7 entry for Isabella.\r\nOur admissions process is detailed on our website, but in summary, it includes an online application, an entrance assessment, and an informal interview. The key dates for 2026 entry will be published in September, but applications typically open in early October.\r\nWe would also be delighted to welcome you to our next Open Morning on Saturday 21st September 2025. You can register your interest here.\r\nPlease let us know if you have any further questions.\r\nBest wishes,\r\nAlex Mason\r\nAdmissions Officer\r\n________________________________\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 13:15\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Alex,\r\nThank you so much for your helpful reply. I have registered for the Open Morning and look forward to meeting the team in September.\r\nBest regards,\r\nEmma\r\n\r\n[signature_2516224571]\r\n	unprocessed	2025-07-18 12:27:48	\N	\N	\N	\N	\N	LOCAL-TEST
15	<36F1C027-E09A-40A5-8936-01EFCCF26AB2@cognitivetasking.com>	\N	\N	FWD: Admissions for Overseas Students	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Tue, 8 Jul 2025, 21:15\r\nSubject: Admissions for Overseas Students\r\nDear Admissions,\r\nWe are based in Hong Kong and interested in applying for Year 9 in 2026. Do you accept international students, and what are the requirements?\r\nBest regards,\r\nMing Chen\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\r\nDate: Wed, 9 Jul 2025, 08:05\r\nSubject: Re: Admissions for Overseas Students\r\nDear Ming,\r\nThank you for your interest. We welcome international pupils and offer full boarding from Year 7 upwards. Applications require academic transcripts, a reference, and an English language assessment. Let us know if you’d like more details or a virtual meeting.\r\nBest wishes,\r\nSophie Dean\r\nAdmissions\r\n________________________________\r\nFrom: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Wed, 9 Jul 2025, 10:55\r\nSubject: Re: Admissions for Overseas Students\r\nThank you, Sophie. Please send more details about the virtual meeting and assessment.\r\nKind regards,\r\nMing\r\n\r\n\r\n[signature_169008624]\r\n	unprocessed	2025-07-18 17:00:48	\N	\N	\N	\N	\N	LOCAL-TEST
17	<5188B36A-45F8-4048-9528-FC9F2B5EC80B@cognitivetasking.com>	\N	\N	FW: Open Day & Admissions Process	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_3453825193]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Open Day & Admissions Process\r\n\r\nOpen Day & Admissions Process\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 09:32\r\nSubject: Admissions Enquiry for Year 7\r\nDear Admissions Team,\r\nI am interested in applying for my daughter, Isabella, to join Year 7 in September 2026. Could you please send me more information about the admissions process and any upcoming open days?\r\nMany thanks,\r\nEmma Williams\r\n________________________________\r\nFrom: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nTo: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nDate: Mon, 15 Jul 2025, 11:03\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Mrs Williams,\r\nThank you for your enquiry regarding Year 7 entry for Isabella.\r\nOur admissions process is detailed on our website, but in summary, it includes an online application, an entrance assessment, and an informal interview. The key dates for 2026 entry will be published in September, but applications typically open in early October.\r\nWe would also be delighted to welcome you to our next Open Morning on Saturday 21st September 2025. You can register your interest here.\r\nPlease let us know if you have any further questions.\r\nBest wishes,\r\nAlex Mason\r\nAdmissions Officer\r\n________________________________\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 13:15\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Alex,\r\nThank you so much for your helpful reply. I have registered for the Open Morning and look forward to meeting the team in September.\r\nBest regards,\r\nEmma\r\n\r\n[signature_2516224571]\r\n	unprocessed	2025-07-17 18:43:17	\N	\N	\N	\N	\N	LOCAL-TEST
18	<9AA5FFED-2D66-4E8A-99A3-9D0CAD31936A@cognitivetasking.com>	\N	\N	FW: Scholarships & Fee Assistance	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_1386025136]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Scholarships & Fee Assistance\r\n\r\nFrom: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Wed, 10 Jul 2025, 16:22\r\nSubject: Enquiry About Scholarships and Fees\r\nHello,\r\nI am enquiring about academic scholarships for entry into Year 9 for my son, Samuel. Do you offer scholarships, and if so, what is the application process? I would also appreciate a copy of your current fee schedule.\r\nKind regards,\r\nSimon Phillips\r\n________________________________\r\nFrom: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nTo: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nDate: Wed, 10 Jul 2025, 17:45\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Mr Phillips,\r\nThank you for contacting us regarding scholarships and fees.\r\nWe do offer academic scholarships for Year 9 entry. The application process involves submitting a scholarship application form by 30th November 2025, followed by an assessment day in January.\r\nOur current fee schedule is attached and also available on our website.\r\nPlease let me know if you require any further information.\r\nBest wishes,\r\nJess Ottley-Woodd\r\nDirector of Admissions\r\n________________________________\r\nFrom: s.phillips@hotmail.com<mailto:s.phillips@hotmail.com>\r\nTo: admissions@bassetths.org.uk<mailto:admissions@bassetths.org.uk>\r\nDate: Thu, 11 Jul 2025, 08:30\r\nSubject: Re: Enquiry About Scholarships and Fees\r\nDear Jess,\r\nMany thanks for your prompt response and for sending the fee schedule. I’ll review the scholarship information with Samuel and be in touch if we have any questions.\r\nBest regards,\r\nSimon\r\n\r\n\r\n[signature_939487133]\r\n	unprocessed	2025-07-17 18:43:26	\N	\N	\N	\N	\N	LOCAL-TEST
19	<644E6CFB-E152-43E1-90EA-43E1E3AFBE02@cognitivetasking.com>	\N	\N	FW: Open Day & Admissions Process	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	\r\n\r\n[signature_46925412]\r\n\r\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\r\nDate: Thursday, 17 July 2025 at 06:53\r\nTo: "smart_reply@penai.co.uk" <smart_reply@penai.co.uk>\r\nSubject: Open Day & Admissions Process\r\n\r\nOpen Day & Admissions Process\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 09:32\r\nSubject: Admissions Enquiry for Year 7\r\nDear Admissions Team,\r\nI am interested in applying for my daughter, Isabella, to join Year 7 in September 2026. Could you please send me more information about the admissions process and any upcoming open days?\r\nMany thanks,\r\nEmma Williams\r\n________________________________\r\nFrom: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nTo: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nDate: Mon, 15 Jul 2025, 11:03\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Mrs Williams,\r\nThank you for your enquiry regarding Year 7 entry for Isabella.\r\nOur admissions process is detailed on our website, but in summary, it includes an online application, an entrance assessment, and an informal interview. The key dates for 2026 entry will be published in September, but applications typically open in early October.\r\nWe would also be delighted to welcome you to our next Open Morning on Saturday 21st September 2025. You can register your interest here.\r\nPlease let us know if you have any further questions.\r\nBest wishes,\r\nAlex Mason\r\nAdmissions Officer\r\n________________________________\r\nFrom: emma.williams@gmail.com<mailto:emma.williams@gmail.com>\r\nTo: admissions@cognitivecollege.org.uk<mailto:admissions@cognitivecollege.org.uk>\r\nDate: Mon, 15 Jul 2025, 13:15\r\nSubject: Re: Admissions Enquiry for Year 7\r\nDear Alex,\r\nThank you so much for your helpful reply. I have registered for the Open Morning and look forward to meeting the team in September.\r\nBest regards,\r\nEmma\r\n\r\n[signature_2516224571]\r\n	unprocessed	2025-07-17 18:43:45	\N	\N	\N	\N	\N	LOCAL-TEST
20	<7C35B5B3-1AAF-48E4-ABDC-B5A64D8C2144@cognitivetasking.com>	\N	\N	FWD: Subject: SEN Provision	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: rachel.hughes@gmail.com<mailto:rachel.hughes@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Mon, 7 Jul 2025, 09:10\r\nSubject: SEN Provision\r\nHello,\r\nI am considering The Waverly School for my son, Jack, who has mild autism. Can you outline your SEN support, particularly in mainstream classrooms?\r\nThank you,\r\nRachel Hughes\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: rachel.hughes@gmail.com<mailto:rachel.hughes@gmail.com>\r\nDate: Mon, 7 Jul 2025, 10:45\r\nSubject: Re: SEN Provision\r\nDear Rachel,\r\nThank you for your enquiry. Our Learning Support Department works closely with classroom teachers to provide individual and small group interventions, tailored to each child’s needs. We also offer regular meetings with our SENCO to review progress.\r\nWould you like to arrange a meeting to discuss Jack’s needs in more detail?\r\nBest wishes,\r\nEmma Carter\r\nAdmissions\r\n________________________________\r\nFrom: rachel.hughes@gmail.com<mailto:rachel.hughes@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Mon, 7 Jul 2025, 11:05\r\nSubject: Re: SEN Provision\r\nThank you, Emma. Yes, I would like to arrange a meeting—do you have any availability next week?\r\nBest,\r\nRachel\r\n\r\n\r\n[signature_16833476]\r\n	unprocessed	2025-07-18 16:59:12	\N	\N	\N	\N	\N	LOCAL-TEST
21	<1B610CC4-C533-455E-B154-2B481F050809@cognitivetasking.com>	\N	\N	Fwd: Subject: Fees and Payment Plans	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: lucy.williams@gmail.com<mailto:lucy.williams@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Thu, 10 Jul 2025, 09:05\r\nSubject: Fees and Payment Plans\r\nDear Admissions Team,\r\nCould you please provide information on tuition fees for international pupils and whether payment plans are available?\r\nKind regards,\r\nLucy Williams\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: lucy.williams@gmail.com<mailto:lucy.williams@gmail.com>\r\nDate: Thu, 10 Jul 2025, 11:20\r\nSubject: Re: Fees and Payment Plans\r\nDear Lucy,\r\nThank you for your enquiry. For the 2025–26 academic year, fees for international pupils are £12,900 per term. We do offer payment plans—these can be discussed with our Finance Office, and arrangements are tailored to each family's circumstances.\r\nIf you would like further details, please let us know.\r\nBest wishes,\r\nEdward Cole\r\nAdmissions\r\n________________________________\r\nFrom: lucy.williams@gmail.com<mailto:lucy.williams@gmail.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Thu, 10 Jul 2025, 13:42\r\nSubject: Re: Fees and Payment Plans\r\nThank you, Edward. I would appreciate details on the available payment plan options and any additional charges.\r\nBest,\r\nLucy\r\n\r\n\r\n[signature_1420540876]\r\n	unprocessed	2025-07-18 16:56:16	\N	\N	\N	\N	\N	LOCAL-TEST
22	<D7697BD0-262A-4CD3-933E-F0CB33DB733F@cognitivetasking.com>	\N	\N	FWD: Subject: Re: School Fees	Robert Ottley <robert.ottley@cognitivetasking.com>	"smart_reply@penai.co.uk" <smart_reply@penai.co.uk>	From: julian.ross@icloud.com<mailto:julian.ross@icloud.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Wed, 9 Jul 2025, 14:00\r\nSubject: School Fees\r\nDear Admissions Team,\r\nCould you provide the termly fee amount for Year 7 and let me know if monthly payment is possible?\r\nThanks,\r\nJulian Ross\r\n________________________________\r\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nTo: julian.ross@icloud.com<mailto:julian.ross@icloud.com>\r\nDate: Wed, 9 Jul 2025, 15:05\r\nSubject: Re: School Fees\r\nDear Julian,\r\nFor 2025–26, the Year 7 fee is £9,850 per term. Monthly payment can be arranged via direct debit—our Finance team will be happy to assist.\r\nWould you like their contact details?\r\nBest wishes,\r\nHarriet Long\r\nAdmissions\r\n________________________________\r\nFrom: julian.ross@icloud.com<mailto:julian.ross@icloud.com>\r\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\r\nDate: Wed, 9 Jul 2025, 16:20\r\nSubject: Re: School Fees\r\nYes, please send their details. Many thanks for your help.\r\nJulian\r\n\r\n\r\n[signature_3223688144]\r\n	unprocessed	2025-07-18 16:59:58	\N	\N	\N	\N	\N	LOCAL-TEST
\.


--
-- Data for Name: enquiries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enquiries (id, parent_id, child_id, enquiry_date, source, raw_text, pipeline_stage_id, customer_id) FROM stdin;
1	1	1	2025-07-19 09:24:10.4137	email	Subject: FWD: Re: Arrange a School Tour\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\nReceived: 2025-07-18T17:01:22\n\nFrom: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Thu, 10 Jul 2025, 09:10\nSubject: Arrange a School Tour\nHello,\nI’d like to book a tour for my daughter, Sophie (applying for Year 5). Are tours available this month?\nThank you,\nLisa Franks\n________________________________\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nTo: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nDate: Thu, 10 Jul 2025, 10:30\nSubject: Re: Arrange a School Tour\nDear Lisa,\nYes, we are running tours every Wednesday and Friday at 10am throughout July. Would you like to join this Friday or next week?\nKind regards,\nNick Foster\nAdmissions\n________________________________\nFrom: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Thu, 10 Jul 2025, 11:12\nSubject: Re: Arrange a School Tour\nThis Friday would be perfect—thank you. See you then!\nLisa\n\n\n[signature_590730159]	\N	LOCAL-TEST
2	1	1	2025-07-19 12:24:45.796573	email	Subject: FWD: Re: Arrange a School Tour\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\nReceived: 2025-07-18T17:01:22\n\nFrom: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Thu, 10 Jul 2025, 09:10\nSubject: Arrange a School Tour\nHello,\nI’d like to book a tour for my daughter, Sophie (applying for Year 5). Are tours available this month?\nThank you,\nLisa Franks\n________________________________\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nTo: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nDate: Thu, 10 Jul 2025, 10:30\nSubject: Re: Arrange a School Tour\nDear Lisa,\nYes, we are running tours every Wednesday and Friday at 10am throughout July. Would you like to join this Friday or next week?\nKind regards,\nNick Foster\nAdmissions\n________________________________\nFrom: lisa.franks@gmail.com<mailto:lisa.franks@gmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Thu, 10 Jul 2025, 11:12\nSubject: Re: Arrange a School Tour\nThis Friday would be perfect—thank you. See you then!\nLisa\n\n\n[signature_590730159]	\N	LOCAL-TEST
3	2	2	2025-07-19 12:25:31.292577	email	Subject: FWD: Admissions for Overseas Students\nFrom: Robert Ottley <robert.ottley@cognitivetasking.com>\nReceived: 2025-07-18T17:00:48\n\nFrom: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Tue, 8 Jul 2025, 21:15\nSubject: Admissions for Overseas Students\nDear Admissions,\nWe are based in Hong Kong and interested in applying for Year 9 in 2026. Do you accept international students, and what are the requirements?\nBest regards,\nMing Chen\n________________________________\nFrom: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nTo: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\nDate: Wed, 9 Jul 2025, 08:05\nSubject: Re: Admissions for Overseas Students\nDear Ming,\nThank you for your interest. We welcome international pupils and offer full boarding from Year 7 upwards. Applications require academic transcripts, a reference, and an English language assessment. Let us know if you’d like more details or a virtual meeting.\nBest wishes,\nSophie Dean\nAdmissions\n________________________________\nFrom: ming.chen@hotmail.com<mailto:ming.chen@hotmail.com>\nTo: admissions@thewaverlyschool.org<mailto:admissions@thewaverlyschool.org>\nDate: Wed, 9 Jul 2025, 10:55\nSubject: Re: Admissions for Overseas Students\nThank you, Sophie. Please send more details about the virtual meeting and assessment.\nKind regards,\nMing\n\n\n[signature_169008624]	\N	LOCAL-TEST
\.


--
-- Data for Name: parents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parents (id, name, email, phone, account_number, customer_id) FROM stdin;
1	Lisa Franks	lisa.franks@gmail.com		P-20250719-001	LOCAL-TEST
2	Ming Chen	ming.chen@hotmail.com		P-20250719-002	LOCAL-TEST
\.


--
-- Data for Name: pipeline_stages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pipeline_stages (id, name) FROM stdin;
\.


--
-- Name: accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_id_seq', 1, true);


--
-- Name: children_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.children_id_seq', 2, true);


--
-- Name: emails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emails_id_seq', 22, true);


--
-- Name: enquiries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enquiries_id_seq', 3, true);


--
-- Name: parents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parents_id_seq', 2, true);


--
-- Name: pipeline_stages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pipeline_stages_id_seq', 1, false);


--
-- Name: accounts accounts_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_email_key UNIQUE (email);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: children children_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.children
    ADD CONSTRAINT children_pkey PRIMARY KEY (id);


--
-- Name: emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_pkey PRIMARY KEY (id);


--
-- Name: enquiries enquiries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enquiries
    ADD CONSTRAINT enquiries_pkey PRIMARY KEY (id);


--
-- Name: parents parents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parents
    ADD CONSTRAINT parents_pkey PRIMARY KEY (id);


--
-- Name: pipeline_stages pipeline_stages_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pipeline_stages
    ADD CONSTRAINT pipeline_stages_name_key UNIQUE (name);


--
-- Name: pipeline_stages pipeline_stages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pipeline_stages
    ADD CONSTRAINT pipeline_stages_pkey PRIMARY KEY (id);


--
-- Name: children uix_parent_child_name_dob; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.children
    ADD CONSTRAINT uix_parent_child_name_dob UNIQUE (parent_id, name, dob);


--
-- Name: ix_children_account_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_children_account_number ON public.children USING btree (account_number);


--
-- Name: ix_children_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_children_customer_id ON public.children USING btree (customer_id);


--
-- Name: ix_children_dob; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_children_dob ON public.children USING btree (dob);


--
-- Name: ix_children_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_children_name ON public.children USING btree (name);


--
-- Name: ix_children_parent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_children_parent_id ON public.children USING btree (parent_id);


--
-- Name: ix_emails_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emails_customer_id ON public.emails USING btree (customer_id);


--
-- Name: ix_emails_date_received; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emails_date_received ON public.emails USING btree (date_received);


--
-- Name: ix_emails_thread_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emails_thread_id ON public.emails USING btree (thread_id);


--
-- Name: ix_emails_unique_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_emails_unique_id ON public.emails USING btree (unique_id);


--
-- Name: ix_enquiries_child_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_enquiries_child_id ON public.enquiries USING btree (child_id);


--
-- Name: ix_enquiries_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_enquiries_customer_id ON public.enquiries USING btree (customer_id);


--
-- Name: ix_enquiries_enquiry_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_enquiries_enquiry_date ON public.enquiries USING btree (enquiry_date);


--
-- Name: ix_enquiries_parent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_enquiries_parent_id ON public.enquiries USING btree (parent_id);


--
-- Name: ix_parents_account_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_parents_account_number ON public.parents USING btree (account_number);


--
-- Name: ix_parents_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_parents_customer_id ON public.parents USING btree (customer_id);


--
-- Name: ix_parents_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_parents_email ON public.parents USING btree (email);


--
-- Name: ix_parents_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_parents_name ON public.parents USING btree (name);


--
-- Name: children children_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.children
    ADD CONSTRAINT children_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.parents(id);


--
-- Name: enquiries enquiries_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enquiries
    ADD CONSTRAINT enquiries_child_id_fkey FOREIGN KEY (child_id) REFERENCES public.children(id);


--
-- Name: enquiries enquiries_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enquiries
    ADD CONSTRAINT enquiries_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.parents(id);


--
-- Name: enquiries enquiries_pipeline_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enquiries
    ADD CONSTRAINT enquiries_pipeline_stage_id_fkey FOREIGN KEY (pipeline_stage_id) REFERENCES public.pipeline_stages(id);


--
-- PostgreSQL database dump complete
--

