# WhatsApp Gift Card Sharing with Twilio Integration

This document explains how to use the updated WhatsApp gift card sharing functionality with Twilio integration.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The `twilio==8.10.0` package has been added to requirements.txt.

### 2. Environment Configuration

Add the following environment variables to your `.env` file:

```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token-here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### 3. Twilio Account Setup

1. Sign up for a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token from the Twilio Console
3. Set up WhatsApp Sandbox or get approval for WhatsApp Business API
4. Use the sandbox number `+14155238886` for testing

## API Endpoints

### 1. Share Gift Card via WhatsApp

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
  "message": "Gift card shared successfully to 2 contacts",
  "success_count": 2,
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

### 2. Test WhatsApp Message Sending

**Endpoint:** `POST /api/v1/voucher/whatsapp-contacts/test-whatsapp-send/`

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
  "message": "WhatsApp test message sent successfully",
  "phone_number": "+919876543210",
  "message_sid": "SM1234567890abcdef",
  "status": "queued"
}
```

## How It Works

### 1. Gift Card Sharing Flow

1. **User purchases a gift card** - Creates `UserVoucherRedemption` record
2. **User shares gift card** - Calls share endpoint with phone numbers
3. **System validates contacts** - Checks if contacts have WhatsApp
4. **Creates share records** - `GiftCardShare` records for each recipient
5. **Sends WhatsApp messages** - Uses Twilio to send formatted messages
6. **Recipients claim gift cards** - Using claim reference from message

### 2. WhatsApp Message Format

The system sends formatted WhatsApp messages like this:

```
🎁 *Gift Card: 50% Off Coffee*

Get 50% off on your next coffee purchase!

🏪 *Merchant:* Coffee Corner
📍 *Location:* Mumbai, Maharashtra

💳 *Voucher Type:* percentage
💰 *Value:* 50% off

⏰ *Valid Until:* December 31, 2024

🔑 *Claim Reference:* GFT-123456

To claim this gift card:
1. Visit: https://bartr.club/claim-gift-card/GFT-123456
2. Or show this reference to the merchant

*This gift card can only be claimed once by the recipient.*
```

### 3. Phone Number Formatting

The system automatically formats phone numbers for WhatsApp:

- `9876543210` → `+919876543210`
- `+919876543210` → `+919876543210` (unchanged)
- `whatsapp:+919876543210` → `whatsapp:+919876543210` (unchanged)

## Error Handling

The system handles various error scenarios:

1. **Invalid phone numbers** - Returns error for malformed numbers
2. **Twilio API errors** - Logs errors and returns failure status
3. **Network issues** - Graceful fallback with error logging
4. **Rate limiting** - Twilio handles rate limiting automatically

## Testing

### 1. Test Phone Number Validation

```bash
curl -X POST "https://your-domain.com/api/v1/voucher/whatsapp-contacts/test-whatsapp-validation/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210"}'
```

### 2. Test WhatsApp Message Sending

```bash
curl -X POST "https://your-domain.com/api/v1/voucher/whatsapp-contacts/test-whatsapp-send/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210", "message": "Test from Bartr"}'
```

## Production Considerations

1. **Replace sandbox number** - Use your approved WhatsApp Business number
2. **Monitor costs** - Twilio charges per message sent
3. **Rate limiting** - Implement proper rate limiting for bulk sends
4. **Error monitoring** - Set up proper logging and monitoring
5. **Message templates** - Use approved message templates for production

## Troubleshooting

### Common Issues

1. **"Invalid phone number format"** - Check phone number format and country code
2. **"Twilio authentication failed"** - Verify Account SID and Auth Token
3. **"Message not delivered"** - Check if recipient has WhatsApp and number is correct
4. **"Rate limit exceeded"** - Implement delays between bulk sends

### Debug Mode

Enable debug logging by setting `DEBUG=True` in your Django settings to see detailed error messages.

## Security Notes

1. **Never expose Auth Token** - Keep it in environment variables only
2. **Validate phone numbers** - Always validate before sending
3. **Rate limiting** - Implement proper rate limiting to prevent abuse
4. **Message content** - Ensure message content complies with WhatsApp policies
