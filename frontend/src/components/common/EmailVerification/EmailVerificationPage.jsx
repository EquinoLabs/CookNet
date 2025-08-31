import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { verifyEmail } from "../../../api/actions";
import './EmailVerification.scss'

export default function EmailVerificationPage() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("Verifying your email...");
  const [verified, setVerified] = useState(false);
  const [loading, setLoading] = useState(true);

  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setStatus("❌ Invalid verification link.");
      setLoading(false);
      return;
    }

    let mounted = true; // cleanup flag for StrictMode

    verifyEmail(token)
      .then((res) => {
        console.log("Verify API response:", res);
        if (mounted) {
          setVerified(true);
          setStatus("✅ Your email has been verified successfully!");
        }
      })
      .catch((err) => {
        console.error("Verify API error:", err);
        if (mounted) {
          setVerified(false);
          setStatus("⚠️ Unable to load verification status. You can try logging in to check your account.");
        }
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false; // prevent state updates if unmounted
    };
  }, [token]);

  return (
    <div className="verify-email-page">
        <div className="verify-email-container">
            {loading ? (
                <p>Verifying your email...</p>
            ) : (
                <div className="verify-email-content">
                    <h2>{status}</h2>
                    {verified ? (
                    <Link to="/login" className="login-link-button">
                        Go to Login
                    </Link>
                    ) : (
                    <Link to="/" className="home-link-button">
                        Go to Home
                    </Link>
                    )}
                </div>
            )}
        </div>
    </div>
  );
}
