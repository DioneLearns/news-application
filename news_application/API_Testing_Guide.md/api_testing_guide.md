# API Testing Guide

##  Authentication Required
All endpoints require user authentication. Use these test accounts:

**Test Users:**
- Reader: `web_reader` / `webpass123`
- Journalist: `web_journalist` / `webpass123` 
- Editor: `web_editor` / `webpass123`

## API Endpoints

### Articles
- `GET /api/articles/` - Get articles based on user role
- `GET /api/articles/my_subscriptions/` - Reader's subscribed content

### Publishers  
- `GET /api/publishers/` - List all publishers
- `POST /api/publishers/{id}/subscribe/` - Subscribe to publisher
- `POST /api/publishers/{id}/unsubscribe/` - Unsubscribe from publisher

### Users (Journalists)
- `GET /api/users/` - List all journalists
- `POST /api/users/{id}/subscribe/` - Subscribe to journalist
- `POST /api/users/{id}/unsubscribe/` - Unsubscribe from journalist

##  Test Scenarios

### Scenario 1: Reader Access
1. Login as `web_reader`
2. `GET /api/articles/` - Should see empty list (no subscriptions yet)
3. `POST /api/publishers/1/subscribe/` - Subscribe to publisher
4. `GET /api/articles/` - Should now see publisher's articles

### Scenario 2: Journalist Access  
1. Login as `web_journalist`
2. `GET /api/articles/` - Should see only own articles
3. Create article via web interface
4. Verify article appears in API

### Scenario 3: Editor Access
1. Login as `web_editor` 
2. `GET /api/articles/` - Should see ALL articles
3. Approve pending articles via web interface
4. Verify approved articles appear to readers

### Scenario 4: Subscription Management
1. Login as reader
2. Subscribe to journalist via `POST /api/users/2/subscribe/`
3. Verify journalist's articles appear
4. Unsubscribe and verify articles disappear

## Required Screenshots

1. **Reader view** - Empty articles list before subscriptions
2. **Reader view** - Articles after subscribing to publisher/journalist  
3. **Journalist view** - Only own articles visible
4. **Editor view** - All articles visible
5. **Subscription endpoints** - Successful subscribe/unsubscribe responses
6. **Authentication error** - Access without login