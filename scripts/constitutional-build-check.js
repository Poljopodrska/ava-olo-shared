#!/usr/bin/env node

/**
 * Constitutional Design Build Checker - Principle #14: DESIGN-FIRST
 * 🏛️ ERROR-LEVEL ENFORCEMENT: Build fails if design violated
 * 
 * This script integrates with build processes to enforce constitutional design compliance
 * Usage: node scripts/constitutional-build-check.js [path]
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

// Import constitutional design checker
const { ConstitutionalDesignChecker, ConstitutionalDesignError } = require('../src/utils/constitutional-design-checker');

class ConstitutionalBuildChecker {
    constructor(options = {}) {
        this.options = {
            failOnWarnings: false,
            failOnErrors: true,
            excludePatterns: ['node_modules/**', 'dist/**', 'build/**', '.git/**'],
            includePatterns: ['**/*.jsx', '**/*.js', '**/*.css', '**/*.html'],
            ...options
        };
        
        this.violations = [];
        this.totalFiles = 0;
        this.compliantFiles = 0;
    }

    async checkAllFiles(rootPath = '.') {
        console.log('🏛️ CONSTITUTIONAL DESIGN BUILD CHECK - Principle #14');
        console.log('=' * 60);
        console.log('🎨 Enforcing constitutional design compliance...\n');

        try {
            // Find all relevant files
            const files = await this.findRelevantFiles(rootPath);
            this.totalFiles = files.length;

            console.log(`📁 Found ${files.length} files to check`);
            console.log('🔍 Checking constitutional design compliance...\n');

            // Check each file
            const results = [];
            for (const file of files) {
                try {
                    const result = await this.checkFile(file);
                    results.push(result);
                    
                    if (result.compliant) {
                        this.compliantFiles++;
                        console.log(`✅ ${file}`);
                    } else {
                        console.log(`❌ ${file} - ${result.violations.length} violations`);
                        this.violations.push(...result.violations.map(v => ({ ...v, file })));
                    }
                } catch (error) {
                    console.error(`💥 Error checking ${file}: ${error.message}`);
                    results.push({ 
                        file, 
                        compliant: false, 
                        violations: [{ 
                            type: 'CHECK_ERROR', 
                            message: error.message, 
                            severity: 'ERROR' 
                        }] 
                    });
                }
            }

            // Generate final report
            await this.generateBuildReport(results);
            
            // Determine if build should fail
            const shouldFail = this.shouldFailBuild();
            
            if (shouldFail) {
                console.error('\n🚨 BUILD FAILED: Constitutional design violations detected!');
                process.exit(1);
            } else {
                console.log('\n🎉 BUILD PASSED: Constitutional design compliance verified!');
                process.exit(0);
            }

        } catch (error) {
            console.error(`💥 Constitutional build check failed: ${error.message}`);
            process.exit(1);
        }
    }

    async findRelevantFiles(rootPath) {
        const files = [];
        
        for (const pattern of this.options.includePatterns) {
            const matches = await glob(pattern, {
                cwd: rootPath,
                ignore: this.options.excludePatterns,
                absolute: true
            });
            files.push(...matches);
        }
        
        // Remove duplicates
        return [...new Set(files)];
    }

    async checkFile(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const relativePath = path.relative(process.cwd(), filePath);
        
        try {
            const result = ConstitutionalDesignChecker.validateComponent(relativePath, content);
            return {
                file: relativePath,
                compliant: result.compliant,
                score: result.score,
                violations: []
            };
        } catch (error) {
            if (error instanceof ConstitutionalDesignError) {
                return {
                    file: relativePath,
                    compliant: false,
                    score: 0,
                    violations: error.violations
                };
            }
            throw error;
        }
    }

    shouldFailBuild() {
        const criticalViolations = this.violations.filter(v => v.severity === 'ERROR');
        const warningViolations = this.violations.filter(v => v.severity === 'WARNING');
        
        if (this.options.failOnErrors && criticalViolations.length > 0) {
            return true;
        }
        
        if (this.options.failOnWarnings && warningViolations.length > 0) {
            return true;
        }
        
        return false;
    }

    async generateBuildReport(results) {
        const complianceRate = this.totalFiles > 0 ? (this.compliantFiles / this.totalFiles * 100) : 0;
        const criticalViolations = this.violations.filter(v => v.severity === 'ERROR');
        const warningViolations = this.violations.filter(v => v.severity === 'WARNING');

        console.log('\n🏛️ CONSTITUTIONAL DESIGN COMPLIANCE REPORT');
        console.log('=' * 50);
        console.log(`📊 Overall Compliance: ${complianceRate.toFixed(1)}%`);
        console.log(`📁 Files Checked: ${this.totalFiles}`);
        console.log(`✅ Compliant Files: ${this.compliantFiles}`);
        console.log(`❌ Non-Compliant Files: ${this.totalFiles - this.compliantFiles}`);
        console.log(`🚨 Critical Violations: ${criticalViolations.length}`);
        console.log(`⚠️ Warning Violations: ${warningViolations.length}`);

        if (this.violations.length > 0) {
            console.log('\n🚨 CONSTITUTIONAL DESIGN VIOLATIONS:');
            console.log('-' * 40);
            
            // Group violations by file
            const violationsByFile = {};
            this.violations.forEach(violation => {
                if (!violationsByFile[violation.file]) {
                    violationsByFile[violation.file] = [];
                }
                violationsByFile[violation.file].push(violation);
            });

            Object.entries(violationsByFile).forEach(([file, violations]) => {
                console.log(`\n📁 ${file}:`);
                violations.forEach(violation => {
                    const icon = violation.severity === 'ERROR' ? '🚨' : '⚠️';
                    console.log(`   ${icon} ${violation.type}: ${violation.message}`);
                    if (violation.details) {
                        console.log(`      💡 ${violation.details}`);
                    }
                });
            });

            console.log('\n🏛️ CONSTITUTIONAL DESIGN REQUIREMENTS:');
            console.log('✅ Use brown & olive color palette (var(--primary-brown), var(--primary-olive))');
            console.log('✅ 18px+ font sizes for older farmers (var(--font-large))');
            console.log('✅ Enter key functionality on ALL inputs (onKeyPress handler)');
            console.log('✅ Mobile-first responsive design (@media queries)');
            console.log('✅ Constitutional classes (constitutional-btn, constitutional-card)');
            console.log('✅ Atomic logo in headers (electron1, electron2, electron3)');
            console.log('\n🥭 MANGO RULE: Design must work for Bulgarian mango farmers globally!');
        }

        // Save report to file
        const reportData = {
            timestamp: new Date().toISOString(),
            complianceRate,
            totalFiles: this.totalFiles,
            compliantFiles: this.compliantFiles,
            violations: this.violations,
            principle: 'DESIGN-FIRST',
            buildStatus: this.shouldFailBuild() ? 'FAILED' : 'PASSED'
        };

        const reportPath = path.join(process.cwd(), 'constitutional-design-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
        console.log(`\n📋 Detailed report saved to: ${reportPath}`);
    }
}

// CLI Usage
async function main() {
    const args = process.argv.slice(2);
    const rootPath = args[0] || '.';
    
    const options = {
        failOnWarnings: process.env.FAIL_ON_WARNINGS === 'true',
        failOnErrors: process.env.FAIL_ON_ERRORS !== 'false' // Default to true
    };

    const checker = new ConstitutionalBuildChecker(options);
    await checker.checkAllFiles(rootPath);
}

// Webpack Plugin Export
class ConstitutionalDesignWebpackPlugin {
    constructor(options = {}) {
        this.options = options;
    }

    apply(compiler) {
        compiler.hooks.emit.tapAsync('ConstitutionalDesignPlugin', async (compilation, callback) => {
            console.log('🏛️ Running Constitutional Design Check...');
            
            try {
                const checker = new ConstitutionalBuildChecker(this.options);
                
                // Check all assets
                Object.keys(compilation.assets).forEach(filename => {
                    if (filename.endsWith('.js') || filename.endsWith('.css') || filename.endsWith('.html')) {
                        try {
                            const source = compilation.assets[filename].source();
                            ConstitutionalDesignChecker.validateComponent(filename, source);
                        } catch (error) {
                            if (error instanceof ConstitutionalDesignError) {
                                compilation.errors.push(new Error(`Constitutional Design Violation in ${filename}: ${error.message}`));
                            }
                        }
                    }
                });
                
                callback();
            } catch (error) {
                callback(error);
            }
        });
    }
}

// Package.json scripts integration
const packageJsonScripts = {
    "check-design": "node scripts/constitutional-build-check.js",
    "check-design-strict": "FAIL_ON_WARNINGS=true node scripts/constitutional-build-check.js",
    "build": "npm run check-design && webpack build",
    "build-strict": "npm run check-design-strict && webpack build"
};

console.log('\n📦 Add these scripts to your package.json:');
console.log(JSON.stringify(packageJsonScripts, null, 2));

// Export for use as module
module.exports = {
    ConstitutionalBuildChecker,
    ConstitutionalDesignWebpackPlugin
};

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error('💥 Constitutional build check failed:', error);
        process.exit(1);
    });
}