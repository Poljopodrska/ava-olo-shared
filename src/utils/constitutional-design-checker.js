/**
 * Constitutional Design Compliance Checker - Principle #14: DESIGN-FIRST
 * 🏛️ ERROR-LEVEL ENFORCEMENT: Build fails if design violated
 * 
 * This checker validates all components against constitutional design requirements:
 * - Brown & olive color palette compliance
 * - 18px+ font sizes for older farmers
 * - Enter key functionality on all inputs
 * - Mobile responsiveness
 * - Constitutional branding
 */

class ConstitutionalDesignChecker {
    static CONSTITUTIONAL_COLORS = {
        '--primary-brown': '#6B5B73',
        '--primary-olive': '#8B8C5A',
        '--dark-olive': '#5D5E3F',
        '--light-olive': '#A8AA6B',
        '--accent-green': '#7A8B5A',
        '--earth-brown': '#8B7355',
        '--cream': '#F5F3F0',
        '--dark-charcoal': '#2C2C2C',
        '--medium-gray': '#666666',
        '--light-gray': '#E8E8E6',
        '--white': '#FFFFFF',
        '--error-red': '#C85450',
        '--success-green': '#6B8E23',
        '--warning-orange': '#D2691E'
    };

    static CONSTITUTIONAL_FONTS = {
        minSize: 18, // Minimum for older farmers
        allowedSizes: [
            'var(--font-large)', 
            'var(--font-medium)', 
            'var(--font-small)', 
            'var(--font-heading)', 
            'var(--font-title)'
        ]
    };

    static REQUIRED_CLASSES = [
        'constitutional-header',
        'constitutional-card',
        'constitutional-input',
        'constitutional-btn'
    ];

    /**
     * Main validation method - validates component for constitutional compliance
     */
    static validateComponent(componentPath, componentCode) {
        const violations = [];

        try {
            // Check colors
            const colorViolations = this.checkColors(componentCode);
            violations.push(...colorViolations);

            // Check font sizes
            const fontViolations = this.checkFontSizes(componentCode);
            violations.push(...fontViolations);

            // Check Enter key functionality
            const enterKeyViolations = this.checkEnterKeyFunctionality(componentCode);
            violations.push(...enterKeyViolations);

            // Check mobile responsiveness
            const mobileViolations = this.checkMobileResponsiveness(componentCode);
            violations.push(...mobileViolations);

            // Check constitutional classes
            const classViolations = this.checkConstitutionalClasses(componentCode);
            violations.push(...classViolations);

            // Check atomic logo implementation
            const logoViolations = this.checkAtomicLogo(componentCode);
            violations.push(...logoViolations);

            if (violations.length > 0) {
                throw new ConstitutionalDesignError(componentPath, violations);
            }

            return { 
                compliant: true, 
                score: 100,
                principles: ['DESIGN-FIRST'],
                message: '✅ Constitutional design compliance verified'
            };

        } catch (error) {
            if (error instanceof ConstitutionalDesignError) {
                throw error;
            }
            throw new ConstitutionalDesignError(componentPath, [{
                type: 'VALIDATION_ERROR',
                message: `❌ CONSTITUTIONAL DESIGN CHECKER ERROR`,
                details: `Validation failed: ${error.message}`,
                severity: 'ERROR'
            }]);
        }
    }

    /**
     * Check color compliance - only constitutional colors allowed
     */
    static checkColors(code) {
        const violations = [];
        
        // Check for non-constitutional hex colors
        const colorRegex = /#[0-9A-Fa-f]{6}\b/g;
        const foundColors = code.match(colorRegex) || [];
        
        foundColors.forEach(color => {
            const upperColor = color.toUpperCase();
            const isConstitutional = Object.values(this.CONSTITUTIONAL_COLORS)
                .some(constitutionalColor => constitutionalColor.toUpperCase() === upperColor);
                
            if (!isConstitutional) {
                violations.push({
                    type: 'COLOR_VIOLATION',
                    message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Non-constitutional color detected`,
                    details: `Found: ${color}\nExpected: Use constitutional color variables from design system\nFix: Replace with var(--primary-brown), var(--primary-olive), etc.\nConstitutional colors: ${Object.keys(this.CONSTITUTIONAL_COLORS).join(', ')}`,
                    severity: 'ERROR',
                    location: this.getLineNumber(code, color)
                });
            }
        });

        // Check for RGB colors (should use CSS variables)
        const rgbRegex = /rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)/g;
        const rgbMatches = code.match(rgbRegex) || [];
        
        rgbMatches.forEach(rgbColor => {
            violations.push({
                type: 'RGB_COLOR_VIOLATION',
                message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Direct RGB color usage`,
                details: `Found: ${rgbColor}\nExpected: Use constitutional CSS variables\nFix: Replace with constitutional color variables\nExample: var(--primary-brown) instead of rgb(107, 91, 115)`,
                severity: 'WARNING',
                location: this.getLineNumber(code, rgbColor)
            });
        });

        return violations;
    }

    /**
     * Check font size compliance - 18px minimum for accessibility
     */
    static checkFontSizes(code) {
        const violations = [];
        
        // Check for font sizes below minimum
        const fontSizeRegex = /font-size:\s*(\d+)px/g;
        let match;
        
        while ((match = fontSizeRegex.exec(code)) !== null) {
            const size = parseInt(match[1]);
            if (size < this.CONSTITUTIONAL_FONTS.minSize) {
                violations.push({
                    type: 'FONT_SIZE_VIOLATION',
                    message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Font size too small for older farmers`,
                    details: `Found: ${size}px\nExpected: Minimum ${this.CONSTITUTIONAL_FONTS.minSize}px for accessibility\nFix: Use var(--font-large) (18px) or larger\nReason: Older farmers need larger, more readable text`,
                    severity: 'ERROR',
                    location: this.getLineNumber(code, match[0])
                });
            }
        }

        // Check for missing font-size declarations in major elements
        if (code.includes('input') && !code.includes('font-size')) {
            violations.push({
                type: 'MISSING_FONT_SIZE',
                message: `⚠️ CONSTITUTIONAL DESIGN WARNING: Input missing explicit font size`,
                details: `Expected: All inputs should have explicit font-size\nFix: Add font-size: var(--font-large) to input elements\nReason: Ensures accessibility for older farmers`,
                severity: 'WARNING'
            });
        }

        return violations;
    }

    /**
     * Check Enter key functionality - MANDATORY on all inputs
     */
    static checkEnterKeyFunctionality(code) {
        const violations = [];
        
        // Check React components for input elements
        const inputRegex = /<input[^>]*>/g;
        const inputMatches = code.match(inputRegex) || [];
        
        inputMatches.forEach(inputElement => {
            // Check if input has onKeyPress, onKeyDown, or onEnterPress handler
            const hasEnterHandler = /on(KeyPress|KeyDown|EnterPress)/i.test(inputElement);
            
            if (!hasEnterHandler) {
                violations.push({
                    type: 'ENTER_KEY_VIOLATION',
                    message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Input missing Enter key functionality`,
                    details: `Found: ${inputElement.substring(0, 50)}...\nExpected: All inputs must handle Enter key press\nFix: Add onKeyPress={handleEnterKey} or onEnterPress prop\nReason: Farmers expect Enter key to submit forms (accessibility)`,
                    severity: 'ERROR',
                    location: this.getLineNumber(code, inputElement)
                });
            }
        });

        // Check for handleEnterKey function definition
        if (inputMatches.length > 0 && !code.includes('handleEnterKey') && !code.includes('onEnterPress')) {
            violations.push({
                type: 'MISSING_ENTER_HANDLER',
                message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Missing Enter key handler function`,
                details: `Expected: handleEnterKey function or onEnterPress prop\nFix: Implement Enter key handling logic\nExample: const handleEnterKey = (e) => { if (e.key === 'Enter') buttonRef.current.click(); }`,
                severity: 'ERROR'
            });
        }

        return violations;
    }

    /**
     * Check mobile responsiveness - mobile-first design required
     */
    static checkMobileResponsiveness(code) {
        const violations = [];
        
        // Check for media queries
        const hasMediaQueries = /@media/.test(code);
        
        // Check for responsive classes
        const hasResponsiveClasses = /responsive|mobile|tablet|desktop/.test(code);
        
        // Check for viewport meta tag (in HTML)
        const hasViewportMeta = /viewport.*width=device-width/.test(code);
        
        if (!hasMediaQueries && !hasResponsiveClasses && code.includes('style')) {
            violations.push({
                type: 'MOBILE_RESPONSIVENESS_VIOLATION',
                message: `⚠️ CONSTITUTIONAL DESIGN WARNING: Missing mobile responsiveness`,
                details: `Expected: Mobile-first responsive design\nFound: No responsive design indicators\nFix: Add @media queries or constitutional responsive classes\nExample: @media (max-width: 768px) { /* mobile styles */ }`,
                severity: 'WARNING'
            });
        }

        // Check for fixed pixel widths (should be responsive)
        const fixedWidthRegex = /width:\s*\d+px(?!\s*;?\s*max-width)/g;
        const fixedWidths = code.match(fixedWidthRegex) || [];
        
        if (fixedWidths.length > 0) {
            violations.push({
                type: 'FIXED_WIDTH_VIOLATION',
                message: `⚠️ CONSTITUTIONAL DESIGN WARNING: Fixed pixel widths detected`,
                details: `Found: ${fixedWidths.join(', ')}\nExpected: Responsive units (%, rem, em, vw)\nFix: Use flexible units or max-width instead\nReason: Ensures mobile compatibility`,
                severity: 'WARNING'
            });
        }

        return violations;
    }

    /**
     * Check for proper constitutional class usage
     */
    static checkConstitutionalClasses(code) {
        const violations = [];
        
        // Check if component uses constitutional classes
        const usesConstitutionalClasses = this.REQUIRED_CLASSES.some(className => 
            code.includes(className)
        );
        
        if (code.includes('className') && !usesConstitutionalClasses) {
            violations.push({
                type: 'CONSTITUTIONAL_CLASS_VIOLATION',
                message: `⚠️ CONSTITUTIONAL DESIGN WARNING: Non-constitutional classes detected`,
                details: `Expected: Use constitutional design system classes\nRequired classes: ${this.REQUIRED_CLASSES.join(', ')}\nFix: Replace custom classes with constitutional equivalents\nExample: className="constitutional-btn constitutional-btn-primary"`,
                severity: 'WARNING'
            });
        }

        return violations;
    }

    /**
     * Check atomic logo implementation in headers
     */
    static checkAtomicLogo(code) {
        const violations = [];
        
        // If this is a header component, check for atomic logo
        if (code.includes('header') || code.includes('Header')) {
            const hasAtomicLogo = code.includes('electron1') && 
                                 code.includes('electron2') && 
                                 code.includes('electron3');
            
            if (!hasAtomicLogo) {
                violations.push({
                    type: 'ATOMIC_LOGO_VIOLATION',
                    message: `❌ CONSTITUTIONAL DESIGN VIOLATION: Missing atomic structure logo`,
                    details: `Expected: All headers must include atomic structure logo\nFix: Add electron1, electron2, electron3 elements\nExample: <div className="constitutional-logo"><div className="electron1"></div>...\nReason: Constitutional branding requirement`,
                    severity: 'ERROR'
                });
            }
        }

        return violations;
    }

    /**
     * Get line number for better error reporting
     */
    static getLineNumber(code, searchString) {
        const index = code.indexOf(searchString);
        if (index === -1) return null;
        
        const beforeString = code.substring(0, index);
        const lineNumber = beforeString.split('\n').length;
        return lineNumber;
    }

    /**
     * Generate compliance report
     */
    static generateComplianceReport(results) {
        const report = {
            totalComponents: results.length,
            compliantComponents: results.filter(r => r.compliant).length,
            violationCount: results.reduce((total, r) => total + (r.violations?.length || 0), 0),
            overallScore: 0,
            details: results
        };

        // Calculate overall score
        if (report.totalComponents > 0) {
            report.overallScore = (report.compliantComponents / report.totalComponents) * 100;
        }

        return report;
    }
}

/**
 * Constitutional Design Error Class
 */
class ConstitutionalDesignError extends Error {
    constructor(componentPath, violations) {
        const errorMessage = `🏛️ CONSTITUTIONAL PRINCIPLE #14 VIOLATION in ${componentPath}

🚨 BUILD FAILED: Design compliance violations detected

${violations.map(v => `
❌ ${v.message}
📍 ${v.details}
🔧 Severity: ${v.severity}
${v.location ? `📋 Line: ${v.location}` : ''}
`).join('\n')}

🏛️ CONSTITUTIONAL DESIGN REQUIREMENTS:
✅ Use brown & olive color palette (var(--primary-brown), var(--primary-olive))
✅ 18px+ font sizes for older farmers (var(--font-large))
✅ Enter key functionality on ALL inputs (onKeyPress handler)
✅ Mobile-first responsive design (@media queries)
✅ Constitutional classes (constitutional-btn, constitutional-card)
✅ Atomic logo in headers (electron1, electron2, electron3)

🥭 MANGO RULE: Design must work for Bulgarian mango farmers globally!

Fix these violations to continue building.`;

        super(errorMessage);
        this.name = 'ConstitutionalDesignError';
        this.violations = violations;
        this.componentPath = componentPath;
        this.principle = 'DESIGN-FIRST';
    }
}

module.exports = { ConstitutionalDesignChecker, ConstitutionalDesignError };