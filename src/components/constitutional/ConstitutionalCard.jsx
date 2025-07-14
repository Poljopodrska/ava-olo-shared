import React from 'react';

/**
 * Constitutional Card Component - Principle #14: DESIGN-FIRST
 * Features:
 * - Constitutional badges
 * - Status indicators
 * - Brown & olive styling
 * - Accessible typography (18px minimum)
 */
const ConstitutionalCard = ({ 
    title,
    badge,
    children,
    status,
    className = ""
}) => {
    return (
        <div className={`constitutional-card ${className}`}>
            <div className="constitutional-card-header">
                <h2 className="constitutional-card-title">{title}</h2>
                <div style={{ display: 'flex', gap: 'var(--spacing-sm)', alignItems: 'center' }}>
                    {badge && (
                        <span className="constitutional-badge">{badge}</span>
                    )}
                    {status && (
                        <span className={`status status-${status.type}`}>
                            {status.text}
                        </span>
                    )}
                </div>
            </div>
            <div className="constitutional-card-content">
                {children}
            </div>
        </div>
    );
};

export default ConstitutionalCard;