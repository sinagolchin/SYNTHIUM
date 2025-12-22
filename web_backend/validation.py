"""
Validation system for empirical testing
Created by Sina Golchin & Maysam BaygMuhammady
"""
import asyncio
import json
import csv
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthium_core.vectors import SynthiumVector


class SynthiumValidator:
    """Validates Synthium predictions against empirical data"""

    def __init__(self, engine):
        self.engine = engine
        self.validation_results = []
        self.validation_protocols = self._load_validation_protocols()

    def _load_validation_protocols(self) -> Dict:
        """Load standard validation protocols"""
        return {
            "phenomenon_validation": {
                "description": "Validate vector predictions for specific phenomena",
                "metrics": ["vector_correlation", "phase_accuracy", "wellbeing_correlation"],
                "success_criteria": {
                    "vector_correlation": 0.7,
                    "phase_accuracy": 0.8,
                    "wellbeing_correlation": 0.6
                }
            },
            "intervention_efficacy": {
                "description": "Test effectiveness of Synthium interventions",
                "metrics": ["pre_post_effect_size", "user_satisfaction", "adherence_rate"],
                "success_criteria": {
                    "effect_size": 0.5,
                    "satisfaction": 4.0,  # out of 5
                    "adherence": 0.7  # 70%
                }
            }
        }

    async def validate_phenomenon(self,
                                phenomenon_id: int,
                                empirical_data: List[Dict]) -> Dict:
        """Validate a phenomenon against empirical data"""
        print(f"Validating phenomenon {phenomenon_id}...")

        # Get predicted vector
        phenomenon = self.engine.db.get_phenomenon(phenomenon_id)
        if not phenomenon:
            return {"error": f"Phenomenon {phenomenon_id} not found"}

        predicted_vector = self.engine.estimate_phenomenon_vector(phenomenon)

        # Calculate correlations
        correlations = self._calculate_correlations(predicted_vector, empirical_data)

        # Calculate phase accuracy
        phase_accuracy = self._calculate_phase_accuracy(phenomenon, empirical_data)

        # Calculate wellbeing correlation
        wellbeing_corr = self._calculate_wellbeing_correlation(predicted_vector, empirical_data)

        result = {
            "phenomenon_id": phenomenon_id,
            "phenomenon_name": phenomenon.term,
            "predicted_vector": predicted_vector.to_dict(),
            "validation_metrics": {
                "vector_correlation": round(correlations["overall"], 3),
                "phase_accuracy": round(phase_accuracy, 3),
                "wellbeing_correlation": round(wellbeing_corr, 3)
            },
            "validation_passed": self._evaluate_validation_result(correlations, phase_accuracy, wellbeing_corr),
            "timestamp": datetime.now().isoformat(),
            "sample_size": len(empirical_data)
        }

        self.validation_results.append(result)
        return result

    def _calculate_correlations(self,
                              predicted_vector: SynthiumVector,
                              empirical_data: List[Dict]) -> Dict:
        """Calculate correlations between predicted and empirical vectors"""
        if not empirical_data:
            return {"v": 0.0, "R": 0.0, "r": 0.0, "C": 0.0, "S": 0.0, "overall": 0.0}

        # Extract empirical vectors
        empirical_vectors = []
        for entry in empirical_data:
            if "vector" in entry:
                empirical_vectors.append(SynthiumVector.from_dict(entry["vector"]))

        if not empirical_vectors:
            return {"v": 0.0, "R": 0.0, "r": 0.0, "C": 0.0, "S": 0.0, "overall": 0.0}

        # Calculate average empirical vector
        avg_v = sum(v.v for v in empirical_vectors) / len(empirical_vectors)
        avg_R = sum(v.R for v in empirical_vectors) / len(empirical_vectors)
        avg_r = sum(v.r for v in empirical_vectors) / len(empirical_vectors)
        avg_C = sum(v.C for v in empirical_vectors) / len(empirical_vectors)
        avg_S = sum(v.S for v in empirical_vectors) / len(empirical_vectors)

        # Calculate component-wise correlations (simplified)
        corr_v = 1.0 / (1.0 + abs(predicted_vector.v - avg_v))
        corr_R = 1.0 / (1.0 + abs(predicted_vector.R - avg_R))
        corr_r = 1.0 / (1.0 + abs(predicted_vector.r - avg_r))
        corr_C = 1.0 / (1.0 + abs(predicted_vector.C - avg_C))
        corr_S = 1.0 / (1.0 + abs(predicted_vector.S - avg_S))

        overall = (corr_v + corr_R + corr_r + corr_C + corr_S) / 5

        return {
            "v": round(corr_v, 3),
            "R": round(corr_R, 3),
            "r": round(corr_r, 3),
            "C": round(corr_C, 3),
            "S": round(corr_S, 3),
            "overall": round(overall, 3)
        }

    def _calculate_phase_accuracy(self,
                                phenomenon: Any,
                                empirical_data: List[Dict]) -> float:
        """Calculate accuracy of phase prediction"""
        if not empirical_data:
            return 0.0

        phase_matches = 0
        total = 0

        for entry in empirical_data:
            if "phase" in entry:
                total += 1
                if entry["phase"] == phenomenon.phase:
                    phase_matches += 1

        if total == 0:
            return 0.0

        return phase_matches / total

    def _calculate_wellbeing_correlation(self,
                                       predicted_vector: SynthiumVector,
                                       empirical_data: List[Dict]) -> float:
        """Calculate correlation between predicted and empirical wellbeing"""
        if not empirical_data:
            return 0.0

        predicted_wellbeing = self.engine.calculate_wellbeing(predicted_vector)

        empirical_wellbeing_scores = []
        for entry in empirical_data:
            if "wellbeing" in entry:
                empirical_wellbeing_scores.append(entry["wellbeing"])
            elif "vector" in entry:
                vec = SynthiumVector.from_dict(entry["vector"])
                empirical_wellbeing_scores.append(self.engine.calculate_wellbeing(vec))

        if not empirical_wellbeing_scores:
            return 0.0

        avg_empirical = sum(empirical_wellbeing_scores) / len(empirical_wellbeing_scores)

        # Simple correlation measure
        correlation = 1.0 / (1.0 + abs(predicted_wellbeing - avg_empirical))
        return correlation

    def _evaluate_validation_result(self,
                                  correlations: Dict,
                                  phase_accuracy: float,
                                  wellbeing_corr: float) -> bool:
        """Evaluate if validation passes success criteria"""
        protocol = self.validation_protocols["phenomenon_validation"]
        criteria = protocol["success_criteria"]

        return (correlations["overall"] >= criteria["vector_correlation"] and
                phase_accuracy >= criteria["phase_accuracy"] and
                wellbeing_corr >= criteria["wellbeing_correlation"])

    async def run_validation_study(self,
                                 phenomenon_ids: List[int],
                                 participant_data: Dict[str, List[Dict]]) -> Dict:
        """Run a complete validation study"""
        print(f"Running validation study for {len(phenomenon_ids)} phenomena...")

        results = {}
        for pid in phenomenon_ids:
            # Get data for this phenomenon
            phenomenon_data = []
            for participant_id, data_list in participant_data.items():
                for entry in data_list:
                    if entry.get("phenomenon_id") == pid:
                        phenomenon_data.append(entry)

            # Validate
            result = await self.validate_phenomenon(pid, phenomenon_data)
            results[pid] = result

            status = "✅ PASS" if result.get("validation_passed") else "❌ FAIL"
            print(f"  Phenomenon {pid}: {status} (correlation: {result.get('validation_metrics', {}).get('vector_correlation', 0)})")

        # Summary statistics
        passed = sum(1 for r in results.values() if r.get("validation_passed"))
        total = len(results)

        return {
            "study_id": f"study_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "summary": {
                "total_phenomena": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": round(passed / total, 3) if total > 0 else 0.0
            },
            "detailed_results": results,
            "recommendations": self._generate_validation_recommendations(results)
        }

    def _generate_validation_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        low_correlation = []
        for pid, result in results.items():
            if result.get("validation_metrics", {}).get("vector_correlation", 0) < 0.6:
                low_correlation.append(pid)

        if low_correlation:
            recommendations.append(
                f"Re-evaluate vector mappings for phenomena: {low_correlation[:5]}"
            )

        return recommendations

    def export_validation_results(self,
                                format: str = "json",
                                filepath: Optional[str] = None) -> str:
        """Export validation results to file"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"validation_results_{timestamp}.{format}"

        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "engine_version": "2.1.0",
                "total_validations": len(self.validation_results)
            },
            "results": self.validation_results
        }

        if format == "json":
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == "csv":
            self._export_to_csv(filepath, data)
        else:
            raise ValueError(f"Unsupported format: {format}")

        print(f"Results exported to {filepath}")
        return filepath

    def _export_to_csv(self, filepath: str, data: Dict):
        """Export to CSV format"""
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow([
                "phenomenon_id", "phenomenon_name",
                "vector_correlation", "phase_accuracy", "wellbeing_correlation",
                "validation_passed", "sample_size", "timestamp"
            ])

            # Write data
            for result in data["results"]:
                writer.writerow([
                    result["phenomenon_id"],
                    result["phenomenon_name"],
                    result["validation_metrics"]["vector_correlation"],
                    result["validation_metrics"]["phase_accuracy"],
                    result["validation_metrics"]["wellbeing_correlation"],
                    result["validation_passed"],
                    result["sample_size"],
                    result["timestamp"]
                ])
