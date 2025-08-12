import { useNavigate } from "react-router-dom";
import { navigateToHome } from "../../store/actions/navigateAction";

const NotFound = () => {
    const navigate = useNavigate();

    const handleHomeClick = () => {
        navigateToHome(navigate);
    };

    return (
        <div className="not-found__container">
            <div className="img__container">
                {/* <img src={NotFoundImg} /> */}
            </div>
            <div className="not-fount__text">
                <h2>Page Not Found</h2>
                <p>
                We can&apos;t see to find a page you are looking for. Don&apos;t worry
                and try it out again.
                </p>
            </div>
            <div className="not-found__actions">
                <button onClick={handleHomeClick}>Back to home</button>
            </div>
        </div>
    )
};

export default NotFound
