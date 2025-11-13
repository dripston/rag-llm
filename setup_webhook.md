# Prisma Database Webhook Setup

This document explains how to set up automatic RAG updates when your Prisma database is updated.

## Overview

When new data is inserted or updated in your Prisma database, you want to automatically notify your RAG system running on Render at `https://rag-llm-1.onrender.com`.

## Setup Options

### Option 1: Database Triggers (Recommended)

If your database supports triggers, you can set up a trigger that calls the webhook whenever data is inserted or updated.

Example for PostgreSQL:
```sql
-- Create a function to call the webhook
CREATE OR REPLACE FUNCTION notify_rag_update()
RETURNS TRIGGER AS $$
BEGIN
    -- This would need to be implemented with a stored procedure
    -- that can make HTTP requests, or use an external service
    PERFORM pg_notify('rag_update', json_build_object(
        'table', TG_TABLE_NAME,
        'operation', TG_OP,
        'timestamp', NOW()
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers on relevant tables
CREATE TRIGGER rag_update_trigger
    AFTER INSERT OR UPDATE ON "Hospital"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_update();

CREATE TRIGGER rag_update_trigger
    AFTER INSERT OR UPDATE ON "Doctor"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_update();

CREATE TRIGGER rag_update_trigger
    AFTER INSERT OR UPDATE ON "User"
    FOR EACH ROW EXECUTE FUNCTION notify_rag_update();
```

### Option 2: Application-Level Webhooks

In your application code that updates the Prisma database, add a call to the webhook handler after successful database operations:

```python
# After updating your Prisma database
from prisma_webhook_handler import trigger_rag_update

# Trigger RAG update
trigger_rag_update()
```

### Option 3: Scheduled Updates

Set up a cron job or scheduled task to periodically check for updates and send them to the RAG system:

```bash
# Add to crontab to run every 10 minutes
*/10 * * * * cd /path/to/your/project && python prisma_webhook_handler.py
```

## Environment Variables

Make sure the following environment variables are set in your Prisma database environment:

```
RENDER_SERVICE_URL=https://rag-llm-1.onrender.com
DATABASE_URL=your_prisma_database_url
```

## Testing

To test the webhook setup:

1. Run the test script:
   ```bash
   python test_webhook.py
   ```

2. Check the Render logs to verify the update was received.

## Troubleshooting

1. **Connection Issues**: Ensure your database can reach the Render endpoint.
2. **Authentication**: The current implementation doesn't require authentication, but you may want to add it for production use.
3. **Rate Limiting**: Be aware of any rate limits on your Render service.