import React, { createContext, useContext, useEffect, useState } from "react";
import { subscribe, emitToast } from "./ToastEmiiter";
import './ToastContext.scss';

const ToastContext = createContext();
export const useToast = () => useContext(ToastContext);

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = (title, message, type = "error") => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, title, message, type }]);

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 5000);
  };

  // listen for external emits
  useEffect(() => {
    const unsub = subscribe(showToast);
    return unsub;
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="toast-container">
        {toasts.map((toast) => (
            <div key={toast.id} className={`toast ${toast.type}`}>
                <div className="toast-content">
                    <div className="toast-title">{toast.title}</div>
                    <div className="toast-message">{toast.message}</div>
                </div>
                <button 
                    className="toast-close" 
                    onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
                >
                    ✖
                </button>
            </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};
