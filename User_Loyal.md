# Simple Voucher System API Documentation

## 📋 Overview

The Simple Voucher System provides basic functionality for merchant-to-user voucher management. This system tracks user visits and allows merchants to give store-specific vouchers that users can use at the same store.

## ✨ Key Features

- **Simple Visit Tracking**: Track user visits to merchants
- **Store-Specific Vouchers**: Merchants can give vouchers to users for their store only
- **Voucher Management**: Create, use, and track vouchers
- **Expiry Management**: Automatic expiry tracking for vouchers
- **Basic Analytics**: Simple statistics for merchants

## 🏗️ System Architecture

### Models

#### SimpleVisit

Tracks user visits to merchants for basic analytics.

**Fields:**

- `user`: Foreign key to ApplicationUser
- `merchant`: Foreign key to MerchantProfile
- `visit_date`: Date and time of visit
- `notes`: Optional merchant notes about the visit

#### StoreVoucher

Simple voucher model for store-specific vouchers.

**Fields:**

- `voucher_code`: Unique voucher code
- `title`: Voucher title
- `description`: Voucher description
- `merchant`: Foreign key to MerchantProfile (store-specific)
- `user`: Foreign key to ApplicationUser
- `discount_type`: Percentage or fixed amount
- `discount_value`: Discount value
- `max_discount_amount`: Maximum discount for percentage vouchers
- `status`: Voucher status (active, used, expired, cancelled)
- `expiry_date`: When the voucher expires
- `used_at`: When the voucher was used
- `used_amount`: Amount of discount applied

## 🚀 API Endpoints

### 📍 Visit Tracking

#### Track User Visit

```http
POST /api/custom_auth/v1/simple-visits/track-visit/
```

**Description:** Track a user's visit to a merchant.

**Authentication:** Required (JWT Token)

**Request Headers:**

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "merchant_id": 1,
  "notes": "Customer came for lunch"
}
```

**Response:**

```json
{
  "message": "Visit tracked successfully",
  "visit": {
    "id": 1,
    "user": 1,
    "user_name": "John Doe",
    "merchant": 1,
    "merchant_name": "Pizza Palace",
    "visit_date": "2024-01-01T10:00:00Z",
    "notes": "Customer came for lunch",
    "create_time": "2024-01-01T10:00:00Z"
  }
}
```

#### Get Visit History

```http
GET /api/custom_auth/v1/simple-visits/
```

**Description:** Get user's visit history or merchant's visitor history.

**Authentication:** Required (JWT Token)

**Query Parameters:**

- `merchant`: Filter by merchant ID
- `page`: Page number for pagination
- `page_size`: Number of results per page

**Response:**

```json
{
  "count": 25,
  "next": "http://api.example.com/simple-visits/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_name": "John Doe",
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "visit_date": "2024-01-01T10:00:00Z",
      "notes": "Customer came for lunch",
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### 🎫 Voucher Management

#### Give Voucher to User

```http
POST /api/custom_auth/v1/store-vouchers/give-voucher/
```

**Description:** Merchant gives a voucher to a user for their store.

**Authentication:** Required (JWT Token - Merchant only)

**Request Body:**

```json
{
  "user_id": 1,
  "title": "Welcome Back Voucher",
  "description": "Special discount for our loyal customer",
  "discount_type": "percentage",
  "discount_value": 15.0,
  "max_discount_amount": 200.0,
  "expiry_date": "2024-02-15T23:59:59Z",
  "merchant_notes": "First time visitor bonus"
}
```

**Discount Types:**

- `percentage`: Percentage discount
- `fixed`: Fixed amount discount

**Response:**

```json
{
  "message": "Voucher given successfully",
  "voucher": {
    "id": 1,
    "voucher_code": "VOUCHER_A1B2C3D4",
    "title": "Welcome Back Voucher",
    "description": "Special discount for our loyal customer",
    "merchant": 1,
    "merchant_name": "Pizza Palace",
    "user": 1,
    "user_name": "John Doe",
    "discount_type": "percentage",
    "discount_value": 15.0,
    "max_discount_amount": 200.0,
    "status": "active",
    "expiry_date": "2024-02-15T23:59:59Z",
    "is_expired": false,
    "can_use": true,
    "create_time": "2024-01-01T10:00:00Z"
  }
}
```

#### Use Voucher

```http
POST /api/custom_auth/v1/store-vouchers/use-voucher/
```

**Description:** User uses a voucher at the store.

**Authentication:** Required (JWT Token)

**Request Body:**

```json
{
  "voucher_code": "VOUCHER_A1B2C3D4",
  "amount": 1000.0,
  "notes": "Used for dinner order"
}
```

**Response:**

```json
{
  "message": "Voucher used successfully",
  "discount_amount": 150.0,
  "final_amount": 850.0,
  "voucher": {
    "id": 1,
    "voucher_code": "VOUCHER_A1B2C3D4",
    "title": "Welcome Back Voucher",
    "status": "used",
    "used_at": "2024-01-15T19:30:00Z",
    "used_amount": 150.0,
    "usage_notes": "Used for dinner order",
    "is_expired": false,
    "can_use": false
  }
}
```

#### Get User's Vouchers

```http
GET /api/custom_auth/v1/store-vouchers/my-vouchers/
```

**Description:** Get user's vouchers or merchant's given vouchers.

**Authentication:** Required (JWT Token)

**Query Parameters:**

- `status`: Filter by voucher status (active, used, expired, cancelled)
- `merchant_id`: Filter by merchant ID
- `page`: Page number for pagination
- `page_size`: Number of results per page

**Response:**

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "voucher_code": "VOUCHER_A1B2C3D4",
      "title": "Welcome Back Voucher",
      "description": "Special discount for our loyal customer",
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "user": 1,
      "user_name": "John Doe",
      "discount_type": "percentage",
      "discount_value": 15.0,
      "max_discount_amount": 200.0,
      "status": "active",
      "expiry_date": "2024-02-15T23:59:59Z",
      "is_expired": false,
      "can_use": true,
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### Cancel Voucher

```http
POST /api/custom_auth/v1/store-vouchers/{id}/cancel-voucher/
```

**Description:** Merchant cancels a voucher.

**Authentication:** Required (JWT Token - Merchant only)

**Response:**

```json
{
  "message": "Voucher cancelled successfully"
}
```

#### Get Voucher Statistics

```http
GET /api/custom_auth/v1/store-vouchers/voucher-stats/
```

**Description:** Get voucher statistics for the merchant.

**Authentication:** Required (JWT Token - Merchant only)

**Response:**

```json
{
  "total_vouchers": 50,
  "active_vouchers": 30,
  "used_vouchers": 15,
  "expired_vouchers": 3,
  "cancelled_vouchers": 2
}
```

## 🔄 Business Logic

### Simple Voucher Flow

#### User to Merchant Flow

1. **User Visits Store** → `POST /simple-visits/track-visit/`
2. **Merchant Gives Voucher** → `POST /store-vouchers/give-voucher/`
3. **User Uses Voucher** → `POST /store-vouchers/use-voucher/`

#### Key Points:

- Vouchers are store-specific (can only be used at the merchant who gave them)
- No complex loyalty programs or auto-generation
- Simple visit tracking for basic analytics
- Vouchers have expiry dates and status tracking
- Merchants can cancel active vouchers

### Voucher Status Flow

```
Active → Used (when user uses voucher)
Active → Expired (when expiry date passes)
Active → Cancelled (when merchant cancels)
```

## 💼 Use Cases

### For Merchants

1. **Visit Tracking**:

   - Track customer visits to their store
   - View visitor history and patterns
   - Basic analytics on customer engagement

2. **Voucher Management**:

   - Give vouchers to customers
   - Track voucher usage and effectiveness
   - Cancel vouchers if needed
   - View voucher statistics

3. **Customer Engagement**:
   - Give vouchers to encourage repeat visits
   - Track which customers use vouchers
   - Monitor voucher redemption rates

### For Users

1. **Visit Tracking**:

   - Check in at merchant locations
   - Track visit history across merchants
   - Simple visit logging

2. **Voucher Management**:
   - View available vouchers
   - Use vouchers at merchant locations
   - Track voucher expiry dates
   - See voucher usage history

## ⚠️ Error Handling

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Voucher cannot be used",
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
  "error": "Only merchants can give vouchers",
  "status": 403
}
```

#### 404 Not Found

```json
{
  "error": "Merchant not found",
  "status": 404
}
```

#### 409 Conflict

```json
{
  "error": "Visit already tracked for today",
  "status": 409
}
```

## 🔒 Security Considerations

1. **Authentication**: All endpoints require JWT token authentication
2. **Authorization**: Users can only access their own data, merchants can only manage their vouchers
3. **Store-Specific**: Vouchers can only be used at the merchant who gave them
4. **Data Validation**: All input data is validated and sanitized
5. **Audit Trail**: All transactions are logged for security

## 📊 Integration Points

### Simple Analytics

- Basic visit tracking for merchants
- Voucher usage statistics
- Simple customer engagement metrics

### Voucher System

- Store-specific vouchers only
- Expiry management
- Status tracking (active, used, expired, cancelled)

## 🎯 Summary

This simplified voucher system provides:

- **Basic visit tracking** for analytics
- **Store-specific vouchers** that can only be used at the giving merchant
- **Simple voucher management** (create, use, cancel, track)
- **No complex loyalty programs** or auto-generation
- **Clean, focused functionality** for merchant-user interactions

The system is designed to be simple, easy to use, and focused on the core need: merchants giving vouchers to users for their specific store.
