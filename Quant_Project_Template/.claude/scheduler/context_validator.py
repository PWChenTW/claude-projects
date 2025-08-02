#!/usr/bin/env python3
"""
Context validation for ensuring comprehensive feature context.
Based on context-engineering principles.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ContextValidationResult:
    """Result of context validation check."""
    feature_name: str
    score: int  # 0-100
    has_examples: bool
    has_documentation: bool
    has_patterns: bool
    has_validation_criteria: bool
    missing_elements: List[str]
    recommendations: List[str]


class ContextValidator:
    """Validates that features have comprehensive context for implementation."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.specs_dir = self.project_root / ".kiro" / "specs"
        self.examples_dir = self.project_root / "docs" / "examples"
        self.initial_file = self.project_root / "INITIAL.md"
        
    def validate_feature_context(self, feature_name: str) -> ContextValidationResult:
        """
        Validate that feature has comprehensive context for implementation.
        
        Args:
            feature_name: Name of the feature to validate
            
        Returns:
            ContextValidationResult with validation details
        """
        feature_dir = self.specs_dir / feature_name
        
        # Check each context element
        has_examples = self._check_examples_exist(feature_name)
        has_documentation = self._check_documentation_references(feature_name)
        has_patterns = self._check_implementation_patterns(feature_name)
        has_validation = self._check_validation_criteria(feature_name)
        
        # Calculate score
        score = 0
        if has_examples:
            score += 25
        if has_documentation:
            score += 25
        if has_patterns:
            score += 25
        if has_validation:
            score += 25
            
        # Determine missing elements
        missing_elements = []
        recommendations = []
        
        if not has_examples:
            missing_elements.append("Code examples")
            recommendations.append("Add relevant code examples to docs/examples/ or reference existing patterns")
            
        if not has_documentation:
            missing_elements.append("Documentation references")
            recommendations.append("Include links to relevant API docs, tutorials, or specifications")
            
        if not has_patterns:
            missing_elements.append("Implementation patterns")
            recommendations.append("Reference similar implementations or architectural patterns")
            
        if not has_validation:
            missing_elements.append("Validation criteria")
            recommendations.append("Define clear success criteria and test scenarios")
            
        return ContextValidationResult(
            feature_name=feature_name,
            score=score,
            has_examples=has_examples,
            has_documentation=has_documentation,
            has_patterns=has_patterns,
            has_validation_criteria=has_validation,
            missing_elements=missing_elements,
            recommendations=recommendations
        )
    
    def _check_examples_exist(self, feature_name: str) -> bool:
        """Check if relevant code examples are available."""
        # Check for examples in feature spec
        feature_dir = self.specs_dir / feature_name
        
        # Check requirements.md for example references
        requirements_file = feature_dir / "requirements.md"
        if requirements_file.exists():
            content = requirements_file.read_text().lower()
            if any(keyword in content for keyword in ["example", "sample", "pattern", "reference"]):
                return True
                
        # Check for blueprint with examples
        blueprint_file = feature_dir / "implementation_blueprint.md"
        if blueprint_file.exists():
            content = blueprint_file.read_text().lower()
            if "existing patterns" in content or "code examples" in content:
                return True
                
        # Check INITIAL.md
        if self.initial_file.exists():
            content = self.initial_file.read_text()
            if "## EXAMPLES" in content and len(content.split("## EXAMPLES")[1].split("##")[0].strip()) > 50:
                return True
                
        return False
    
    def _check_documentation_references(self, feature_name: str) -> bool:
        """Validate external documentation is referenced."""
        feature_dir = self.specs_dir / feature_name
        
        # Check various files for documentation references
        files_to_check = [
            feature_dir / "requirements.md",
            feature_dir / "implementation_blueprint.md",
            self.initial_file
        ]
        
        for file_path in files_to_check:
            if file_path.exists():
                content = file_path.read_text()
                # Look for URLs or documentation references
                if any(indicator in content for indicator in ["http://", "https://", "docs.", "documentation", "api reference"]):
                    return True
                    
        return False
    
    def _check_implementation_patterns(self, feature_name: str) -> bool:
        """Check for implementation patterns and architectural guidance."""
        feature_dir = self.specs_dir / feature_name
        
        # Check for implementation details
        blueprint_file = feature_dir / "implementation_blueprint.md"
        if blueprint_file.exists():
            content = blueprint_file.read_text().lower()
            if any(section in content for section in ["implementation plan", "pseudocode", "code structure"]):
                return True
                
        # Check for architectural patterns in examples
        if self.examples_dir.exists():
            pattern_indicators = ["pattern", "architecture", "structure", "design"]
            for pattern_file in self.examples_dir.rglob("*.md"):
                if any(indicator in pattern_file.stem.lower() for indicator in pattern_indicators):
                    return True
                    
        return False
    
    def _check_validation_criteria(self, feature_name: str) -> bool:
        """Check for clear validation and success criteria."""
        feature_dir = self.specs_dir / feature_name
        
        # Check spec.json for validation criteria
        spec_file = feature_dir / "spec.json"
        if spec_file.exists():
            spec_data = json.loads(spec_file.read_text())
            if spec_data.get("validation_criteria"):
                return True
                
        # Check other files for test/validation sections
        files_to_check = [
            feature_dir / "requirements.md",
            feature_dir / "implementation_blueprint.md"
        ]
        
        validation_keywords = ["test", "validation", "acceptance criteria", "success criteria", "verify"]
        
        for file_path in files_to_check:
            if file_path.exists():
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in validation_keywords):
                    return True
                    
        return False
    
    def validate_all_features(self) -> Dict[str, ContextValidationResult]:
        """Validate context for all features in the project."""
        results = {}
        
        if self.specs_dir.exists():
            for feature_dir in self.specs_dir.iterdir():
                if feature_dir.is_dir() and not feature_dir.name.startswith('.'):
                    result = self.validate_feature_context(feature_dir.name)
                    results[feature_dir.name] = result
                    
        return results
    
    def generate_report(self, results: Optional[Dict[str, ContextValidationResult]] = None) -> str:
        """Generate a comprehensive context validation report."""
        if results is None:
            results = self.validate_all_features()
            
        report_lines = [
            "# Context Validation Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"Total features analyzed: {len(results)}",
            ""
        ]
        
        # Calculate statistics
        if results:
            avg_score = sum(r.score for r in results.values()) / len(results)
            features_ready = sum(1 for r in results.values() if r.score >= 75)
            features_need_context = sum(1 for r in results.values() if r.score < 50)
            
            report_lines.extend([
                f"Average context score: {avg_score:.1f}/100",
                f"Features ready for implementation (≥75): {features_ready}",
                f"Features needing more context (<50): {features_need_context}",
                "",
                "## Feature Details",
                ""
            ])
            
            # Sort features by score (lowest first)
            sorted_features = sorted(results.items(), key=lambda x: x[1].score)
            
            for feature_name, result in sorted_features:
                status_emoji = "✅" if result.score >= 75 else "⚠️" if result.score >= 50 else "❌"
                
                report_lines.extend([
                    f"### {status_emoji} {feature_name} (Score: {result.score}/100)",
                    "",
                    "**Context Elements:**",
                    f"- Examples: {'✓' if result.has_examples else '✗'}",
                    f"- Documentation: {'✓' if result.has_documentation else '✗'}",
                    f"- Patterns: {'✓' if result.has_patterns else '✗'}",
                    f"- Validation: {'✓' if result.has_validation_criteria else '✗'}",
                    ""
                ])
                
                if result.missing_elements:
                    report_lines.extend([
                        "**Missing Elements:**",
                        *[f"- {element}" for element in result.missing_elements],
                        ""
                    ])
                    
                if result.recommendations:
                    report_lines.extend([
                        "**Recommendations:**",
                        *[f"- {rec}" for rec in result.recommendations],
                        ""
                    ])
                    
        return "\n".join(report_lines)
    
    def enforce_context_requirements(self, feature_name: str, min_score: int = 75) -> Tuple[bool, str]:
        """
        Enforce context requirements before allowing implementation.
        
        Args:
            feature_name: Feature to check
            min_score: Minimum required context score (default 75)
            
        Returns:
            Tuple of (is_valid, message)
        """
        result = self.validate_feature_context(feature_name)
        
        if result.score >= min_score:
            return True, f"Feature '{feature_name}' has sufficient context (score: {result.score}/100)"
        else:
            message = f"Feature '{feature_name}' lacks sufficient context (score: {result.score}/100)\n"
            message += "Missing elements:\n"
            for element in result.missing_elements:
                message += f"  - {element}\n"
            message += "\nPlease address these items before implementation."
            
            return False, message


def main():
    """CLI interface for context validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate feature context completeness")
    parser.add_argument("feature", nargs="?", help="Feature name to validate (omit for all features)")
    parser.add_argument("--min-score", type=int, default=75, help="Minimum required score")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    
    args = parser.parse_args()
    
    validator = ContextValidator()
    
    if args.report or not args.feature:
        # Generate report for all features
        report = validator.generate_report()
        print(report)
    else:
        # Validate specific feature
        is_valid, message = validator.enforce_context_requirements(args.feature, args.min_score)
        print(message)
        exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()