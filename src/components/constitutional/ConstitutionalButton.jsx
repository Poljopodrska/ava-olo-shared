import React from 'react';

/**
 * Constitutional Button Component - Principle #14: DESIGN-FIRST
 * Features:
 * - Large size (48px minimum height) for accessibility
 * - 18px+ font size for older farmers
 * - Constitutional color variants
 * - Proper hover states
 */
const ConstitutionalButton = ({
    children,
    variant = "primary",
    onClick,
    disabled = false,
    type = "button",
    id,
    className = "",
    size = "normal",
    ...props
}) => {
    const getButtonClass = () => {
        let baseClass = "constitutional-btn";
        
        // Add variant class
        switch (variant) {
            case "primary":
                baseClass += " constitutional-btn-primary";
                break;
            case "secondary":
                baseClass += " constitutional-btn-secondary";
                break;
            case "success":
                baseClass += " constitutional-btn-success";
                break;
            case "error":
                baseClass += " constitutional-btn-error";
                break;
            default:
                baseClass += " constitutional-btn-primary";
        }
        
        // Add size modifications if needed
        if (size === "large") {
            baseClass += " constitutional-btn-large";
        }
        
        return `${baseClass} ${className}`;
    };

    return (
        <button
            type={type}
            id={id}
            className={getButtonClass()}
            onClick={onClick}
            disabled={disabled}
            {...props}
        >
            {children}
        </button>
    );
};

export default ConstitutionalButton;