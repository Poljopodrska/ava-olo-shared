import React, { useState, useEffect } from 'react';
import { ConstitutionalDesignChecker } from '../../utils/constitutional-design-checker';
import ConstitutionalCard from './ConstitutionalCard';

/**
 * Design Compliance Dashboard - Principle #14: DESIGN-FIRST
 * Real-time monitoring of constitutional design compliance
 */
const DesignComplianceDashboard = () => {
    const [complianceData, setComplianceData] = useState([]);
    const [overallScore, setOverallScore] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [lastCheck, setLastCheck] = useState(null);

    useEffect(() => {
        scanComponentCompliance();
        
        // Auto-refresh every 30 seconds
        const interval = setInterval(scanComponentCompliance, 30000);
        return () => clearInterval(interval);
    }, []);

    const scanComponentCompliance = async () => {
        setIsLoading(true);
        try {
            // In a real implementation, this would scan actual component files
            const mockResults = await checkAllComponents();
            setComplianceData(mockResults);
            
            // Calculate overall score
            const score = mockResults.length > 0 
                ? (mockResults.filter(c => c.compliant).length / mockResults.length) * 100 
                : 0;
            setOverallScore(score);
            setLastCheck(new Date().toLocaleString());
        } catch (error) {
            console.error('Constitutional design compliance check failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Mock component scanning (replace with actual file system scanning)
    const checkAllComponents = async () => {
        const mockComponents = [
            {
                name: 'ConstitutionalHeader.jsx',
                path: 'src/components/constitutional/ConstitutionalHeader.jsx',
                compliant: true,
                score: 100,
                violations: []
            },
            {
                name: 'ConstitutionalCard.jsx', 
                path: 'src/components/constitutional/ConstitutionalCard.jsx',
                compliant: true,
                score: 100,
                violations: []
            },
            {
                name: 'ConstitutionalInput.jsx',
                path: 'src/components/constitutional/ConstitutionalInput.jsx', 
                compliant: true,
                score: 100,
                violations: []
            },
            {
                name: 'LegacyComponent.jsx',
                path: 'src/components/legacy/LegacyComponent.jsx',
                compliant: false,
                score: 45,
                violations: [
                    {
                        type: 'COLOR_VIOLATION',
                        message: 'Non-constitutional color detected',
                        severity: 'ERROR'
                    },
                    {
                        type: 'FONT_SIZE_VIOLATION',
                        message: 'Font size below 18px minimum',
                        severity: 'ERROR'
                    },
                    {
                        type: 'ENTER_KEY_VIOLATION',
                        message: 'Missing Enter key functionality',
                        severity: 'ERROR'
                    }
                ]
            }
        ];

        return mockComponents;
    };

    const getComplianceIcon = (compliant) => {
        return compliant ? '✅' : '❌';
    };

    const getScoreColor = (score) => {
        if (score >= 80) return 'var(--success-green)';
        if (score >= 60) return 'var(--warning-orange)';
        return 'var(--error-red)';
    };

    const getSeverityIcon = (severity) => {
        switch (severity) {
            case 'ERROR': return '🚨';
            case 'WARNING': return '⚠️';
            case 'INFO': return 'ℹ️';
            default: return '❓';
        }
    };

    return (
        <ConstitutionalCard
            title="🎨 Constitutional Design Compliance Dashboard"
            badge="🏛️ Principle #14"
            status={{ type: overallScore >= 80 ? 'success' : 'error', text: `${overallScore.toFixed(1)}% Compliant` }}
        >
            {/* Overall Status */}
            <div className="constitutional-grid" style={{ marginBottom: 'var(--spacing-lg)' }}>
                <div className="constitutional-card" style={{ textAlign: 'center', padding: 'var(--spacing-md)' }}>
                    <div style={{ fontSize: 'var(--font-title)', color: getScoreColor(overallScore), fontWeight: 'bold' }}>
                        {overallScore.toFixed(1)}%
                    </div>
                    <div style={{ fontSize: 'var(--font-medium)', color: 'var(--medium-gray)' }}>
                        Overall Compliance
                    </div>
                </div>
                
                <div className="constitutional-card" style={{ textAlign: 'center', padding: 'var(--spacing-md)' }}>
                    <div style={{ fontSize: 'var(--font-title)', color: 'var(--primary-olive)', fontWeight: 'bold' }}>
                        {complianceData.filter(c => c.compliant).length}/{complianceData.length}
                    </div>
                    <div style={{ fontSize: 'var(--font-medium)', color: 'var(--medium-gray)' }}>
                        Compliant Components
                    </div>
                </div>
                
                <div className="constitutional-card" style={{ textAlign: 'center', padding: 'var(--spacing-md)' }}>
                    <div style={{ fontSize: 'var(--font-title)', color: 'var(--error-red)', fontWeight: 'bold' }}>
                        {complianceData.reduce((total, c) => total + c.violations.length, 0)}
                    </div>
                    <div style={{ fontSize: 'var(--font-medium)', color: 'var(--medium-gray)' }}>
                        Total Violations
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div style={{ marginBottom: 'var(--spacing-lg)', display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
                <button 
                    className="constitutional-btn constitutional-btn-primary"
                    onClick={scanComponentCompliance}
                    disabled={isLoading}
                >
                    {isLoading ? '🔄 Scanning...' : '🔍 Scan Components'}
                </button>
                
                <button className="constitutional-btn constitutional-btn-secondary">
                    📋 Export Report
                </button>
                
                <button className="constitutional-btn constitutional-btn-success">
                    🛠️ Auto-Fix Violations
                </button>
            </div>

            {/* Component List */}
            <div className="compliance-component-list">
                <h3 style={{ marginBottom: 'var(--spacing-md)', color: 'var(--primary-brown)' }}>
                    📂 Component Compliance Status
                </h3>
                
                {complianceData.map((component, index) => (
                    <div 
                        key={index} 
                        className="compliance-item"
                        style={{
                            padding: 'var(--spacing-md)',
                            marginBottom: 'var(--spacing-sm)',
                            background: component.compliant ? 'rgba(107, 139, 35, 0.1)' : 'rgba(196, 84, 80, 0.1)',
                            border: `2px solid ${component.compliant ? 'var(--success-green)' : 'var(--error-red)'}`,
                            borderRadius: 'var(--border-radius)'
                        }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-sm)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
                                <span style={{ fontSize: 'var(--font-heading)' }}>
                                    {getComplianceIcon(component.compliant)}
                                </span>
                                <div>
                                    <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>
                                        {component.name}
                                    </div>
                                    <div style={{ fontSize: 'var(--font-small)', color: 'var(--medium-gray)' }}>
                                        {component.path}
                                    </div>
                                </div>
                            </div>
                            
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ 
                                    fontSize: 'var(--font-large)', 
                                    fontWeight: 'bold',
                                    color: getScoreColor(component.score)
                                }}>
                                    {component.score}%
                                </div>
                                <div style={{ fontSize: 'var(--font-small)', color: 'var(--medium-gray)' }}>
                                    Score
                                </div>
                            </div>
                        </div>
                        
                        {/* Violations */}
                        {component.violations.length > 0 && (
                            <div className="violations-list">
                                <div style={{ fontWeight: 'bold', marginBottom: 'var(--spacing-xs)', fontSize: 'var(--font-medium)' }}>
                                    🚨 Constitutional Violations:
                                </div>
                                {component.violations.map((violation, vIndex) => (
                                    <div 
                                        key={vIndex} 
                                        className="violation-item"
                                        style={{
                                            padding: 'var(--spacing-sm)',
                                            marginBottom: 'var(--spacing-xs)',
                                            background: 'rgba(255, 255, 255, 0.7)',
                                            borderRadius: '4px',
                                            borderLeft: `4px solid ${violation.severity === 'ERROR' ? 'var(--error-red)' : 'var(--warning-orange)'}`
                                        }}
                                    >
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
                                            <span>{getSeverityIcon(violation.severity)}</span>
                                            <span style={{ fontWeight: 'bold', fontSize: 'var(--font-small)' }}>
                                                {violation.type}:
                                            </span>
                                            <span style={{ fontSize: 'var(--font-small)' }}>
                                                {violation.message}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Constitutional Requirements */}
            <div style={{ 
                marginTop: 'var(--spacing-lg)', 
                padding: 'var(--spacing-md)',
                background: 'var(--cream)',
                borderRadius: 'var(--border-radius)',
                border: '2px solid var(--primary-olive)'
            }}>
                <h4 style={{ color: 'var(--primary-brown)', marginBottom: 'var(--spacing-sm)' }}>
                    🏛️ Constitutional Design Requirements (Principle #14)
                </h4>
                <div className="constitutional-grid">
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>🎨 Color Palette:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>Brown & olive agricultural theme</div>
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>📱 Typography:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>18px+ minimum for older farmers</div>
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>⌨️ Accessibility:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>Enter key functionality required</div>
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>📱 Layout:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>Mobile-first responsive design</div>
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>⚛️ Branding:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>Atomic structure logo required</div>
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: 'var(--font-medium)' }}>🛠️ Philosophy:</div>
                        <div style={{ fontSize: 'var(--font-small)' }}>Functionality before beauty</div>
                    </div>
                </div>
            </div>

            {/* Last Check Info */}
            {lastCheck && (
                <div style={{ 
                    marginTop: 'var(--spacing-md)',
                    fontSize: 'var(--font-small)',
                    color: 'var(--medium-gray)',
                    textAlign: 'center'
                }}>
                    Last compliance check: {lastCheck}
                </div>
            )}
        </ConstitutionalCard>
    );
};

export default DesignComplianceDashboard;