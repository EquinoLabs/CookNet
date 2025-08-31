import './EmailVerification.scss'

export default function EmailVerificationSent() {
  return (
    <div className="email-sent-page">
      <div className='email-sent-container'>
        <h2>✅ Verification Email Sent</h2>
        <p>
          We have sent a verification link to your email address. Please check your inbox (or spam folder) to verify your account.
        </p>
        <div className="button-group">
          <a
            href="https://mail.google.com"
            target="_blank"
            rel="noopener noreferrer"
            className="open-gmail-button"
          >
            <img src="https://img.icons8.com/color/48/gmail-new.png" alt="gmail-new"/>
            Open Gmail
          </a>
          <a
            href="/"
            className="go-home-button"
          >
            Go to Home
          </a>
        </div>
      </div>
    </div>
  );
}
