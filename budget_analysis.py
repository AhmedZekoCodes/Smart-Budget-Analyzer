# budget_analysis.py
import logging
from datetime import datetime
import numpy as np
from budget_interfaces import IAnalysisStrategy, Subject

logger = logging.getLogger(__name__)

class TrendAnalysisStrategy(IAnalysisStrategy):
    def analyze(self, transactions):
        total_credit = sum(t.get_amount() for t in transactions if 'Source:' in t.get_details())
        total_debit = sum(t.get_amount() for t in transactions if 'Destination:' in t.get_details())
        net_balance = total_credit - total_debit
        report = {
            'Total Credit': total_credit,
            'Total Debit': total_debit,
            'Net Balance': net_balance
        }
        logger.info("Trend analysis completed.")
        return report

class ClusteringStrategy(IAnalysisStrategy):
    def analyze(self, transactions):
        clusters = {}
        for t in transactions:
            cat = t.get_category()
            clusters.setdefault(cat, 0)
            clusters[cat] += t.get_amount()
        logger.info("Clustering analysis completed.")
        return clusters

class ForecastAnalysisStrategy(IAnalysisStrategy):
    def analyze(self, transactions):
        if not transactions:
            return {"Forecast": "No data"}
        dates = np.array([t.get_date().toordinal() for t in transactions])
        amounts = np.array([t.get_amount() for t in transactions])
        if len(dates) < 2:
            return {"Forecast": "Insufficient data for forecasting"}
        A = np.vstack([dates, np.ones(len(dates))]).T
        m, b = np.linalg.lstsq(A, amounts, rcond=None)[0]
        next_day = datetime.fromordinal(int(max(dates) + 1))
        forecast_amount = m * next_day.toordinal() + b
        report = {
            'Forecast Date': next_day.strftime('%Y-%m-%d'),
            'Forecast Amount': round(forecast_amount, 2),
            'Regression Slope': round(m, 4),
            'Regression Intercept': round(b, 4)
        }
        logger.info("Forecast analysis completed.")
        return report

# New advanced strategy: Anomaly Detection using standard deviation
class AnomalyDetectionStrategy(IAnalysisStrategy):
    def analyze(self, transactions):
        if not transactions:
            return {"Anomalies": "No data"}
        amounts = [t.get_amount() for t in transactions]
        mean = np.mean(amounts)
        std = np.std(amounts)
        # Flag transactions outside 2 standard deviations from the mean.
        anomalies = [t.get_details() for t in transactions if abs(t.get_amount() - mean) > 2 * std]
        report = {
            'Mean Amount': round(mean, 2),
            'Standard Deviation': round(std, 2),
            'Anomalies Found': len(anomalies),
            'Anomaly Details': anomalies if anomalies else "None"
        }
        logger.info("Anomaly detection analysis completed.")
        return report

class BudgetAnalyzer(Subject):
    def __init__(self, transactions):
        super().__init__()
        self.transactions = transactions
        self.strategy = None
    
    def set_strategy(self, strategy: IAnalysisStrategy):
        self.strategy = strategy
    
    def analyze(self):
        if self.strategy is None:
            raise Exception("No analysis strategy set.")
        report = self.strategy.analyze(self.transactions)
        self.notify("Analysis complete using " + self.strategy.__class__.__name__)
        return report
