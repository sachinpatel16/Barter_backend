# Meta WhatsApp Business API Integration

This document explains how to integrate and use Facebook Meta's WhatsApp Business API for sending gift card vouchers in the Bartr platform.

## Overview

The Meta WhatsApp Business API integration replaces the Twilio WhatsApp service for sending gift card vouchers. This provides better reliability, lower costs, and more features for WhatsApp messaging.

## Configuration

### Environment Variables

Add the following environment variables to your `.env` file:

```env
# Meta WhatsApp Business API Configuration
META_WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
META_WHATSAPP_ACCESS_TOKEN=your_access_token
META_WHATSAPP_API_VERSION=v18.0
META_WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
```

### Settings Configuration

The settings are automatically configured in `config/settings/base.py`:

```python
# Meta WhatsApp Business API Configuration
# --------------------------------------------------------------------------
META_WHATSAPP_PHONE_NUMBER_ID = env('META_WHATSAPP_PHONE_NUMBER_ID', default='')
META_WHATSAPP_ACCESS_TOKEN = env('META_WHATSAPP_ACCESS_TOKEN', default='')
META_WHATSAPP_API_VERSION = env('META_WHATSAPP_API_VERSION', default='v18.0')
META_WHATSAPP_BUSINESS_ACCOUNT_ID = env('META_WHATSAPP_BUSINESS_ACCOUNT_ID', default='')
```

## Setup Instructions

### 1. Create Meta Business Account

1. Go to [Facebook Business](https://business.facebook.com/)
2. Create a new business account or use existing one
3. Verify your business account

### 2. Create WhatsApp Business App

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app and select "Business" type
3. Add WhatsApp product to your app
4. Complete the setup wizard

### 3. Get Required Credentials

#### Phone Number ID

1. In your WhatsApp Business app dashboard
2. Go to WhatsApp > API Setup
3. Copy the "Phone number ID" (this is your `META_WHATSAPP_PHONE_NUMBER_ID`)

#### Access Token

1. In WhatsApp > API Setup
2. Generate a permanent access token
3. Copy the token (this is your `META_WHATSAPP_ACCESS_TOKEN`)

#### Business Account ID

1. In your app dashboard
2. Go to WhatsApp > API Setup
3. Copy the "WhatsApp Business Account ID" (this is your `META_WHATSAPP_BUSINESS_ACCOUNT_ID`)

### 4. Configure Webhook (Optional)

For receiving message status updates and incoming messages:

1. Set webhook URL: `https://yourdomain.com/api/v1/webhook/whatsapp/`
2. Subscribe to `messages` and `message_deliveries` events
3. Verify webhook with the provided token

## API Endpoints

### Gift Card Sharing

**Endpoint:** `POST /api/v1/voucher/{voucher_id}/share-gift-card/`

**Request Body:**

```json
{
  "phone_numbers": ["+919876543210", "+919876543211"]
}
```

**Response:**

```json
{
  "message": "Gift card shared successfully to 3 contacts",
  "success_count": 3,
  "failed_numbers": [],
  "shares_created": [
    {
      "phone_number": "+919876543210",
      "claim_reference": "GFT-123456",
      "share_id": 1
    }
  ]
}
```

### Test Meta WhatsApp

**Endpoint:** `POST /api/v1/whatsapp-contacts/test-meta-whatsapp-send/`

**Request Body:**

```json
{
  "phone_number": "+919876543210",
  "message": "Test message from Bartr"
}
```

**Response:**

```json
{
  "message": "Meta WhatsApp test message sent successfully",
  "phone_number": "919876543210",
  "message_id": "wamid.xxx",
  "status": "sent"
}
```

## Message Format

The gift card message sent via Meta WhatsApp includes:

```
🎁 *Gift Card: [Voucher Title]*

[Voucher Message]

🏪 *Merchant:* [Business Name]
📍 *Location:* [City], [State]

💳 *Voucher Type:* [Type]
💰 *Value:* [Value Description]

🔑 *Claim Reference:* [Reference]

To claim this gift card:
1. Visit: https://bartr.club/claim-gift-card/[reference]
2. Or show this reference to the merchant

*This gift card can only be claimed once by the recipient.*
```

## Phone Number Formatting

The system automatically formats phone numbers for Meta WhatsApp:

- **Input:** `9876543210` → **Output:** `919876543210`
- **Input:** `+919876543210` → **Output:** `919876543210`
- **Input:** `09876543210` → **Output:** `919876543210`

## Error Handling

### Common Error Codes

- **400 Bad Request:** Invalid phone number format or missing configuration
- **401 Unauthorized:** Invalid access token
- **403 Forbidden:** Phone number not registered on WhatsApp
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** Meta API server error

### Error Response Format

```json
{
  "error": "Failed to send Meta WhatsApp message",
  "status_code": 400,
  "error_details": {
    "error": {
      "message": "Invalid phone number",
      "type": "OAuthException",
      "code": 100
    }
  }
}
```

## Rate Limits

Meta WhatsApp Business API has the following rate limits:

- **Tier 1:** 1,000 messages per day
- **Tier 2:** 10,000 messages per day
- **Tier 3:** 100,000 messages per day
- **Tier 4:** 1,000,000 messages per day

Rate limits are automatically handled by the API.

## Testing

### 1. Test Configuration

Use the test endpoint to verify your configuration:

```bash
curl -X POST "https://yourdomain.com/api/v1/whatsapp-contacts/test-meta-whatsapp-send/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "message": "Test message from Bartr"
  }'
```

### 2. Test Gift Card Sharing

```bash
curl -X POST "https://yourdomain.com/api/v1/voucher/123/share-gift-card/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_numbers": ["+919876543210"]
  }'
```

## Troubleshooting

### Common Issues

1. **"Meta WhatsApp configuration missing"**

   - Check that all required environment variables are set
   - Verify the values are correct

2. **"Invalid phone number format"**

   - Ensure phone numbers are in correct format
   - Check the phone number formatting function

3. **"Phone number not registered on WhatsApp"**

   - Verify the recipient has WhatsApp installed
   - Check if the phone number is correct

4. **"Access token expired"**
   - Generate a new permanent access token
   - Update the environment variable

### Debug Mode

Enable debug logging by setting `DEBUG=True` in your Django settings. This will show detailed error messages and API responses.

## Migration from Twilio

If you're migrating from Twilio WhatsApp:

1. Update environment variables
2. Test the new Meta WhatsApp integration
3. Update any frontend code that handles WhatsApp responses
4. Monitor the new integration for any issues

## Support

For issues with Meta WhatsApp Business API:

1. Check [Meta WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
2. Review [Meta Business Help Center](https://www.facebook.com/business/help)
3. Contact Meta Business Support

For issues with the Bartr integration:

1. Check the application logs
2. Test with the provided test endpoints
3. Verify configuration settings

