Version 1 - No whitelisting and no optimisation

CREATE EXTENSION IF NOT EXISTS hstore;

CREATE SCHEMA audit;

REVOKE ALL ON SCHEMA audit FROM public;

CREATE TABLE audit.logged_actions (
    event_id bigserial primary key,
    table_name text not null,
    id bigserial not null,
    action_tstamp_tx TIMESTAMP WITH TIME ZONE NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('I','D','U', 'T')),
    original_fields hstore,
    changed_fields hstore
);

REVOKE ALL ON audit.logged_actions FROM public;

CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS TRIGGER AS $body$
DECLARE
    audit_row audit.logged_actions;
    excluded_cols text[] = ARRAY[]::text[];
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'audit.if_modified_func() may only run as an AFTER trigger';
    END IF;

    audit_row = ROW(
        nextval('audit.logged_actions_event_id_seq'), -- event_id
        TG_TABLE_NAME::text,                          -- table_name
        OLD.id,                                       -- primary key for the changed record
        current_timestamp,                            -- action_tstamp_tx
        substring(TG_OP,1,1),                         -- action
        NULL,																					-- original_fields
        NULL                                          -- changed_fields
        );

		IF TG_ARGV[0] IS NOT NULL THEN
        excluded_cols = TG_ARGV[0]::text[];
    END IF;
    
    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        audit_row.original_fields =  (hstore(OLD.*) - hstore(NEW.*) - excluded_cols) - excluded_cols;
        audit_row.changed_fields =  (hstore(NEW.*) - hstore(OLD.*) - excluded_cols) - excluded_cols;
        IF audit_row.changed_fields = hstore('') THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
    		audit_row.changed_fields = NULL;
        audit_row.original_fields = hstore(OLD.*) - excluded_cols;
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
    		audit_row.original_fields = NULL;
        audit_row.changed_fields = hstore(NEW.*) - excluded_cols;
    ELSE
        RAISE EXCEPTION '[audit.if_modified_func] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;
    INSERT INTO audit.logged_actions VALUES (audit_row.*);
    RETURN NULL;
END;
$body$
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public;


CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass, ignored_cols text[]) RETURNS void AS $body$
DECLARE
  _q_txt text;
  _ignored_cols_snip text = '';
BEGIN
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_row ON ' || target_table;

    IF array_length(ignored_cols,1) > 0 THEN
        _ignored_cols_snip = quote_literal(ignored_cols);
    END IF;
    _q_txt = 'CREATE TRIGGER audit_trigger_row AFTER INSERT OR UPDATE OR DELETE ON ' || 
             target_table || 
             ' FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func(' ||
             _ignored_cols_snip || ');';
    RAISE NOTICE '%',_q_txt;
    EXECUTE _q_txt;
END;
$body$
language 'plpgsql';


CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass) RETURNS void AS $body$
SELECT audit.audit_table($1, ARRAY[]::text[]);
$body$ LANGUAGE SQL;


Version 2 - Whitelisting and Optimisation

CREATE EXTENSION IF NOT EXISTS hstore;

CREATE SCHEMA audit;

REVOKE ALL ON SCHEMA audit FROM public;

CREATE TABLE audit.logged_actions (
    event_id bigserial primary key,
    table_name text not null,
    id bigserial not null,
    action_tstamp_tx TIMESTAMP WITH TIME ZONE NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('I','D','U', 'T')),
    original_fields hstore,
    changed_fields hstore
);

REVOKE ALL ON audit.logged_actions FROM public;

CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS TRIGGER AS $body$
DECLARE
    audit_row audit.logged_actions;
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'audit.if_modified_func() may only run as an AFTER trigger';
    END IF;

    audit_row = ROW(
        nextval('audit.logged_actions_event_id_seq'), -- event_id
        TG_TABLE_NAME::text,                          -- table_name
        OLD.id,                                       -- primary key for the changed record
        current_timestamp,                            -- action_tstamp_tx
        substring(TG_OP,1,1),                         -- action
        NULL,																					-- original_fields
        NULL                                          -- changed_fields
        );

    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        audit_row.original_fields =  (hstore(OLD.*) - hstore(NEW.*));
        audit_row.changed_fields =  (hstore(NEW.*) - hstore(OLD.*));
        IF audit_row.changed_fields = hstore('') THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
    		audit_row.changed_fields = NULL;
        audit_row.original_fields = hstore(OLD.*);
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
    		audit_row.original_fields = NULL;
        audit_row.changed_fields = hstore(NEW.*);
    ELSE
        RAISE EXCEPTION '[audit.if_modified_func] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;
    INSERT INTO audit.logged_actions VALUES (audit_row.*);
    RETURN NULL;
END;
$body$
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public;


CREATE TRIGGER audit_update_trigger_row 
AFTER UPDATE ON target_table 
FOR EACH ROW
WHEN ((OLD.column_name) IS DISTINCT FROM (NEW.column_name))
EXECUTE PROCEDURE audit.if_modified_func();

CREATE TRIGGER audit_delete_and_insert_trigger_row 
AFTER INSERT OR DELETE ON target_table 
FOR EACH ROW
WHEN ((OLD.column_name) IS DISTINCT FROM (NEW.column_name))
EXECUTE PROCEDURE audit.if_modified_func();


Reference : 
https://wiki.postgresql.org/wiki/Audit_trigger_91plus
https://github.com/2ndQuadrant/audit-trigger


