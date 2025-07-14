import React from 'react';

/**
 * Constitutional Input Component - Principle #14: DESIGN-FIRST
 * Features:
 * - MANDATORY Enter key functionality (constitutional requirement)
 * - 18px+ font size for older farmers
 * - Constitutional styling
 * - Accessibility compliant
 */
const ConstitutionalInput = ({ 
    label, 
    placeholder, 
    type = "text", 
    onEnterPress, 
    buttonId,
    value,
    onChange,
    className = "",
    required = false,
    ...props 
}) => {
    const handleEnterKey = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            
            // Execute onEnterPress callback if provided
            if (onEnterPress) {
                onEnterPress();
            }
            
            // Click associated button if buttonId provided
            if (buttonId) {
                const button = document.getElementById(buttonId);
                if (button) {
                    button.click();
                }
            }
        }
    };

    return (
        <div className={`constitutional-form-group ${className}`}>
            {label && (
                <label className="constitutional-label">
                    {label}
                    {required && <span style={{ color: 'var(--error-red)' }}> *</span>}
                </label>
            )}
            <input
                type={type}
                placeholder={placeholder}
                className="constitutional-input"
                value={value}
                onChange={onChange}
                onKeyPress={handleEnterKey}
                required={required}
                {...props}
            />
        </div>
    );
};

/**
 * Constitutional Select Component
 */
export const ConstitutionalSelect = ({
    label,
    options = [],
    value,
    onChange,
    onEnterPress,
    buttonId,
    className = "",
    required = false,
    placeholder = "Select option...",
    ...props
}) => {
    const handleEnterKey = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (onEnterPress) onEnterPress();
            if (buttonId) document.getElementById(buttonId)?.click();
        }
    };

    return (
        <div className={`constitutional-form-group ${className}`}>
            {label && (
                <label className="constitutional-label">
                    {label}
                    {required && <span style={{ color: 'var(--error-red)' }}> *</span>}
                </label>
            )}
            <select
                className="constitutional-select"
                value={value}
                onChange={onChange}
                onKeyPress={handleEnterKey}
                required={required}
                {...props}
            >
                {placeholder && <option value="">{placeholder}</option>}
                {options.map((option, index) => (
                    <option key={index} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

/**
 * Constitutional Textarea Component
 */
export const ConstitutionalTextarea = ({
    label,
    placeholder,
    value,
    onChange,
    onEnterPress,
    buttonId,
    className = "",
    required = false,
    rows = 4,
    ...props
}) => {
    const handleEnterKey = (event) => {
        // For textarea, only trigger on Ctrl+Enter or Cmd+Enter
        if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            if (onEnterPress) onEnterPress();
            if (buttonId) document.getElementById(buttonId)?.click();
        }
    };

    return (
        <div className={`constitutional-form-group ${className}`}>
            {label && (
                <label className="constitutional-label">
                    {label}
                    {required && <span style={{ color: 'var(--error-red)' }}> *</span>}
                </label>
            )}
            <textarea
                className="constitutional-textarea"
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                onKeyPress={handleEnterKey}
                required={required}
                rows={rows}
                {...props}
            />
        </div>
    );
};

export default ConstitutionalInput;