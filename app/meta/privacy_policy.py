from fastapi.responses import HTMLResponse


def get_privacy_policy():
    return HTMLResponse(
        content="""
    <html>
    <head><title>Privacy Policy - Staff AI</title></head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h1>Privacy Policy for Staff AI</h1>
        <p>At Staff AI, we respect your privacy. This Privacy Policy explains how we collect, use, and protect information when businesses use our WhatsApp automation agent and when end users interact with that agent.</p>

        <h2>1. About Our Service</h2>
        <p>Staff AI provides a WhatsApp automation agent for businesses. The agent is available 24/7 to receive messages and answer customer queries on behalf of the business through the WhatsApp Business Platform.</p>

        <h2>2. Information We Collect</h2>
        <p>Depending on how you use our service, we may collect:</p>
        <ul>
            <li><strong>Business account information:</strong> business name, contact details, and WhatsApp Business account credentials needed to connect your account to our platform.</li>
            <li><strong>WhatsApp messaging data:</strong> phone numbers, message content, timestamps, and related metadata sent to or from your WhatsApp Business number.</li>
            <li><strong>Customer query data:</strong> questions, requests, and other information users share when messaging your business on WhatsApp.</li>
            <li><strong>Technical and usage data:</strong> logs, device or session information, and service performance data needed to operate and improve the agent.</li>
        </ul>

        <h2>3. How We Use Your Data</h2>
        <p>We use collected information solely to:</p>
        <ul>
            <li>Operate the WhatsApp automation agent and respond to user queries on behalf of your business.</li>
            <li>Provide 24/7 automated customer support and query handling through the WhatsApp Business API.</li>
            <li>Maintain conversation context so the agent can give relevant and accurate replies.</li>
            <li>Monitor, secure, and improve the reliability and quality of our service.</li>
        </ul>
        <p>We do not use your data for unrelated advertising or purposes outside of delivering our WhatsApp automation service.</p>

        <h2>4. Data Sharing</h2>
        <p>We do not sell, trade, or rent your personal information. We may share data only with:</p>
        <ul>
            <li><strong>Meta / WhatsApp:</strong> as required to send and receive messages through the WhatsApp Business Platform.</li>
            <li><strong>Service providers:</strong> trusted infrastructure or AI providers that help us operate the agent, under strict confidentiality and data protection obligations.</li>
            <li><strong>Legal requirements:</strong> when required by applicable law or to protect our rights, users, or the public.</li>
        </ul>

        <h2>5. Data Retention</h2>
        <p>We retain message and account data only for as long as needed to provide the service, maintain conversation history for your business, comply with legal obligations, or resolve disputes. You may request deletion of your business data subject to applicable law and operational requirements.</p>

        <h2>6. Data Security</h2>
        <p>We implement encryption, access controls, and secure storage practices to protect your data from unauthorized access, loss, or misuse.</p>

        <h2>7. Your Rights</h2>
        <p>Depending on your location, you may have the right to access, correct, delete, or restrict processing of your personal data. End users who message a business on WhatsApp should contact that business directly for privacy requests related to their conversation.</p>

        <h2>8. Contact Us</h2>
        <p>If you have any questions about this Privacy Policy or our WhatsApp automation service, contact us at <a href="mailto:info@staffai.ae">info@staffai.ae</a>.</p>

        <p>Last Updated: June 2026</p>
    </body>
    </html>
"""
    )


def get_terms_of_service():
    return HTMLResponse(
        content="""
    <html>
    <head><title>Terms of Service - Staff AI</title></head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px;">
        <h1>Terms of Service for Staff AI</h1>
        <p>By using Staff AI, you agree to the following terms of service:</p>
    </body>
    </html>
"""
    )