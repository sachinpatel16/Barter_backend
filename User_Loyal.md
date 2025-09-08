# User Loyalty System API Documentation

## 📋 Overview

The User Loyalty System provides comprehensive functionality for merchant-to-user loyalty programs. This system tracks user visits, automatically generates rewards, and manages reward expiry and usage.

## ✨ Key Features

- **Visit Tracking**: Track user visits to merchants (physical, online, purchase, redemption)
- **Automatic Rewards**: Generate gift vouchers, points, discounts, or free items based on visit frequency
- **Manual Rewards**: Merchants can give instant rewards without visit requirements
- **Expiry Management**: Automatic expiry tracking for rewards
- **Cooldown Periods**: Prevent spam rewards with configurable cooldown periods
- **Point Integration**: Seamless integration with wallet point system

## 🏗️ System Architecture

### Models

#### UserVisitTracking

Tracks user visits to merchants for loyalty program calculations.

**Fields:**

- `user`: Foreign key to ApplicationUser
- `merchant`: Foreign key to MerchantProfile
- `visit_date`: Date and time of visit
- `visit_type`: Type of visit (physical, online, purchase, redemption)
- `visit_notes`: Additional notes about the visit
- `location`: Specific location details

#### MerchantLoyaltyProgram

Merchant loyalty program configuration.

**Fields:**

- `merchant`: One-to-one relationship with MerchantProfile
- `is_active`: Whether the program is active
- `visits_required`: Number of visits required for reward
- `reward_type`: Type of reward (voucher, points, discount, free_item)
- `cooldown_days`: Days to wait before next reward

#### UserLoyaltyReward

Tracks loyalty rewards given to users.

**Fields:**

- `user`: Foreign key to ApplicationUser
- `merchant`: Foreign key to MerchantProfile
- `reward_type`: Type of reward given
- `status`: Reward status (pending, active, used, expired, cancelled)
- `expiry_date`: When the reward expires

## 🚀 API Endpoints

### 📍 Visit Tracking

#### Track User Visit

```http
POST /api/custom_auth/v1/visit-tracking/track-visit/
```

**Description:** Track a user's visit to a merchant and check for loyalty rewards.

**Authentication:** Required (JWT Token)

**Request Headers:**

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Location Examples:**

- `"Store Location - Ground Floor"`
- `"Main Branch - Mumbai"`
- `"Outlet 1 - Delhi"`
- `"Online Store"`
- `"Mobile App"`
- `"Drive-through"`
- `"Pickup Counter"`
- `"Home Delivery"`

**Request Body:**

```json
{
  "merchant_id": 1,
  "visit_type": "physical",
  "visit_notes": "Customer came for lunch",
  "location": "Store Location - Ground Floor"
}
```

**Visit Types:**

- `physical`: In-store visit
- `online`: Website/app visit
- `purchase`: Purchase made
- `redemption`: Voucher redeemed

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
    "visit_type": "physical",
    "visit_notes": "Customer came for lunch",
    "location": "Store Location - Ground Floor"
  },
  "loyalty_status": {
    "visits_count": 3,
    "visits_required": 3,
    "eligible_for_reward": true,
    "reward_generated": true
  }
}
```

#### Get Visit History

```http
GET /api/custom_auth/v1/visit-tracking/
```

**Description:** Get user's visit history or merchant's visitor history.

**Authentication:** Required (JWT Token)

**Query Parameters:**

- `merchant`: Filter by merchant ID
- `visit_type`: Filter by visit type (physical, online, purchase, redemption)
- `visit_date`: Filter by date
- `page`: Page number for pagination
- `page_size`: Number of results per page

**Response:**

```json
{
  "count": 25,
  "next": "http://api.example.com/visit-tracking/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_name": "John Doe",
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "visit_date": "2024-01-01T10:00:00Z",
      "visit_type": "physical",
      "visit_notes": "Customer came for lunch",
      "location": "Store Location - Ground Floor"
    }
  ]
}
```

### 🎯 Loyalty Programs

#### Create Loyalty Program

```http
POST /api/custom_auth/v1/loyalty-programs/
```

**Description:** Create a loyalty program for a merchant.

**Authentication:** Required (JWT Token - Merchant only)

**Request Body:**

```json
{
  "is_active": true,
  "visits_required": 3,
  "reward_type": "voucher",
  "voucher_title": "Welcome Back Voucher",
  "voucher_message": "Thank you for your loyalty!",
  "voucher_value": 50.0,
  "voucher_expiry_days": 30,
  "cooldown_days": 7
}
```

**Reward Types:**

- `voucher`: Gift voucher reward
- `points`: Points added to wallet
- `discount`: Discount percentage
- `free_item`: Free item reward

**Response:**

```json
{
  "id": 1,
  "merchant": 1,
  "merchant_name": "Pizza Palace",
  "is_active": true,
  "visits_required": 3,
  "reward_type": "voucher",
  "voucher_title": "Welcome Back Voucher",
  "voucher_value": 50.0,
  "voucher_expiry_days": 30,
  "cooldown_days": 7,
  "create_time": "2024-01-01T10:00:00Z"
}
```

#### Get Loyalty Program Stats

```http
GET /api/custom_auth/v1/loyalty-programs/stats/
```

**Description:** Get loyalty program statistics for the merchant.

**Authentication:** Required (JWT Token - Merchant only)

**Response:**

```json
{
  "total_visits": 150,
  "total_rewards_given": 25,
  "active_rewards": 15,
  "used_rewards": 8,
  "expired_rewards": 2,
  "total_points_given": 2500.0,
  "average_visits_per_user": 3.2,
  "top_visiting_users": [
    { "user__fullname": "John Doe", "visit_count": 12 },
    { "user__fullname": "Jane Smith", "visit_count": 8 }
  ],
  "recent_activity": {
    "visits_last_30_days": 45,
    "rewards_given_last_30_days": 8
  }
}
```

### 🎁 Loyalty Rewards

#### Get User Rewards

```http
GET /api/custom_auth/v1/loyalty-rewards/
```

**Description:** Get user's loyalty rewards or merchant's given rewards.

**Authentication:** Required (JWT Token)

**Query Parameters:**

- `status`: Filter by reward status (pending, active, used, expired, cancelled)
- `reward_type`: Filter by reward type (voucher, points, discount, free_item)
- `merchant`: Filter by merchant
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
      "user": 1,
      "user_name": "John Doe",
      "merchant": 1,
      "merchant_name": "Pizza Palace",
      "reward_type": "voucher",
      "status": "active",
      "voucher_title": "Welcome Back Voucher",
      "voucher_value": 50.0,
      "voucher_code": "LOYALTY_ABC123",
      "expiry_date": "2024-02-01T10:00:00Z",
      "is_expired": false,
      "create_time": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### Use Reward

```http
POST /api/custom_auth/v1/loyalty-rewards/{id}/use/
```

**Description:** Mark a loyalty reward as used.

**Authentication:** Required (JWT Token)

**Request Body:**

```json
{
  "location": "Store Location",
  "notes": "Used during lunch visit"
}
```

**Response:**

```json
{
  "message": "Reward used successfully",
  "reward": {
    "id": 1,
    "status": "used",
    "used_at": "2024-01-15T14:30:00Z",
    "usage_location": "Store Location",
    "usage_notes": "Used during lunch visit"
  }
}
```

#### Give Manual Reward

```http
POST /api/custom_auth/v1/loyalty-rewards/give-manual/
```

**Description:** Give manual reward to user (merchant can give anytime without visit requirements).

**Authentication:** Required (JWT Token - Merchant only)

**Request Body:**

```json
{
  "user_id": 1,
  "reward_type": "voucher",
  "voucher_title": "Special Gift Voucher",
  "voucher_message": "Thank you for being a valued customer!",
  "voucher_value": 100.0
}
```

**Response:**

```json
{
  "message": "Manual reward given successfully",
  "reward": {
    "id": 1,
    "user": 1,
    "user_name": "John Doe",
    "merchant": 1,
    "merchant_name": "Pizza Palace",
    "reward_type": "voucher",
    "status": "active",
    "voucher_title": "Special Gift Voucher",
    "voucher_value": 100.0,
    "voucher_code": "MANUAL_ABC12345",
    "expiry_date": "2024-02-15T10:00:00Z"
  }
}
```

**Manual Reward Types:**

1. **Voucher Reward:**

```json
{
  "user_id": 1,
  "reward_type": "voucher",
  "voucher_title": "Special Gift Voucher",
  "voucher_message": "Thank you for being a valued customer!",
  "voucher_value": 100.0
}
```

2. **Points Reward:**

```json
{
  "user_id": 1,
  "reward_type": "points",
  "points_amount": 500.0
}
```

3. **Discount Reward:**

```json
{
  "user_id": 1,
  "reward_type": "discount",
  "discount_percentage": 15.0,
  "discount_max_amount": 1000.0
}
```

4. **Free Item Reward:**

```json
{
  "user_id": 1,
  "reward_type": "free_item",
  "free_item_name": "Free Pizza",
  "free_item_description": "Get a free medium pizza with any order!"
}
```

## 🔄 Business Logic

### Loyalty Reward Generation

#### Automatic Rewards (Based on Visits)

1. **Visit Tracking**: When a user visits a merchant, the system tracks the visit
2. **Visit Counting**: System counts visits in the last 30 days
3. **Reward Eligibility**: If visits >= required visits, user becomes eligible
4. **Cooldown Check**: System checks if user got reward recently (cooldown period)
5. **Reward Generation**: If eligible and not in cooldown, reward is generated
6. **Automatic Points**: For point rewards, points are automatically added to wallet
7. **Wallet Integration**: Points are deducted from merchant's wallet when giving rewards

#### Manual Rewards (Merchant Can Give Anytime)

1. **No Visit Requirement**: Merchant can give rewards without any visit requirements
2. **Instant Reward**: Reward is created immediately when merchant gives it
3. **Custom Values**: Merchant can set custom voucher values, points, discounts
4. **Flexible Timing**: Can be given anytime, no cooldown restrictions
5. **Direct Points**: Points are added directly to user's wallet
6. **Wallet Deduction**: Points are deducted from merchant's wallet

### Point Usage Flow

#### Merchant-to-User Flow

```
Merchant Wallet → Points Deducted → User Reward Created → User Uses at Same Merchant
```

#### Key Points:

- Points are deducted from merchant's wallet when giving rewards
- User can only use rewards at the merchant who gave them
- All transactions are tracked in WalletHistory
- Reward expiry is automatically managed

## 💼 Use Cases

### For Merchants

1. **Loyalty Program Setup**:

   - Configure visit requirements (e.g., 3 visits = reward)
   - Set reward types (voucher, points, discount, free item)
   - Configure expiry and cooldown periods
   - Monitor program performance

2. **Customer Engagement**:

   - Track customer visit patterns
   - Give manual rewards for special occasions
   - Monitor reward usage and effectiveness

3. **Analytics & Insights**:
   - View detailed statistics
   - Track top visiting customers
   - Analyze loyalty program success

### For Users

1. **Visit Tracking**:

   - Check in at merchant locations
   - Track visit history across merchants
   - Monitor reward eligibility status

2. **Reward Management**:
   - View available rewards
   - Use rewards at merchant locations
   - Track reward expiry dates
   - Receive automatic rewards

## ⚠️ Error Handling

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Reward has expired",
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
2. **Authorization**: Users can only access their own data, merchants can only manage their programs
3. **Rate Limiting**: Visit tracking has built-in cooldown periods
4. **Data Validation**: All input data is validated and sanitized
5. **Point Security**: Wallet operations are atomic and secure
6. **Audit Trail**: All transactions are logged for security

## 📊 Integration Points

### Wallet System Integration

- Points are deducted from merchant wallet when giving rewards
- User wallet receives points for point-type rewards
- All transactions are tracked in WalletHistory

### Voucher System Integration

- Loyalty vouchers integrate with main voucher system
- Vouchers can be redeemed at merchant locations
- Expiry management is handled automatically

### Notification System

- Automatic notifications for reward generation
- Email/SMS notifications for reward expiry
- Merchant notifications for program statistics
