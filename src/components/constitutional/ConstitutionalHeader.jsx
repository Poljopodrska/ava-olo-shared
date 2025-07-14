import React from 'react';

/**
 * Constitutional Header Component - Principle #14: DESIGN-FIRST
 * Features:
 * - Atomic structure logo (mandatory)
 * - Constitutional branding
 * - Brown & olive color scheme
 * - Mobile responsive
 */
const ConstitutionalHeader = ({ 
    title = "AVA OLO", 
    tagline = "Constitutional Agricultural CRM",
    className = ""
}) => {
    return (
        <header className={`constitutional-header ${className}`}>
            <div className="constitutional-logo">
                <div className="electron1"></div>
                <div className="electron2"></div>
                <div className="electron3"></div>
            </div>
            <div className="constitutional-brand">{title}</div>
            <div className="constitutional-tagline">{tagline}</div>
        </header>
    );
};

export default ConstitutionalHeader;