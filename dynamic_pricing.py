"""
[Cipher Engine] Dynamic Pricing & Automated Sales Tracker
윤자동 챌린지 다이내믹 프라이싱 메커니즘을 시뮬레이션 및 실제 서비스에 연동할 수 있는 자동화 코어 모듈
"""

import json
import os
import sys
from datetime import datetime

STATE_FILE = "sales_state.json"
BASE_PRICE = 70000  # 7만 미소
PRICE_UNIT = "미소"
PAYMENT_METHOD = "경제앱으로 박희망에게 입금"
TARGET_REVENUE = 10000000  # 1,000만 미소

class DynamicPricingEngine:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = {
                "total_sold": 0,
                "current_price": BASE_PRICE,
                "currency": PRICE_UNIT,
                "payment_method": PAYMENT_METHOD,
                "total_revenue": 0,
                "target_revenue": TARGET_REVENUE,
                "orders": []
            }
            self.save_state()

    def save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def record_order(self, buyer_name: str, buyer_email: str):
        sold_price = self.state["current_price"]
        self.state["total_sold"] += 1
        self.state["total_revenue"] += sold_price

        order_record = {
            "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.state['total_sold']:03d}",
            "buyer_name": buyer_name,
            "buyer_email": buyer_email,
            "paid_amount": f"{sold_price:,} {PRICE_UNIT}",
            "payment_method": PAYMENT_METHOD,
            "timestamp": datetime.now().isoformat()
        }
        self.state["orders"].append(order_record)
        self.save_state()

        progress_pct = (self.state["total_revenue"] / self.state["target_revenue"]) * 100
        print(f"[⚡ ORDER PROCESSED] #{self.state['total_sold']} - {buyer_name}님 주문 접수 ({sold_price:,} {PRICE_UNIT})")
        print(f"   ▶ 결제 수단: {PAYMENT_METHOD}")
        print(f"   ▶ 누적 매출: {self.state['total_revenue']:,} {PRICE_UNIT} / 목표 달성률: {progress_pct:.1f}%")
        return order_record

    def get_summary(self):
        return {
            "total_sold": self.state["total_sold"],
            "current_price": self.state["current_price"],
            "total_revenue": self.state["total_revenue"],
            "progress_percent": round((self.state["total_revenue"] / self.state["target_revenue"]) * 100, 2)
        }

if __name__ == "__main__":
    engine = DynamicPricingEngine()
    print("=== [Cipher] 다이내믹 프라이싱 엔진 초기화 완료 ===")
    summary = engine.get_summary()
    print(f"현재 판매 수량: {summary['total_sold']}권 | 현재 단가: {summary['current_price']:,} 미소 | 누적 매출: {summary['total_revenue']:,} 미소")

