-- Prisma Database Triggers for RAG System Updates
-- This script creates triggers that notify the RAG system when data changes

-- First, let's create a function that can make HTTP requests
-- Note: This requires the http extension in PostgreSQL
-- If you don't have it installed, you might need to use an alternative approach

-- For databases that support HTTP requests directly:
/*
CREATE EXTENSION IF NOT EXISTS http;

CREATE OR REPLACE FUNCTION notify_rag_system()
RETURNS TRIGGER AS $func_notify_rag$
DECLARE
    payload JSON;
    result TEXT;
BEGIN
    -- Create payload with information about the change
    payload := json_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'timestamp', NOW(),
        'record_id', COALESCE(NEW.id, OLD.id)
    );
    
    -- Send HTTP POST request to the RAG system
    -- Note: Adjust the URL to match your actual Render endpoint
    SELECT content INTO result FROM http_post(
        'https://rag-llm-1.onrender.com/update_rag',
        payload::TEXT,
        'application/json'
    );
    
    RETURN NEW;
EXCEPTION
    WHEN OTHERS THEN
        -- Log error but don't fail the transaction
        RAISE WARNING 'Failed to notify RAG system: %', SQLERRM;
        RETURN NEW;
END;
$func_notify_rag$ LANGUAGE plpgsql;
*/

-- Alternative approach using pg_notify (requires external listener):
CREATE OR REPLACE FUNCTION notify_rag_system()
RETURNS TRIGGER AS $func_notify_rag$
DECLARE
    payload JSON;
BEGIN
    -- Create payload with information about the change
    payload := json_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'timestamp', NOW(),
        'schema', TG_TABLE_SCHEMA
    );
    
    -- Notify any listening processes
    PERFORM pg_notify('rag_update', payload::TEXT);
    
    RETURN NEW;
EXCEPTION
    WHEN OTHERS THEN
        -- Log error but don't fail the transaction
        RAISE WARNING 'Failed to notify RAG system: %', SQLERRM;
        RETURN NEW;
END;
$func_notify_rag$ LANGUAGE plpgsql;

-- Create triggers for each table that should trigger RAG updates

-- Hospital table trigger
DROP TRIGGER IF EXISTS hospital_rag_update_trigger ON "Hospital";
CREATE TRIGGER hospital_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "Hospital"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- Doctor table trigger
DROP TRIGGER IF EXISTS doctor_rag_update_trigger ON "Doctor";
CREATE TRIGGER doctor_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "Doctor"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- User (Patient) table trigger
DROP TRIGGER IF EXISTS user_rag_update_trigger ON "User";
CREATE TRIGGER user_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "User"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- Interaction table trigger
DROP TRIGGER IF EXISTS interaction_rag_update_trigger ON "Interaction";
CREATE TRIGGER interaction_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "Interaction"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- Report table trigger
DROP TRIGGER IF EXISTS report_rag_update_trigger ON "Report";
CREATE TRIGGER report_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "Report"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- SOAP Note table trigger
DROP TRIGGER IF EXISTS soap_note_rag_update_trigger ON "SoapNote";
CREATE TRIGGER soap_note_rag_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "SoapNote"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_system();

-- Create a function to manually trigger RAG updates for all data
CREATE OR REPLACE FUNCTION trigger_full_rag_update()
RETURNS TEXT AS $func_full_rag_update$
DECLARE
    result TEXT;
BEGIN
    -- Notify for a full data refresh
    PERFORM pg_notify('rag_update', json_build_object(
        'type', 'full_refresh',
        'timestamp', NOW()
    )::TEXT);
    
    RETURN 'Full RAG update triggered';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error triggering full RAG update: ' || SQLERRM;
END;
$func_full_rag_update$ LANGUAGE plpgsql;

-- To manually trigger a full RAG update, you can call:
-- SELECT trigger_full_rag_update();

-- To listen for notifications (in another session):
-- LISTEN rag_update;