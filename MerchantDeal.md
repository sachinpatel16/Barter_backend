# Merchant Deal System API Documentation

## 📋 Overview

The Merchant Deal System provides functionality for merchant-to-merchant **fixed point deal exchange**. Merchants can create deals with fixed point amounts, discover other merchants' deals, and exchange points through a structured, no-negotiation process.

## ✨ Key Features

- **Fixed Point Deals**: Merchants create deals with fixed point amounts (no negotiation)
- **Point-Based Exchange**: 1 Rupee = 10 Points conversion rate
- **Deal Discovery**: Find deals from other merchants with merchant logos
- **Automatic Point Transfer**: Seamless point exchange when deals are completed
- **Location-Based Filtering**: Deals can be filtered by city and location
- **Deal Management**: Create, update, activate, deactivate deals
- **Real-time Notifications**: Instant notifications for deal activities
- **Point Tracking**: Complete audit trail of point usage
- **Merchant Logos**: Visual merchant identification in all API responses

## 🏗️ System Architecture

### Models

#### MerchantDeal

Main model for merchant deals with point-based system.

**Fields:**

- `merchant`: Foreign key to MerchantProfile
- `title`: Deal title
- `description`: Deal description
- `points_offered`: Points offered for the deal
- `points_used`: Points already used
- `points_remaining`: Available points
- `deal_value`: Monetary value (points/10)
- `category`: Deal category
- `status`: Deal status (active, inactive, completed)
- `expiry_date`: Deal expiry date

#### MerchantDealRequest

Model to track merchant deal requests with fixed point system.

**Fields:**

- `requesting_merchant`: Merchant requesting the deal
- `deal`: Deal being requested
- `points_requested`: Points requested (automatically set to deal's points_offered)
- `status`: Request status (pending, accepted, rejected)
- `message`: Request message

**Fixed Point Logic:**

- Points requested must exactly match deal's points_offered
- No negotiation or counter-offers allowed
- System automatically sets points_requested = deal.points_offered

#### MerchantDealConfirmation

Model for confirmed merchant deals.

**Fields:**

- `deal`: Associated deal
- `merchant1`: Deal creator
- `merchant2`: Deal requester
- `points_exchanged`: Points to be exchanged
- `status`: Confirmation status (pending, confirmed, completed)

#### MerchantPointsTransfer

Model for points transfer between merchants.

**Fields:**

- `from_merchant`: Sender merchant
- `to_merchant`: Receiver merchant
- `points_amount`: Points transferred
- `transfer_fee`: Transfer fee
- `net_amount`: Net amount after fees
- `status`: Transfer status (pending, completed, failed)

#### DealPointUsage

Model to track how deal points are used.

**Fields:**

- `deal`: Associated deal
- `from_merchant`: Merchant using points
- `to_merchant`: Merchant receiving points
- `usage_type`: Type of usage (exchange, discount, transfer)
- `points_used`: Points used

## 🚀 API Endpoints

### 💼 Merchant Deals

#### Create Deal

```http
POST /api/custom_auth/v1/merchant-deals/
```

**Description:** Create a new merchant deal.

**Authentication:** Required (JWT Token - Merchant only)

**Request Headers:**

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "Food Delivery Service",
  "description": "Looking for reliable delivery partner for food delivery service",
  "points_offered": 500.0,
  "category": 1,
  "expiry_date": "2024-01-31T23:59:59Z",
  "preferred_cities": ["Mumbai", "Delhi", "Bangalore"],
  "terms_conditions": "Must have delivery vehicles and experienced staff"
}
```

**Important Notes:**

- Points are deducted from merchant's wallet when deal is created
- Deal becomes active immediately after creation
- Points are locked until deal is completed or expired

**Response:**

```json
{
  "id": 1,
  "merchant": 1,
  "merchant_name": "Pizza Palace",
  "merchant_logo": "http://localhost:8000/media/merchant/logo/pizza_logo.jpg",
  "title": "Food Delivery Service",
  "description": "Looking for reliable delivery partner",
  "points_offered": 500.0,
  "points_remaining": 500.0,
  "deal_value": 50.0,
  "category": 1,
  "category_name": "Food & Beverage",
  "status": "active",
  "expiry_date": "2024-01-31T23:59:59Z",
  "is_expired": false,
  "request_count": 0,
  "confirmation_count": 0,
  "create_time": "2024-01-01T10:00:00Z"
}
```

#### Get My Deals

```http
GET /api/custom_auth/v1/merchant-deals/
```

**Description:** Get deals created by the current merchant.

**Authentication:** Required (JWT Token - Merchant only)

**Query Parameters:**

- `status`: Filter by deal status (active, inactive, completed)
- `category`: Filter by category ID
- `page`: Page number for pagination
- `page_size`: Number of results per page

**Response:**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "merchant_logo": "http://localhost:8000/media/merchant/logo/pizza_logo.jpg",
      "title": "Food Delivery Service",
      "points_offered": 500.0,
      "points_remaining": 500.0,
      "status": "active",
      "request_count": 3,
      "confirmation_count": 1,
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### Activate Deal

```http
POST /api/custom_auth/v1/merchant-deals/{id}/activate/
```

**Description:** Activate a deal.

**Response:**

```json
{
  "message": "Deal activated successfully"
}
```

#### Deactivate Deal

```http
POST /api/custom_auth/v1/merchant-deals/{id}/deactivate/
```

**Description:** Deactivate a deal.

**Response:**

```json
{
  "message": "Deal deactivated successfully"
}
```

#### Get Deal Usage History

```http
GET /api/custom_auth/v1/merchant-deals/{id}/usage-history/
```

**Description:** Get point usage history for a deal.

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "deal_title": "Food Delivery Service",
      "from_merchant_name": "Pizza Palace",
      "to_merchant_name": "Delivery Co",
      "points_used": 500.0,
      "usage_type": "exchange",
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### Deal Discovery

#### Get All Deals

```http
GET /api/custom_auth/v1/deal-discovery/
```

**Description:** Discover deals from other merchants.

**Query Parameters:**

- `category`: Filter by category ID
- `points_offered`: Filter by points offered
- `merchant__city`: Filter by merchant city
- `min_points`: Minimum points filter
- `max_points`: Maximum points filter

**Response:**

```json
{
  "results": [
    {
      "id": 2,
      "merchant": 2,
      "merchant_name": "Delivery Co",
      "merchant_logo": "http://localhost:8000/media/merchant/logo/delivery_logo.jpg",
      "title": "Marketing Support",
      "points_offered": 300.0,
      "points_remaining": 300.0,
      "category_name": "Marketing",
      "status": "active"
    }
  ]
}
```

#### Get Deals by Points

```http
GET /api/custom_auth/v1/deal-discovery/by-points/?points=500
```

**Description:** Get deals filtered by specific point range.

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "merchant_logo": "http://localhost:8000/media/merchant/logo/pizza_logo.jpg",
      "title": "Food Delivery Service",
      "points_offered": 500.0,
      "points_remaining": 500.0
    }
  ]
}
```

### Deal Requests

#### Create Deal Request

```http
POST /api/custom_auth/v1/merchant-deal-requests/
```

**Description:** Request to work on a deal with fixed point system.

**Request Body:**

```json
{
  "deal": 1,
  "message": "I can provide delivery services in Mumbai"
}
```

**Important Notes:**

- `points_requested` is automatically set to the deal's `points_offered`
- No negotiation allowed - fixed point system
- Only one request per deal per merchant allowed

**Response:**

```json
{
  "id": 1,
  "requesting_merchant": 2,
  "requesting_merchant_name": "Delivery Co",
  "requesting_merchant_logo": "http://localhost:8000/media/merchant/logo/delivery_logo.jpg",
  "deal": 1,
  "deal_title": "Food Delivery Service",
  "deal_merchant": "Pizza Palace",
  "deal_merchant_logo": "http://localhost:8000/media/merchant/logo/pizza_logo.jpg",
  "status": "pending",
  "points_requested": 500.0
}
```

#### Accept Deal Request

```http
POST /api/custom_auth/v1/merchant-deal-requests/{id}/accept/
```

**Description:** Accept a deal request with fixed points.

**Response:**

```json
{
  "message": "Deal request accepted successfully"
}
```

#### Reject Deal Request

```http
POST /api/custom_auth/v1/merchant-deal-requests/{id}/reject/
```

**Description:** Reject a deal request.

**Response:**

```json
{
  "message": "Deal request rejected successfully"
}
```

### Deal Confirmations

#### Get Deal Confirmations

```http
GET /api/custom_auth/v1/merchant-deal-confirmations/
```

**Description:** Get deal confirmations for the current merchant.

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "deal": 1,
      "deal_title": "Food Delivery Service",
      "merchant1": 1,
      "merchant1_name": "Pizza Palace",
      "merchant1_logo": "http://localhost:8000/media/merchant/logo/pizza_logo.jpg",
      "merchant2": 2,
      "merchant2_name": "Delivery Co",
      "merchant2_logo": "http://localhost:8000/media/merchant/logo/delivery_logo.jpg",
      "status": "confirmed",
      "points_exchanged": 500.0,
      "confirmation_time": "2024-01-01T10:30:00Z"
    }
  ]
}
```

#### Complete Deal

```http
POST /api/custom_auth/v1/merchant-deal-confirmations/{id}/complete/
```

**Description:** Complete a deal and transfer points automatically.

**Response:**

```json
{
  "message": "Deal completed and points transferred successfully"
}
```

### Notifications

#### Get Notifications

```http
GET /api/custom_auth/v1/merchant-notifications/
```

**Description:** Get merchant notifications.

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "notification_type": "deal_request",
      "title": "New Deal Request!",
      "message": "Delivery Co requested your deal 'Food Delivery Service' for 500 points",
      "is_read": false,
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### Mark Notification as Read

```http
POST /api/custom_auth/v1/merchant-notifications/{id}/mark_read/
```

**Description:** Mark a notification as read.

**Response:**

```json
{
  "message": "Notification marked as read"
}
```

#### Mark All Notifications as Read

```http
POST /api/custom_auth/v1/merchant-notifications/mark_all_read/
```

**Description:** Mark all notifications as read.

**Response:**

```json
{
  "message": "All notifications marked as read"
}
```

#### Get Unread Count

```http
GET /api/custom_auth/v1/merchant-notifications/unread_count/
```

**Description:** Get count of unread notifications.

**Response:**

```json
{
  "unread_count": 5
}
```

### Deal Statistics

#### Get Deal Stats

```http
GET /api/custom_auth/v1/deal-stats/
```

**Description:** Get overall deal statistics for the merchant.

**Response:**

```json
{
  "total_deals": 10,
  "active_deals": 5,
  "total_requests": 15,
  "successful_deals": 8,
  "total_points_offered": 5000.0,
  "total_points_used": 3000.0
}
```

## 🔄 Business Logic

### Fixed Point Deal System

The merchant deal system operates on a **fixed point model** where:

- **No Negotiation**: Points offered are fixed and cannot be negotiated
- **Take It or Leave It**: Merchants must accept the exact point amount offered
- **Automatic Assignment**: `points_requested` is automatically set to `deal.points_offered`
- **Simplified Process**: Eliminates complex counter-offer negotiations

### Deal Creation Process

1. **Deal Creation**: Merchant creates deal with fixed points offer
2. **Point Deduction**: Points are deducted from merchant's wallet immediately
3. **Deal Activation**: Deal becomes available for other merchants
4. **Point Locking**: Points are locked until deal completion or expiry

### Deal Request Process

1. **Deal Discovery**: Other merchants browse available deals with merchant logos
2. **Deal Request**: Merchant requests to work on a deal (points auto-set)
3. **Request Review**: Deal creator reviews the request
4. **Accept/Reject**: Deal creator accepts or rejects the request
5. **Confirmation**: Both merchants confirm the deal with fixed points

### Deal Completion Process

1. **Deal Confirmation**: Both merchants agree on the deal with fixed points
2. **Work Completion**: Work is completed as per deal terms
3. **Point Transfer**: Points are automatically transferred (fixed amount)
4. **Deal Completion**: Deal status is updated to completed
5. **Usage Tracking**: Point usage is recorded in DealPointUsage

### Point Usage Flow

#### Merchant-to-Merchant Flow

```
Merchant A Wallet → Points Deducted → Deal Created → Merchant B Works → Points Transferred to Merchant B
```

#### Key Points:

- Points are deducted from creator's wallet when deal is created
- Points are transferred to requester when deal is completed
- All transactions are tracked in WalletHistory and DealPointUsage
- Points can only be used by the receiving merchant

## 💼 Use Cases

### For Merchants

1. **Deal Management**:

   - Create deals and offer points
   - Work on other merchants' deals for points
   - Filter deals by category and location
   - Monitor deal performance

2. **Point Exchange**:

   - Exchange points with other merchants
   - Track point usage and transfers
   - Monitor wallet balance

3. **Analytics & Insights**:
   - Track deal performance
   - Monitor point usage
   - Analyze deal success rates
   - View transaction history

## ⚠️ Error Handling

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Insufficient points in wallet",
  "status": 400
}
```

```json
{
  "error": "You cannot request your own deal",
  "status": 400
}
```

#### 401 Unauthorized

```json
{
  "error": "Authentication required",
  "status": 401
}
```

#### 403 Forbidden

```json
{
  "error": "Merchant access required",
  "status": 403
}
```

#### 404 Not Found

```json
{
  "error": "Deal not found",
  "status": 404
}
```

#### 409 Conflict

```json
{
  "error": "Deal request already exists",
  "status": 409
}
```

## 🖼️ Merchant Logo Integration

### Logo Display in API Responses

All deal-related API responses now include merchant logos for better visual identification:

- **Deal Lists**: Shows merchant logo for each deal
- **Deal Requests**: Shows both requesting merchant and deal creator logos
- **Deal Confirmations**: Shows both merchant logos involved
- **Deal Discovery**: Shows merchant logos in search results

### Logo URL Format

```json
{
  "merchant_logo": "http://localhost:8000/media/merchant/logo/merchant_logo.jpg"
}
```

### Logo Handling

- **Safe Context Access**: Handles cases where request context might not be available
- **Fallback URLs**: Returns relative URLs if absolute URLs can't be generated
- **Null Handling**: Returns `null` if merchant has no logo
- **No Breaking Changes**: Existing API functionality remains unchanged

## 🔒 Security Considerations

1. **Authentication**: All endpoints require JWT token authentication
2. **Authorization**: Merchants can only access their own data
3. **Point Validation**: System validates sufficient points before deal creation
4. **Data Validation**: All input data is validated and sanitized
5. **Atomic Transactions**: All point transfers are atomic and secure
6. **Audit Trail**: Complete transaction history is maintained
7. **Fixed Point Security**: No point manipulation through negotiation

## 📊 Integration Points

### Wallet System Integration

- Points are deducted from merchant wallet when creating deals
- Points are transferred between merchant wallets when deals complete
- All transactions are tracked in WalletHistory

### Notification System

- Real-time notifications for deal requests
- Email/SMS notifications for deal status changes
- Merchant notifications for point transfers

### Deal Discovery

- Advanced filtering by category, location, and points
- Search functionality for finding relevant deals
- Recommendation system for matching merchants

## 📋 Complete API Endpoints Summary

### Merchant Deals

- `GET /api/custom_auth/v1/merchant-deals/` - List merchant's deals
- `POST /api/custom_auth/v1/merchant-deals/` - Create new deal
- `GET /api/custom_auth/v1/merchant-deals/{id}/` - Get deal details
- `PUT /api/custom_auth/v1/merchant-deals/{id}/` - Update deal
- `POST /api/custom_auth/v1/merchant-deals/{id}/activate/` - Activate deal
- `POST /api/custom_auth/v1/merchant-deals/{id}/deactivate/` - Deactivate deal
- `GET /api/custom_auth/v1/merchant-deals/{id}/usage_history/` - Get usage history

### Deal Discovery

- `GET /api/custom_auth/v1/deal-discovery/` - Discover available deals
- `GET /api/custom_auth/v1/deal-discovery/by_points/` - Filter by point range

### Deal Requests

- `GET /api/custom_auth/v1/merchant-deal-requests/` - List deal requests
- `POST /api/custom_auth/v1/merchant-deal-requests/` - Create deal request
- `POST /api/custom_auth/v1/merchant-deal-requests/{id}/accept/` - Accept request
- `POST /api/custom_auth/v1/merchant-deal-requests/{id}/reject/` - Reject request

### Deal Confirmations

- `GET /api/custom_auth/v1/merchant-deal-confirmations/` - List confirmations
- `POST /api/custom_auth/v1/merchant-deal-confirmations/{id}/complete/` - Complete deal
- `GET /api/custom_auth/v1/merchant-deal-confirmations/{id}/usage_history/` - Get usage history

### Notifications

- `GET /api/custom_auth/v1/merchant-notifications/` - List notifications
- `POST /api/custom_auth/v1/merchant-notifications/{id}/mark_read/` - Mark as read
- `POST /api/custom_auth/v1/merchant-notifications/mark_all_read/` - Mark all as read
- `GET /api/custom_auth/v1/merchant-notifications/unread_count/` - Get unread count

### Statistics

- `GET /api/custom_auth/v1/deal-stats/` - Get deal statistics

## 🎯 Key Features Summary

✅ **Fixed Point Deals** - No negotiation, take it or leave it system  
✅ **Merchant Logos** - Visual identification in all API responses  
✅ **Point Conversion** - 1 Rupee = 10 Points  
✅ **Real-time Notifications** - Instant updates for all activities  
✅ **Complete Audit Trail** - Full transaction history tracking  
✅ **Location Filtering** - Find deals by city and location  
✅ **Category Filtering** - Filter deals by business category  
✅ **Automatic Point Transfer** - Seamless point exchange system  
✅ **Deal Management** - Full CRUD operations for deals  
✅ **Security** - JWT authentication and data validation
