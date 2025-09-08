# Merchant Deal System API Documentation

## 📋 Overview

The Merchant Deal System provides functionality for merchant-to-merchant point-based deal exchange. Merchants can create deals, discover other merchants' deals, and exchange points through a structured process.

## ✨ Key Features

- **Point-Based Deals**: Merchants can create deals and exchange points
- **Deal Discovery**: Find deals from other merchants
- **Point Exchange**: Automatic point transfer when deals are completed
- **Location-Based**: Deals can be filtered by city and location
- **Deal Management**: Create, update, activate, deactivate deals
- **Real-time Notifications**: Instant notifications for deal activities
- **Point Tracking**: Complete audit trail of point usage

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

Model to track merchant deal requests.

**Fields:**

- `requesting_merchant`: Merchant requesting the deal
- `deal`: Deal being requested
- `points_requested`: Points requested
- `status`: Request status (pending, accepted, rejected)
- `message`: Request message

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
POST /api/custom_auth/v1/deal-requests/
```

**Description:** Request to work on a deal.

**Request Body:**

```json
{
  "deal": 1,
  "message": "I can provide delivery services in Mumbai",
  "points_requested": 500.0
}
```

**Response:**

```json
{
  "id": 1,
  "requesting_merchant": 2,
  "requesting_merchant_name": "Delivery Co",
  "deal": 1,
  "deal_title": "Food Delivery Service",
  "status": "pending",
  "points_requested": 500.0
}
```

#### Accept Deal Request

```http
POST /api/custom_auth/v1/deal-requests/{id}/accept/
```

**Description:** Accept a deal request.

**Response:**

```json
{
  "message": "Deal request accepted successfully"
}
```

#### Reject Deal Request

```http
POST /api/custom_auth/v1/deal-requests/{id}/reject/
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
GET /api/custom_auth/v1/deal-confirmations/
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
      "merchant1_name": "Pizza Palace",
      "merchant2_name": "Delivery Co",
      "status": "confirmed",
      "points_exchanged": 500.0
    }
  ]
}
```

#### Complete Deal

```http
POST /api/custom_auth/v1/deal-confirmations/{id}/complete/
```

**Description:** Complete a deal and transfer points.

**Response:**

```json
{
  "message": "Deal completed and points transferred successfully"
}
```

### Notifications

#### Get Notifications

```http
GET /api/custom_auth/v1/notifications/
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
POST /api/custom_auth/v1/notifications/{id}/mark-read/
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
POST /api/custom_auth/v1/notifications/mark-all-read/
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
GET /api/custom_auth/v1/notifications/unread-count/
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

### Deal Creation Process

1. **Deal Creation**: Merchant creates deal with points offer
2. **Point Deduction**: Points are deducted from merchant's wallet
3. **Deal Activation**: Deal becomes available for other merchants
4. **Point Locking**: Points are locked until deal completion or expiry

### Deal Request Process

1. **Deal Discovery**: Other merchants browse available deals
2. **Deal Request**: Merchant requests to work on a deal
3. **Request Review**: Deal creator reviews the request
4. **Accept/Reject**: Deal creator accepts or rejects the request
5. **Confirmation**: Both merchants confirm the deal

### Deal Completion Process

1. **Deal Confirmation**: Both merchants agree on the deal
2. **Work Completion**: Work is completed as per deal terms
3. **Point Transfer**: Points are automatically transferred
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

## 🔒 Security Considerations

1. **Authentication**: All endpoints require JWT token authentication
2. **Authorization**: Merchants can only access their own data
3. **Point Validation**: System validates sufficient points before deal creation
4. **Data Validation**: All input data is validated and sanitized
5. **Atomic Transactions**: All point transfers are atomic and secure
6. **Audit Trail**: Complete transaction history is maintained

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
